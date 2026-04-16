"""Session Handoff Generator — Feature 1 & 4.

Reads git state, file counts, test counts, runs quality gates, compares
baselines, and generates a structured prompt for the next AI coding session.
"""

import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path
from crystal_guard.config import (
    get_crystal_dir, walk_project_files, is_test_file, CODE_EXTENSIONS
)


def get_git_state(project_path: str) -> dict:
    """Read current git state."""
    root = Path(project_path).resolve()
    state = {
        "branch": None,
        "last_commits": [],
        "changed_files": [],
        "untracked_files": [],
        "has_git": False,
    }

    try:
        # Check if git repo
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, cwd=str(root), timeout=5
        )
        if result.returncode != 0:
            return state
        state["has_git"] = True

        # Current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=str(root), timeout=5
        )
        state["branch"] = result.stdout.strip() or "HEAD (detached)"

        # Last 5 commits
        result = subprocess.run(
            ["git", "log", "--oneline", "-5", "--no-decorate"],
            capture_output=True, text=True, cwd=str(root), timeout=5
        )
        state["last_commits"] = [
            line.strip() for line in result.stdout.strip().split("\n") if line.strip()
        ]

        # Changed files (staged + unstaged)
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=str(root), timeout=5
        )
        changed = [f for f in result.stdout.strip().split("\n") if f.strip()]

        # Also get staged
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=str(root), timeout=5
        )
        staged = [f for f in result.stdout.strip().split("\n") if f.strip()]
        state["changed_files"] = list(set(changed + staged))

        # Untracked
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, cwd=str(root), timeout=5
        )
        state["untracked_files"] = [
            f for f in result.stdout.strip().split("\n") if f.strip()
        ][:20]  # Cap at 20

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return state


def get_project_metrics(project_path: str) -> dict:
    """Count files, tests, lines, endpoints."""
    all_files = walk_project_files(project_path, CODE_EXTENSIONS)
    test_files = [f for f in all_files if is_test_file(f, Path(project_path).resolve())]

    total_lines = 0
    for f in all_files:
        try:
            total_lines += len(f.read_text(errors="ignore").split("\n"))
        except OSError:
            pass

    # Count endpoints
    endpoint_count = 0
    route_patterns = [
        "@app.", "@router.", "app.get(", "app.post(", "app.put(", "app.delete(",
        "router.get(", "router.post(", "router.put(", "router.delete(",
    ]
    for f in walk_project_files(project_path, {".py", ".js", ".ts"}):
        if is_test_file(f, Path(project_path).resolve()):
            continue
        try:
            content = f.read_text(errors="ignore")
            for p in route_patterns:
                endpoint_count += content.count(p)
        except OSError:
            pass

    # File type breakdown
    by_ext = {}
    for f in all_files:
        by_ext[f.suffix] = by_ext.get(f.suffix, 0) + 1

    return {
        "file_count": len(all_files),
        "test_file_count": len(test_files),
        "total_lines": total_lines,
        "endpoint_count": endpoint_count,
        "file_types": dict(sorted(by_ext.items(), key=lambda x: x[1], reverse=True)[:10]),
    }


