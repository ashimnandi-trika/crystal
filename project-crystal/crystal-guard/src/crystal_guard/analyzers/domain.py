"""Domain Purity Analyzer — Gates 5-7.

Gate 5: Frontend files don't contain backend patterns
Gate 6: Backend routes don't contain raw DB queries
Gate 7: No cross-layer violations (env vars, crypto in frontend)
"""

import re
from pathlib import Path
from crystal_guard.analyzers import Issue
from crystal_guard.config import is_ignored, is_test_file


def analyze(project_path: str, rules: dict) -> list[Issue]:
    root = Path(project_path).resolve()
    issues = []
    domain_rules = rules.get("domain_purity", {})

    for section_key, section_rules in domain_rules.items():
        file_patterns = section_rules.get("file_patterns", [])
        forbidden = section_rules.get("forbidden", [])

        # Collect matching files
        matched_files = []
        for pattern in file_patterns:
            matched_files.extend(root.glob(pattern))

        for file_path in matched_files:
            if is_ignored(file_path, root) or is_test_file(file_path, root):
                continue
            if not file_path.is_file():
                continue

            try:
                content = file_path.read_text(errors="ignore")
                lines = content.split("\n")
            except OSError:
                continue

            for rule in forbidden:
                pattern = rule.get("pattern")
                if not pattern:
                    continue

                for line_num, line_text in enumerate(lines, 1):
                    stripped = line_text.strip()
                    # Skip comments
                    if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("*"):
                        continue
                    try:
                        if re.search(pattern, line_text):
                            issues.append(Issue(
                                analyzer="domain",
                                severity=rule.get("severity", "medium"),
                                file=str(file_path.relative_to(root)),
                                line=line_num,
                                rule_id=rule["id"],
                                message=rule["message"],
                                suggestion=rule.get("suggestion", "Review this code for domain boundary violations."),
                            ))
                            break  # One match per rule per file is enough
                    except re.error:
                        pass

    return issues
