"""Markdown reporter for PR comments and reports."""



def generate_markdown_report(health_report, issues: list, config=None) -> str:
    lines = []
    lines.append("# Crystal Guard Health Report")
    lines.append("")

    project = config.project_name if config else "Project"
    stack = config.stack if config else "generic"
    lines.append(f"**Project**: {project} | **Stack**: {stack} | **Grade**: {health_report.grade} ({health_report.score}/100)")
    lines.append("")

    if health_report.passed:
        lines.append("> All quality gates passed.")
    else:
        lines.append("> Quality gates **FAILED**. Fix issues before merging.")
    lines.append("")

    # Group by severity
    by_sev = {"critical": [], "high": [], "medium": [], "low": []}
    for issue in issues:
        by_sev.get(issue.severity, []).append(issue)

    for sev in ["critical", "high", "medium", "low"]:
        group = by_sev[sev]
        if group:
            lines.append(f"## {sev.upper()} Issues ({len(group)})")
            lines.append("")
            for issue in group:
                loc = issue.file
                if issue.line:
                    loc += f":{issue.line}"
                lines.append(f"- **[{issue.rule_id}]** {issue.message}")
                lines.append(f"  - File: `{loc}`")
                lines.append(f"  - Fix: {issue.suggestion}")
            lines.append("")

    lines.append("---")
    lines.append(f"*Crystal Guard v0.1.0 | {health_report.summary}*")

    return "\n".join(lines)