def generate_handoff_prompt(
    project_path: str,
    git_state: dict,
    metrics: dict,
    health_report,
    baseline_changes: list,
    debt_summary: dict,
    prd_content: str = "",
) -> str:
    """Generate the structured prompt for the next AI coding session."""

    lines = []
    lines.append("# SESSION HANDOFF — Paste this into your next AI coding session")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")

    # Section 1: Project State
    lines.append("## PROJECT STATE")
    lines.append(f"- Files: {metrics['file_count']} | Tests: {metrics['test_file_count']} | Lines: {metrics['total_lines']:,} | Endpoints: {metrics['endpoint_count']}")
    lines.append(f"- Health: **{health_report.grade}** ({health_report.score}/100) — {health_report.summary}")
    if git_state["has_git"]:
        lines.append(f"- Branch: `{git_state['branch']}`")
    lines.append("")

    # Section 2: What Changed (git)
    if git_state["has_git"] and git_state["last_commits"]:
        lines.append("## RECENT CHANGES")
        for commit in git_state["last_commits"][:5]:
            lines.append(f"- {commit}")
        if git_state["changed_files"]:
            lines.append(f"- Modified files: {', '.join(git_state['changed_files'][:10])}")
        lines.append("")

    # Section 3: Baseline Comparison
    if baseline_changes:
        lines.append("## SINCE LAST SESSION")
        for change in baseline_changes:
            arrow = "+" if change["delta"] > 0 else ""
            flag = " [REGRESSION]" if change["is_regression"] else ""
            lines.append(f"- {change['metric']}: {change['previous']} -> {change['current']} ({arrow}{change['delta']}){flag}")
        lines.append("")

    # Section 4: Quality Gate Results
    lines.append("## QUALITY GATES")
    lines.append(f"- Total issues: {health_report.total_issues}")
    if health_report.critical_count:
        lines.append(f"- CRITICAL: {health_report.critical_count} (must fix)")
    if health_report.high_count:
        lines.append(f"- HIGH: {health_report.high_count} (should fix)")
    if health_report.medium_count:
        lines.append(f"- MEDIUM: {health_report.medium_count}")
    if health_report.low_count:
        lines.append(f"- LOW: {health_report.low_count}")
    if health_report.top_issues:
        lines.append("")
        lines.append("### Top Issues to Fix")
        for issue in health_report.top_issues[:5]:
            loc = f"{issue.file}"
            if issue.line:
                loc += f":{issue.line}"
            lines.append(f"- [{issue.severity.upper()}] {issue.rule_id}: {issue.message} ({loc})")
    lines.append("")

    # Section 5: Technical Debt
    if debt_summary.get("recurring_issues"):
        lines.append("## RECURRING DEBT")
        for item in debt_summary["recurring_issues"][:5]:
            lines.append(f"- {item['rule_id']} in {item['file']}: seen {item['count']} times — {item['message']}")
        if debt_summary.get("trend"):
            lines.append(f"- Trend: {debt_summary['trend']}")
        lines.append("")

    # Section 6: PRD Context
    if prd_content:
        lines.append("## PROJECT CONTEXT (from .crystal/prd.md)")
        # Truncate if too long
        if len(prd_content) > 2000:
            prd_content = prd_content[:2000] + "\n... (truncated)"
        lines.append(prd_content)
        lines.append("")

    # Section 7: Instructions for the AI
    lines.append("## INSTRUCTIONS FOR THIS SESSION")
    lines.append("1. Read the project state and quality gate results above before making any changes.")
    lines.append("2. Do NOT rewrite files that are already working. Only modify what's needed.")
    if health_report.critical_count > 0:
        lines.append(f"3. PRIORITY: Fix the {health_report.critical_count} critical issue(s) listed above before adding new features.")
    else:
        lines.append("3. Continue building from where the last session left off.")
    lines.append("4. After making changes, verify existing functionality still works (no regressions).")
    lines.append("5. Update .crystal/prd.md with what was built/changed in this session.")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by Crystal Guard v0.1.0 — https://github.com/crystalguard/crystal-guard*")

    return "\n".join(lines)


def save_session(project_path: str, handoff_content: str, metrics: dict, health_score: int):
    """Save session record."""
    crystal_dir = get_crystal_dir(project_path)
    crystal_dir.mkdir(parents=True, exist_ok=True)

    sessions_path = crystal_dir / "sessions.json"
    sessions = []
    if sessions_path.exists():
        try:
            with open(sessions_path) as f:
                sessions = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    sessions.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "health_score": health_score,
        "file_count": metrics["file_count"],
        "test_file_count": metrics["test_file_count"],
        "endpoint_count": metrics["endpoint_count"],
    })

    # Keep last 50 sessions
    sessions = sessions[-50:]

    with open(sessions_path, "w") as f:
        json.dump(sessions, f, indent=2)
