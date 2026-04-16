"""Crystal MCP Server — Exposes Crystal tools to AI assistants via MCP protocol.

Usage:
  crystal mcp serve                    # stdio transport (for Cursor, Claude Desktop)
  crystal mcp serve --transport http   # HTTP transport (for web platforms)

AI assistants can call these tools while coding to check architecture,
validate files, get project context, and run quality gates in real-time.
"""

import os
import json
from pathlib import Path
from fastmcp import FastMCP

from crystal_guard.config import load_config, get_crystal_dir, walk_project_files, CODE_EXTENSIONS, is_test_file
from crystal_guard.detector import detect_stack
from crystal_guard.analyzers import architecture, domain, security, placeholders
from crystal_guard.scoring import calculate_health
from crystal_guard.rules.loader import load_rules
from crystal_guard.baseline import load_baselines
from crystal_guard.debt import get_debt_summary
from crystal_guard.handoff import get_git_state, get_project_metrics
from crystal_guard.architect import generate_architecture_md


def get_project_path() -> str:
    """Get the project path from env var or current directory."""
    return os.environ.get("CRYSTAL_PROJECT_PATH", os.getcwd())


mcp = FastMCP(
    "Crystal",
    instructions=(
        "Crystal is your AI coding buddy that protects architecture integrity "
        "and domain purity. Use these tools to check code quality, validate "
        "file placement, and get project context before making changes."
    ),
)


@mcp.tool()
def check_architecture(project_path: str = "") -> str:
    """Run architecture checks on the project.

    Validates file structure, required files, directory depth, and test coverage.
    Returns issues found with plain-English suggestions for fixing them.
    """
    path = project_path or get_project_path()
    config = load_config(path)
    rules = load_rules(path, config.stack)
    issues = architecture.analyze(path, rules)

    if not issues:
        return "Architecture checks passed. No issues found."

    result = f"Found {len(issues)} architecture issues:\n\n"
    for issue in issues:
        result += f"- [{issue.severity.upper()}] {issue.message}\n"
        result += f"  Fix: {issue.suggestion}\n\n"
    return result


@mcp.tool()
def check_domain_purity(project_path: str = "") -> str:
    """Check if files respect domain boundaries.

    Ensures frontend files don't contain database queries,
    backend routes don't contain business logic, etc.
    """
    path = project_path or get_project_path()
    config = load_config(path)
    rules = load_rules(path, config.stack)
    issues = domain.analyze(path, rules)

    if not issues:
        return "Domain purity checks passed. All files respect their boundaries."

    result = f"Found {len(issues)} domain violations:\n\n"
    for issue in issues:
        loc = issue.file
        if issue.line:
            loc += f":{issue.line}"
        result += f"- [{issue.severity.upper()}] {loc}: {issue.message}\n"
        result += f"  Fix: {issue.suggestion}\n\n"
    return result


@mcp.tool()
def check_security(project_path: str = "") -> str:
    """Scan for security issues in the project.

    Detects hardcoded API keys, passwords, exposed .env files,
    CORS wildcards, and SQL injection patterns.
    """
    path = project_path or get_project_path()
    config = load_config(path)
    rules = load_rules(path, config.stack)
    issues = security.analyze(path, rules)

    if not issues:
        return "Security scan passed. No hardcoded secrets or vulnerabilities found."

    result = f"Found {len(issues)} security issues:\n\n"
    for issue in issues:
        loc = issue.file
        if issue.line:
            loc += f":{issue.line}"
        result += f"- [{issue.severity.upper()}] {loc}: {issue.message}\n"
        result += f"  Fix: {issue.suggestion}\n\n"
    return result


@mcp.tool()
def run_all_checks(project_path: str = "") -> str:
    """Run all 15 quality gates and return the health report.

    This is the equivalent of running 'crystal check' from the command line.
    Returns health score (A-F), gate results, and top issues to fix.
    """
    path = project_path or get_project_path()
    config = load_config(path)
    rules = load_rules(path, config.stack)

    all_issues = []
    all_issues.extend(architecture.analyze(path, rules))
    all_issues.extend(domain.analyze(path, rules))
    all_issues.extend(security.analyze(path, rules))
    all_issues.extend(placeholders.analyze(path, rules))

    ignored = set(config.ignore_rules)
    all_issues = [i for i in all_issues if i.rule_id not in ignored]

    health = calculate_health(all_issues, config.severity_threshold)

    result = f"Health: {health.grade} ({health.score}/100)\n"
    result += f"{health.summary}\n\n"
    result += f"Issues: {health.critical_count} critical, {health.high_count} high, "
    result += f"{health.medium_count} medium, {health.low_count} low\n\n"

    if health.top_issues:
        result += "Top issues to fix:\n"
        for issue in health.top_issues[:5]:
            loc = issue.file
            if issue.line:
                loc += f":{issue.line}"
            result += f"- [{issue.severity.upper()}] {issue.rule_id}: {issue.message} ({loc})\n"

    return result


