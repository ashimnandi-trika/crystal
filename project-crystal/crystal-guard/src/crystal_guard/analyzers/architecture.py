"""Architecture Analyzer — Gates 1-4.

Gate 1: Expected directories exist
Gate 2: Required files present (.gitignore, README)
Gate 3: No excessive root files (config sprawl)
Gate 4: No deeply nested directories (>6 levels)
"""

from pathlib import Path
from crystal_guard.analyzers import Issue
from crystal_guard.config import IGNORE_DIRS


def analyze(project_path: str, rules: dict) -> list[Issue]:
    root = Path(project_path).resolve()
    issues = []

    arch_rules = rules.get("architecture", {})
    shared = arch_rules.get("shared", {})

    # Gate 1: Expected directories
    for section_key in ["frontend", "backend"]:
        section = arch_rules.get(section_key, {})
        section_root = section.get("root", "")
        for dir_spec in section.get("expected_dirs", []):
            dir_path = root / section_root / dir_spec["path"] if section_root else root / dir_spec["path"]
            if not dir_path.exists() and not dir_spec.get("optional", False):
                issues.append(Issue(
                    analyzer="architecture",
                    severity="medium",
                    file=str(Path(section_root) / dir_spec["path"]) if section_root else dir_spec["path"],
                    line=None,
                    rule_id="arch-001",
                    message=f"Expected directory '{dir_spec['path']}' not found. Purpose: {dir_spec.get('description', 'N/A')}.",
                    suggestion=f"Create the directory: mkdir -p {section_root}/{dir_spec['path']}" if section_root else f"Create the directory: mkdir -p {dir_spec['path']}",
                ))

    # Gate 2: Required and recommended files
    for req_file in shared.get("required_files", [".gitignore"]):
        if not (root / req_file).exists():
            issues.append(Issue(
                analyzer="architecture",
                severity="high",
                file=req_file,
                line=None,
                rule_id="arch-002",
                message=f"Required file '{req_file}' is missing.",
                suggestion=f"Create '{req_file}' in your project root.",
            ))

    for rec_file in shared.get("recommended_files", []):
        target = root / rec_file.rstrip("/")
        if not target.exists():
            issues.append(Issue(
                analyzer="architecture",
                severity="low",
                file=rec_file,
                line=None,
                rule_id="arch-003",
                message=f"Recommended file/directory '{rec_file}' is missing.",
                suggestion=f"Consider adding '{rec_file}' to improve project quality.",
            ))

    # Gate 3: Root file sprawl
    max_root = shared.get("max_root_files", 12)
    root_files = [f for f in root.iterdir() if f.is_file() and not f.name.startswith(".")]
    if len(root_files) > max_root:
        issues.append(Issue(
            analyzer="architecture",
            severity="medium",
            file="./",
            line=None,
            rule_id="arch-004",
            message=f"Too many files in project root ({len(root_files)} files, max {max_root}). This suggests configuration sprawl.",
            suggestion="Move configuration files into a config/ directory or consolidate them.",
        ))

    # Gate 4: Deep nesting
    max_depth = shared.get("max_depth", 6)
    for path in root.rglob("*"):
        if path.is_dir() and not any(p in IGNORE_DIRS for p in path.parts):
            try:
                depth = len(path.relative_to(root).parts)
                if depth > max_depth:
                    issues.append(Issue(
                        analyzer="architecture",
                        severity="low",
                        file=str(path.relative_to(root)),
                        line=None,
                        rule_id="arch-005",
                        message=f"Directory nested {depth} levels deep (max {max_depth}). Deep nesting makes code hard to navigate.",
                        suggestion="Flatten the directory structure or reorganize modules.",
                    ))
                    break  # One warning is enough
            except ValueError:
                pass

    # Bonus: Check .gitignore contains critical entries
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        critical_entries = [".env", "node_modules", "__pycache__"]
        for entry in critical_entries:
            if entry not in content:
                # Check if .env file actually exists
                if entry == ".env" and (root / ".env").exists():
                    issues.append(Issue(
                        analyzer="architecture",
                        severity="critical",
                        file=".gitignore",
                        line=None,
                        rule_id="arch-006",
                        message=f"'{entry}' is not listed in .gitignore but the file exists. Your secrets may be committed to git.",
                        suggestion=f"Add '{entry}' to your .gitignore file.",
                    ))

    # Check tests directory
    test_dirs = ["tests", "test", "__tests__", "spec"]
    has_tests = any((root / d).exists() for d in test_dirs)
    if not has_tests:
        # Also check for test files anywhere
        test_files = list(root.rglob("test_*.py")) + list(root.rglob("*.test.js")) + list(root.rglob("*.spec.js"))
        test_files = [f for f in test_files if not any(p in str(f) for p in IGNORE_DIRS)]
        if not test_files:
            issues.append(Issue(
                analyzer="architecture",
                severity="high",
                file="tests/",
                line=None,
                rule_id="arch-007",
                message="No test directory or test files found. Your project has no tests.",
                suggestion="Create a 'tests/' directory and add basic tests for critical functions.",
            ))

    return issues
