"""Security Analyzer — Gates 8-11.

Gate 8:  Hardcoded API keys and secrets
Gate 9:  Hardcoded passwords
Gate 10: Known API key formats (sk-, pk_, ghp_, AKIA)
Gate 11: Exposed .env (not in .gitignore), CORS wildcard
"""

import re
from pathlib import Path
from crystal_guard.analyzers import Issue
from crystal_guard.config import is_ignored, is_test_file, CODE_EXTENSIONS


# Built-in security patterns (used when no rules YAML is loaded)
BUILTIN_CHECKS = [
    {
        "id": "sec-001",
        "pattern": r'(api_key|apiKey|API_KEY|api_secret|apiSecret)\s*[=:]\s*["\'][a-zA-Z0-9_\-]{16,}',
        "message": "Hardcoded API key detected. API keys should be in environment variables, never in code.",
        "suggestion": "Move this key to your .env file and reference it with os.environ.get('YOUR_KEY_NAME').",
        "severity": "critical",
    },
    {
        "id": "sec-002",
        "pattern": r'(password|passwd|pwd|secret)\s*[=:]\s*["\'][^"\']{4,}',
        "message": "Hardcoded password detected. Passwords should never appear in code.",
        "suggestion": "Use environment variables for secrets. For user passwords, use bcrypt hashing.",
        "severity": "critical",
    },
    {
        "id": "sec-003",
        "pattern": r'sk-[a-zA-Z0-9]{20,}|pk_(test|live)_[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[0-9A-Z]{16}|sk-ant-[a-zA-Z0-9]{20,}|hf_[a-zA-Z0-9]{20,}|Bearer\s+[a-zA-Z0-9\-._~+/]{20,}',
        "message": "Recognized API key format found in code. This is a significant security risk.",
        "suggestion": "Remove this key immediately, rotate it, and store in .env file.",
        "severity": "critical",
    },
    {
        "id": "sec-005",
        "pattern": r'allow_origins\s*=\s*\[\s*["\']?\*["\']?|cors\(.*origin.*["\']?\*["\']?',
        "message": "CORS is set to allow all origins (*). This allows any website to make requests to your API.",
        "suggestion": "Set specific allowed origins instead of wildcard.",
        "severity": "high",
    },
    {
        "id": "sec-006",
        "pattern": r'f["\'].*SELECT.*\{|["\'].*SELECT.*["\']?\s*\+\s*',
        "message": "Potential SQL injection vulnerability. User input may be directly inserted into SQL query.",
        "suggestion": "Use parameterized queries or an ORM instead of string formatting for SQL.",
        "severity": "high",
    },
]


def analyze(project_path: str, rules: dict) -> list[Issue]:
    root = Path(project_path).resolve()
    issues = []

    # Get checks from rules or use built-in
    sec_rules = rules.get("security", {}).get("global", {})
    checks = sec_rules.get("checks", BUILTIN_CHECKS)

    # Gate 11a: Check .env in .gitignore
    gitignore_path = root / ".gitignore"
    env_path = root / ".env"
    if env_path.exists():
        env_in_gitignore = False
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            env_in_gitignore = ".env" in content.split("\n") or "*.env" in content
        if not env_in_gitignore:
            issues.append(Issue(
                analyzer="security",
                severity="critical",
                file=".env",
                line=None,
                rule_id="sec-004",
                message=".env file is not in .gitignore. Your secrets will be committed to git.",
                suggestion="Add '.env' to your .gitignore file immediately.",
            ))

    # Scan all code files for pattern matches (Gates 8-10, 11b)
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        if is_ignored(file_path, root):
            continue
        if file_path.suffix not in CODE_EXTENSIONS:
            continue
        if is_test_file(file_path, root) or ".example" in file_path.name:
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

            exclude_files = check.get("exclude_files", [])
            skip = False
            for exc in exclude_files:
                exc_clean = exc.replace("*", "")
                if exc_clean in file_path.name:
                    skip = True
                    break
            if skip:
                continue

            for line_num, line_text in enumerate(lines, 1):
                stripped = line_text.strip()
                if stripped.startswith("//") or stripped.startswith("#"):
                    continue
                try:
                    if re.search(pattern, line_text):
                        issues.append(Issue(
                            analyzer="security",
                            severity=check.get("severity", "high"),
                            file=str(file_path.relative_to(root)),
                            line=line_num,
                            rule_id=check["id"],
                            message=check["message"],
                            suggestion=check.get("suggestion", "Review this line for security issues."),
                        ))
                        break  # One match per check per file
                except re.error:
                    pass

    return issues
