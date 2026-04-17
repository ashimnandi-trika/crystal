"""Pipeline — Stage-aware checking (local -> staging -> production)."""

from __future__ import annotations

Different strictness at each stage:
- LOCAL: lenient, you're still building
- STAGING: strict, no localhost, env vars must exist
- PRODUCTION: zero tolerance, all tests pass, no TODOs
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from crystal_guard.config import get_crystal_dir, walk_project_files, is_test_file
from crystal_guard.analyzers import Issue
import re


STAGES = ["local", "staging", "production"]

# What severity level blocks deployment at each stage
STAGE_THRESHOLDS = {
    "local": "critical",       # Only critical blocks local
    "staging": "high",         # Critical + high block staging
    "production": "medium",    # Critical + high + medium block production
}


def get_staging_issues(project_path: str) -> list[Issue]:
    """Extra checks that only apply at staging stage."""
    root = Path(project_path).resolve()
    issues = []

    # stg-001: No localhost URLs in non-config files
    for f in walk_project_files(project_path, {".py", ".js", ".jsx", ".ts", ".tsx"}):
        if is_test_file(f, root):
            continue
        if f.name in (".env", ".env.example", ".env.local"):
            continue
        try:
            content = f.read_text(errors="ignore")
            for i, line in enumerate(content.split("\n"), 1):
                if line.strip().startswith("#") or line.strip().startswith("//"):
                    continue
                if re.search(r'https?://localhost[:\d]*', line):
                    issues.append(Issue(
                        analyzer="staging",
                        severity="high",
                        file=str(f.relative_to(root)),
                        line=i,
                        rule_id="stg-001",
                        message="Localhost URL found. Staging and production need real URLs.",
                        suggestion="Replace with an environment variable like process.env.REACT_APP_API_URL.",
                        why="localhost only works on your computer. On a staging server, this URL points to nothing and your app breaks.",
                    ))
                    break
        except OSError:
            pass

    # stg-002: Check env vars referenced in code exist
    env_vars_used = set()
    env_patterns = [
        r'process\.env\.(\w+)',
        r'os\.environ\.get\(["\'](\w+)',
        r'os\.environ\[["\'](\w+)',
        r'os\.getenv\(["\'](\w+)',
    ]
    for f in walk_project_files(project_path, {".py", ".js", ".jsx", ".ts", ".tsx"}):
        if is_test_file(f, root):
            continue
        try:
            content = f.read_text(errors="ignore")
            for pattern in env_patterns:
                for match in re.finditer(pattern, content):
                    env_vars_used.add(match.group(1))
        except OSError:
            pass

    # Load env vars from .env files
    env_vars_defined = set()
    for env_file in [root / ".env", root / "backend" / ".env", root / "frontend" / ".env"]:
        if env_file.exists():
            try:
                for line in env_file.read_text().split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        env_vars_defined.add(line.split("=")[0].strip())
            except OSError:
                pass

    missing = env_vars_used - env_vars_defined - {"NODE_ENV", "HOME", "PATH", "USER", "SHELL"}
    for var in sorted(missing):
        # Skip common framework vars that are auto-set
        if var.startswith("npm_") or var.startswith("REACT_APP_BACKEND"):
            continue
        issues.append(Issue(
            analyzer="staging",
            severity="medium",
            file=".env",
            line=None,
            rule_id="stg-002",
            message=f"Environment variable {var} is used in code but not defined in any .env file.",
            suggestion=f"Add {var}=your_value to your .env file.",
            why=f"Your code tries to read {var} but it doesn't exist. The feature using it will crash or behave unexpectedly.",
        ))

    return issues


def get_production_issues(project_path: str, test_results: dict = None) -> list[Issue]:
    """Extra checks that only apply at production stage."""
    issues = []

    # prod-001: All tests must pass
    if test_results:
        if not test_results.get("ran"):
            issues.append(Issue(
                analyzer="production",
                severity="high",
                file="tests/",
                line=None,
                rule_id="prod-001",
                message="Tests could not be run. Production requires all tests to pass.",
                suggestion="Make sure your test runner (pytest/npm test) is installed and working.",
                why="Without running tests, there's no proof your app works. Something could be broken and you'd never know until real users hit it.",
            ))
        elif test_results.get("failed", 0) > 0:
            issues.append(Issue(
                analyzer="production",
                severity="critical",
                file="tests/",
                line=None,
                rule_id="prod-001",
                message=f"{test_results['failed']} test(s) failing. Production requires 100% pass rate.",
                suggestion="Fix all failing tests before deploying to production.",
                why="Failing tests mean known bugs. Deploying with known bugs means real users will hit them.",
            ))
    else:
        issues.append(Issue(
            analyzer="production",
            severity="high",
            file="tests/",
            line=None,
            rule_id="prod-001",
            message="No test results available. Run `crystal test` first.",
            suggestion="Run `crystal test` before production check.",
            why="Production deployment without running tests is like flying without checking the instruments.",
        ))

    # prod-002: Health score must be A
    # (This is enforced by threshold, not a separate check)

    return issues


def load_pipeline_state(project_path: str) -> dict:
    """Load pipeline state."""
    pipeline_path = get_crystal_dir(project_path) / "pipeline.json"
    if pipeline_path.exists():
        try:
            with open(pipeline_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"local": None, "staging": None, "production": None}


def save_pipeline_state(project_path: str, stage: str, passed: bool, score: int, issue_count: int):
    """Save pipeline state for a stage."""
    crystal_dir = get_crystal_dir(project_path)
    crystal_dir.mkdir(parents=True, exist_ok=True)

    state = load_pipeline_state(project_path)
    state[stage] = {
        "passed": passed,
        "score": score,
        "issue_count": issue_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # If a lower stage fails, invalidate higher stages
    stage_idx = STAGES.index(stage)
    if not passed:
        for higher in STAGES[stage_idx + 1:]:
            state[higher] = None

    with open(crystal_dir / "pipeline.json", "w") as f:
        json.dump(state, f, indent=2)


def check_stage_progression(project_path: str, target_stage: str) -> str | None:
    """Check if the target stage can be run (previous stage must pass)."""
    state = load_pipeline_state(project_path)
    idx = STAGES.index(target_stage)

    if idx == 0:
        return None  # Local can always run

    prev_stage = STAGES[idx - 1]
    prev_state = state.get(prev_stage)

    if prev_state is None:
        return f"Cannot run {target_stage} check. Run `crystal check --stage {prev_stage}` first."

    if not prev_state.get("passed"):
        return f"Cannot run {target_stage} check. {prev_stage.title()} check failed. Fix issues and re-run `crystal check --stage {prev_stage}` first."

    return None
