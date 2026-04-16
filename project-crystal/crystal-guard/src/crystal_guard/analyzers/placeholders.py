"""Placeholder / Code Hygiene Analyzer — Gates 12-15.

Gate 12: Unresolved TODO/FIXME/HACK comments
Gate 13: Placeholder values (example.com, lorem ipsum)
Gate 14: Debug statements (console.log, print)
Gate 15: Hardcoded localhost URLs in non-dev files
"""

import re
from pathlib import Path
from crystal_guard.analyzers import Issue
from crystal_guard.config import is_ignored, is_test_file, CODE_EXTENSIONS


BUILTIN_CHECKS = [
    {
        "id": "hyg-001",
        "pattern": r"\bTODO\b|\bFIXME\b|\bHACK\b|\bXXX\b",
        "message": "Unresolved TODO/FIXME comment found. Complete or remove before deploying.",
        "severity": "low",
        "exclude_extensions": {".md"},
    },
    {
        "id": "hyg-002",
        "pattern": r"example\.com|test@test\.com|lorem ipsum|placeholder",
        "message": "Placeholder value detected. Replace with real values before deploying.",
        "severity": "medium",
        "exclude_extensions": {".md", ".test.js", ".spec.js"},
    },
    {
        "id": "hyg-003",
        "pattern": r"console\.log\(|(?<!\w)print\(",
        "message": "Debug logging statement found. Remove or replace with proper logging before deploying.",
        "severity": "low",
        "exclude_extensions": set(),
    },
    {
        "id": "hyg-004",
        "pattern": r"localhost:\d{4}",
        "message": "Hardcoded localhost URL found. Use environment variables for URLs.",
        "severity": "medium",
        "exclude_extensions": {".env", ".md"},
    },
]


def analyze(project_path: str, rules: dict) -> list[Issue]:
    root = Path(project_path).resolve()
    issues = []

    placeholder_rules = rules.get("placeholders", {}).get("global", {})
    checks = placeholder_rules.get("checks", None)

    if checks is None:
        checks = BUILTIN_CHECKS

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        if is_ignored(file_path, root):
            continue
        if file_path.suffix not in CODE_EXTENSIONS:
            continue
        if is_test_file(file_path, root):
            continue

        try:
            content = file_path.read_text(errors="ignore")
            lines = content.split("\n")
        except OSError:
            continue

        for check in checks:
            pattern = check.get("pattern")
            if not pattern:
                continue

            exclude_ext = check.get("exclude_extensions", set())
            if isinstance(exclude_ext, list):
                exclude_ext = set(exclude_ext)
            if file_path.suffix in exclude_ext:
                continue

            # Handle YAML-style exclude_files
            exclude_files = check.get("exclude_files", [])
            skip = False
            for exc in exclude_files:
                exc_clean = exc.replace("*", "")
                if exc_clean and (exc_clean in file_path.name or exc_clean in str(file_path)):
                    skip = True
                    break
            if skip:
                continue

            matches_in_file = 0
            for line_num, line_text in enumerate(lines, 1):
                try:
                    if re.search(pattern, line_text, re.IGNORECASE if check["id"] == "hyg-002" else 0):
                        matches_in_file += 1
                        if matches_in_file <= 3:  # Cap at 3 per file per check
                            issues.append(Issue(
                                analyzer="placeholders",
                                severity=check.get("severity", "low"),
                                file=str(file_path.relative_to(root)),
                                line=line_num,
                                rule_id=check["id"],
                                message=check["message"],
                                suggestion=check.get("suggestion", "Review and fix this before deploying."),
                            ))
                except re.error:
                    pass

    return issues