@mcp.tool()
def validate_file_placement(file_path: str, purpose: str, project_path: str = "") -> str:
    """Before creating a new file, check if it's being placed in the right directory.

    Args:
        file_path: Where the file will be created (e.g., 'frontend/src/utils/db.js')
        purpose: What the file does (e.g., 'database helper functions')
        project_path: Project root (optional, uses current directory)
    """
    path = project_path or get_project_path()
    config = load_config(path)

    file_lower = file_path.lower()
    purpose_lower = purpose.lower()
    warnings = []

    # Check if database code is going to frontend
    if ("frontend" in file_lower or "src/" in file_lower) and not "backend" in file_lower:
        db_words = ["database", "mongo", "sql", "query", "collection", "model", "schema"]
        if any(w in purpose_lower for w in db_words):
            warnings.append(
                f"'{file_path}' looks like it's in the frontend, but its purpose involves database operations. "
                f"Database code should go in the backend (e.g., backend/services/ or backend/models/)."
            )

    # Check if frontend code is going to backend
    if "backend" in file_lower:
        ui_words = ["component", "react", "vue", "page", "layout", "css", "style", "ui"]
        if any(w in purpose_lower for w in ui_words):
            warnings.append(
                f"'{file_path}' is in the backend, but its purpose involves UI/frontend code. "
                f"Frontend code should go in frontend/src/."
            )

    if warnings:
        return "WARNING:\n" + "\n".join(warnings)

    return f"File placement looks correct. '{file_path}' is appropriate for: {purpose}"


@mcp.tool()
def get_project_context(project_path: str = "") -> str:
    """Get the current project state for context.

    Returns: stack info, file counts, health score, what was built (from PRD),
    and recent git changes. Use this at the start of a coding session.
    """
    path = project_path or get_project_path()
    config = load_config(path)
    detected = detect_stack(path)
    metrics = get_project_metrics(path)
    git_state = get_git_state(path)
    baselines = load_baselines(path)
    debt = get_debt_summary(path)

    result = f"Project: {config.project_name or Path(path).name}\n"
    result += f"Stack: {detected['stack_id']}\n"
    result += f"Files: {metrics['file_count']} | Tests: {metrics['test_file_count']} | "
    result += f"Lines: {metrics['total_lines']:,} | Endpoints: {metrics['endpoint_count']}\n\n"

    if baselines:
        latest = baselines[-1]
        result += f"Last health check: {latest.get('grade', '?')} ({latest.get('health_score', '?')}/100)\n"
        result += f"Violations: {latest.get('violation_count', 0)}\n"

    if debt.get("trend") != "no data":
        result += f"Debt trend: {debt['trend']}\n"

    if git_state["has_git"]:
        result += f"\nBranch: {git_state['branch']}\n"
        if git_state["last_commits"]:
            result += "Recent commits:\n"
            for c in git_state["last_commits"][:3]:
                result += f"  - {c}\n"

    # PRD content
    prd_path = get_crystal_dir(path) / "prd.md"
    if prd_path.exists():
        prd = prd_path.read_text()
        if len(prd) > 1500:
            prd = prd[:1500] + "\n... (truncated)"
        result += f"\n--- PRD ---\n{prd}"

    return result


@mcp.tool()
def get_health_score(project_path: str = "") -> str:
    """Get the project's current health score (A-F) with a quick summary."""
    path = project_path or get_project_path()
    config = load_config(path)
    rules = load_rules(path, config.stack)

    all_issues = []
    all_issues.extend(architecture.analyze(path, rules))
    all_issues.extend(domain.analyze(path, rules))
    all_issues.extend(security.analyze(path, rules))
    all_issues.extend(placeholders.analyze(path, rules))

    ignored = set(config.ignore_rules)
    all_issues = [i for i in all_issues if i.rule_id not in ignored]

    health = calculate_health(all_issues, config.severity_threshold)
    return f"{health.grade} ({health.score}/100) — {health.summary}"


@mcp.tool()
def update_prd(section: str, content: str, project_path: str = "") -> str:
    """Update the project requirements document after completing a feature.

    Args:
        section: Which section to update (e.g., 'What\\'s Been Built', 'Next Steps')
        content: What to add to that section
    """
    path = project_path or get_project_path()
    prd_path = get_crystal_dir(path) / "prd.md"

    if not prd_path.exists():
        prd_path.parent.mkdir(parents=True, exist_ok=True)
        prd_path.write_text(f"# {Path(path).name} — Crystal PRD\n\n## {section}\n{content}\n")
        return f"Created PRD with section '{section}'."

    current = prd_path.read_text()

    # Try to find and append to existing section
    section_header = f"## {section}"
    if section_header in current:
        parts = current.split(section_header, 1)
        # Find the next section or end of file
        rest = parts[1]
        next_section = rest.find("\n## ")
        if next_section > 0:
            before_next = rest[:next_section]
            after = rest[next_section:]
            updated = parts[0] + section_header + before_next.rstrip() + "\n" + content + "\n" + after
        else:
            updated = parts[0] + section_header + rest.rstrip() + "\n" + content + "\n"
    else:
        updated = current.rstrip() + f"\n\n{section_header}\n{content}\n"

    prd_path.write_text(updated)
    return f"Updated PRD section '{section}'."


@mcp.resource("crystal://health")
def resource_health() -> str:
    """Current health check results."""
    path = get_project_path()
    baselines = load_baselines(path)
    if baselines:
        return json.dumps(baselines[-1], indent=2)
    return "No health data. Run 'crystal check' first."


@mcp.resource("crystal://rules")
def resource_rules() -> str:
    """Architecture rules for this project."""
    path = get_project_path()
    return generate_architecture_md(path)


@mcp.resource("crystal://prd")
def resource_prd() -> str:
    """Project requirements document."""
    path = get_project_path()
    prd_path = get_crystal_dir(path) / "prd.md"
    if prd_path.exists():
        return prd_path.read_text()
    return "No PRD found. Run 'crystal init' first."


def run_server(transport: str = "stdio", port: int = 8080):
    """Run the Crystal MCP server."""
    if transport == "http":
        mcp.run(transport="sse", port=port)
    else:
        mcp.run(transport="stdio")
