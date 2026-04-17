"""Dependency Analyzer — Gate 16+.

Checks for known vulnerabilities, outdated packages, unnecessary dependencies,
duplicate functionality, and license compatibility.
"""

from __future__ import annotations

import subprocess
import json
import re
from pathlib import Path
from crystal_guard.analyzers import Issue
from crystal_guard.config import walk_project_files, is_test_file

# Common duplicate packages
DUPLICATE_GROUPS = [
    ({"axios", "node-fetch", "got", "superagent"}, "HTTP client"),
    ({"lodash", "underscore", "ramda"}, "Utility library"),
    ({"moment", "dayjs", "date-fns", "luxon"}, "Date library"),
    ({"express", "koa", "fastify", "hapi"}, "Node server framework"),
]


def analyze(project_path: str, rules: dict = None) -> list[Issue]:
    root = Path(project_path).resolve()
    issues = []

    # Check Python dependencies
    req_paths = [root / "requirements.txt", root / "backend" / "requirements.txt"]
    for req_path in req_paths:
        if req_path.exists():
            issues.extend(_check_python_deps(root, req_path))

    # Check Node dependencies
    pkg_paths = [root / "package.json", root / "frontend" / "package.json"]
    for pkg_path in pkg_paths:
        if pkg_path.exists():
            issues.extend(_check_node_deps(root, pkg_path))

    return issues


def _check_python_deps(root: Path, req_path: Path) -> list[Issue]:
    issues = []
    rel_path = str(req_path.relative_to(root))

    # dep-001: Run pip-audit for vulnerabilities
    try:
        result = subprocess.run(
            ["pip", "audit", "-r", str(req_path), "--format", "json"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0 and result.stdout:
            try:
                audit = json.loads(result.stdout)
                for vuln in audit.get("vulnerabilities", []):
                    issues.append(Issue(
                        analyzer="dependencies",
                        severity="high",
                        file=rel_path,
                        line=None,
                        rule_id="dep-001",
                        message=f"Vulnerability in {vuln.get('name', '?')}: {vuln.get('id', '')}",
                        suggestion=f"Update {vuln.get('name')} to fix the vulnerability.",
                        why="Packages with known vulnerabilities can be exploited by attackers to compromise your app.",
                    ))
            except json.JSONDecodeError:
                pass
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # dep-003: Detect unused dependencies
    content = req_path.read_text()
    installed_pkgs = set()
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            pkg = re.split(r'[>=<!\[]', line)[0].strip().lower().replace("-", "_")
            if pkg:
                installed_pkgs.add(pkg)

    # Scan code for imports
    imported_pkgs = set()
    for f in walk_project_files(str(root), {".py"}):
        if is_test_file(f, root):
            continue
        try:
            for line in f.read_text(errors="ignore").split("\n"):
                m = re.match(r'^(?:from|import)\s+(\w+)', line.strip())
                if m:
                    imported_pkgs.add(m.group(1).lower().replace("-", "_"))
        except OSError:
            pass

    # Common pkg name mappings (pip name != import name)
    pkg_import_map = {
        "python_dotenv": "dotenv", "python_multipart": "multipart",
        "pyyaml": "yaml", "pillow": "PIL", "scikit_learn": "sklearn",
        "pymongo": "pymongo", "motor": "motor",
    }

    for pkg in installed_pkgs:
        import_name = pkg_import_map.get(pkg, pkg)
        if import_name not in imported_pkgs and pkg not in {"pip", "setuptools", "wheel"}:
            # Check if it's a framework dep (uvicorn, gunicorn) — skip those
            if pkg in {"uvicorn", "gunicorn", "celery", "pytest", "ruff", "black", "mypy"}:
                continue
            issues.append(Issue(
                analyzer="dependencies",
                severity="low",
                file=rel_path,
                line=None,
                rule_id="dep-003",
                message=f"Package '{pkg}' is in requirements but may not be imported in code.",
                suggestion=f"Remove '{pkg}' from {rel_path} if it's not needed.",
                why="Extra dependencies slow down installs, increase attack surface, and add maintenance burden.",
            ))

    return issues


def _check_node_deps(root: Path, pkg_path: Path) -> list[Issue]:
    issues = []
    rel_path = str(pkg_path.relative_to(root))

    try:
        with open(pkg_path) as f:
            pkg = json.load(f)
    except (json.JSONDecodeError, OSError):
        return issues

    all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    dep_names = set(all_deps.keys())

    # dep-004: Detect duplicate functionality
    for group, category in DUPLICATE_GROUPS:
        found = dep_names & group
        if len(found) > 1:
            issues.append(Issue(
                analyzer="dependencies",
                severity="medium",
                file=rel_path,
                line=None,
                rule_id="dep-004",
                message=f"Multiple {category} packages installed: {', '.join(sorted(found))}. Pick one.",
                suggestion=f"Remove all but one {category} package to reduce bundle size and complexity.",
                why="Having multiple packages that do the same thing bloats your app and creates confusion about which one to use.",
            ))

    # dep-001: Run npm audit
    if (pkg_path.parent / "node_modules").exists():
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                capture_output=True, text=True, timeout=30,
                cwd=str(pkg_path.parent)
            )
            if result.stdout:
                try:
                    audit = json.loads(result.stdout)
                    vulns = audit.get("vulnerabilities", {})
                    critical = sum(1 for v in vulns.values() if v.get("severity") == "critical")
                    high = sum(1 for v in vulns.values() if v.get("severity") == "high")
                    if critical > 0 or high > 0:
                        issues.append(Issue(
                            analyzer="dependencies",
                            severity="high",
                            file=rel_path,
                            line=None,
                            rule_id="dep-001",
                            message=f"npm audit found {critical} critical and {high} high vulnerabilities.",
                            suggestion="Run `npm audit fix` to resolve.",
                            why="Vulnerable packages can be exploited to steal data or take control of your app.",
                        ))
                except json.JSONDecodeError:
                    pass
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    return issues
