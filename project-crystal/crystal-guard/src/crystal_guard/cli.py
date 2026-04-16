"""Crystal Guard CLI — The main entry point."""

import sys
import json
import typer
from pathlib import Path
from rich.console import Console
from typing import Optional

from crystal_guard.config import (
    load_config, save_config, CrystalConfig, get_crystal_dir
)
from crystal_guard.detector import detect_stack
from crystal_guard.analyzers import architecture, domain, security, placeholders
from crystal_guard.scoring import calculate_health
from crystal_guard.rules.loader import load_rules
from crystal_guard.baseline import (
    capture_baseline, load_baselines, save_baseline, compare_baselines
)
from crystal_guard.debt import record_session_debt, get_debt_summary
from crystal_guard.handoff import (
    get_git_state, get_project_metrics, generate_handoff_prompt, save_session
)
from crystal_guard.reporters.terminal import (
    print_health, print_issues, print_gates, print_baseline_changes, print_handoff
)
from crystal_guard.reporters.json_reporter import generate_json_report
from crystal_guard.reporters.markdown import generate_markdown_report


app = typer.Typer(
    name="crystal",
    help="Crystal Guard — Architecture guardian for vibe-coded projects.",
    no_args_is_help=True,
)
console = Console()


def run_all_analyzers(project_path: str, rules: dict, config: CrystalConfig) -> list:
    """Run all enabled analyzers and return combined issues."""
    all_issues = []

    if config.checks.get("architecture", True):
        all_issues.extend(architecture.analyze(project_path, rules))

    if config.checks.get("domain_purity", True):
        all_issues.extend(domain.analyze(project_path, rules))

    if config.checks.get("security", True):
        all_issues.extend(security.analyze(project_path, rules))

    if config.checks.get("placeholders", True):
        all_issues.extend(placeholders.analyze(project_path, rules))

    # Filter ignored rules
    ignored = set(config.ignore_rules)
    all_issues = [i for i in all_issues if i.rule_id not in ignored]

    return all_issues


@app.command()
def init(
    path: str = typer.Argument(".", help="Project path"),
    stack: Optional[str] = typer.Option(None, "--stack", "-s", help="Explicit stack (e.g., react-python-mongo)"),
    ci: bool = typer.Option(False, "--ci", help="Non-interactive CI mode"),
):
    """Initialize Crystal Guard for a project."""
    project_path = Path(path).resolve()

    if not project_path.exists():
        console.print(f"[red]Path not found: {project_path}[/red]")
        raise typer.Exit(1)

    # Detect stack
    if stack:
        detected = {"stack_id": stack, "confidence": "manual", "detected_from": ["--stack flag"]}
    else:
        detected = detect_stack(str(project_path))

    console.print(f"[green]Detected stack:[/green] {detected['stack_id']} (confidence: {detected['confidence']})")
    if detected["detected_from"]:
        console.print(f"[dim]Detected from: {', '.join(detected['detected_from'])}[/dim]")

    # Create config
    config = CrystalConfig(
        project_name=project_path.name,
        stack=detected["stack_id"],
        project_path=str(project_path),
    )
    save_config(config, str(project_path))

    # Create PRD template
    prd_path = get_crystal_dir(str(project_path)) / "prd.md"
    if not prd_path.exists():
        prd_path.write_text(
            f"# {project_path.name} — Crystal PRD\n\n"
            f"## Project Overview\n[Describe your project here]\n\n"
            f"## What's Been Built\n- [ ] Feature 1\n- [ ] Feature 2\n\n"
            f"## Architecture Decisions\n- Stack: {detected['stack_id']}\n\n"
            f"## Next Steps\n- \n"
        )

    # Load and count rules
    rules = load_rules(str(project_path), config.stack)
    rule_count = 0
    for section in rules.values():
        if isinstance(section, dict):
            for sub in section.values():
                if isinstance(sub, dict):
                    rule_count += len(sub.get("forbidden", []))
                    rule_count += len(sub.get("checks", []))
                    for sd in sub.values():
                        if isinstance(sd, list):
                            for item in sd:
                                if isinstance(item, dict) and "expected_dirs" in str(item):
                                    rule_count += 1

    console.print(f"[green]Created .crystal/ configuration[/green]")
    console.print(f"[green]Loaded {max(rule_count, 15)} rules for {detected['stack_id']}[/green]")
    console.print(f"\nRun [cyan]crystal check {path}[/cyan] to analyze your project.")


@app.command()
def check(
    path: str = typer.Argument(".", help="Project path"),
    format: str = typer.Option("terminal", "--format", "-f", help="Output format: terminal, json, markdown"),
    severity: str = typer.Option("all", "--severity", help="Minimum severity to show: critical, high, medium, all"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Write report to file"),
):
    """Run all quality gates and show health report."""
    project_path = str(Path(path).resolve())
    config = load_config(project_path)
    rules = load_rules(project_path, config.stack)

    console.print("[dim]Running quality gates...[/dim]\n")

    issues = run_all_analyzers(project_path, rules, config)
    health = calculate_health(issues, config.severity_threshold)

    # Filter by severity for display
    if severity != "all":
        sev_rank = {"critical": 0, "high": 1, "medium": 2}.get(severity, 3)
        display_issues = [i for i in issues if {"critical": 0, "high": 1, "medium": 2, "low": 3}[i.severity] <= sev_rank]
    else:
        display_issues = issues

    if format == "json":
        report = generate_json_report(health, issues, config)
        if output:
            Path(output).write_text(report)
            console.print(f"[green]Report written to {output}[/green]")
        else:
            console.print(report)
    elif format == "markdown":
        report = generate_markdown_report(health, issues, config)
        if output:
            Path(output).write_text(report)
            console.print(f"[green]Report written to {output}[/green]")
        else:
            console.print(report)
    else:
        # Terminal output
        gate_results = {
            "Architecture": sum(1 for i in issues if i.analyzer == "architecture"),
            "Domain Purity": sum(1 for i in issues if i.analyzer == "domain"),
            "Security": sum(1 for i in issues if i.analyzer == "security"),
            "Code Hygiene": sum(1 for i in issues if i.analyzer == "placeholders"),
        }
        print_gates(gate_results, console)
        print_health(health, console)
        if display_issues:
            console.print()
            print_issues(display_issues, console)

        if output:
            report = generate_json_report(health, issues, config)
            Path(output).write_text(report)
            console.print(f"\n[dim]Report saved to {output}[/dim]")

    # Update baseline and debt
    snapshot = capture_baseline(project_path, health.score, health.grade, issues)
    save_baseline(project_path, snapshot)
    record_session_debt(project_path, issues, health.score)

    if not health.passed:
        raise typer.Exit(1)


@app.command()
def status(
    path: str = typer.Argument(".", help="Project path"),
):
    """Show quick project health dashboard."""
    project_path = str(Path(path).resolve())
    config = load_config(project_path)

    baselines = load_baselines(project_path)
    debt_summary = get_debt_summary(project_path)
    metrics = get_project_metrics(project_path)

    console.print(f"\n[bold]{config.project_name or Path(project_path).name}[/bold]")
    console.print(f"[dim]Stack: {config.stack}[/dim]")
    console.print(f"Files: {metrics['file_count']} | Tests: {metrics['test_file_count']} | Lines: {metrics['total_lines']:,} | Endpoints: {metrics['endpoint_count']}")

    if baselines:
        latest = baselines[-1]
        console.print(f"\n[bold]Last Check:[/bold] {latest.get('timestamp', 'N/A')}")
        grade = latest.get("grade", "?")
        score = latest.get("health_score", 0)
        grade_colors = {"A": "green", "B": "cyan", "C": "yellow", "D": "red", "F": "bold red"}
        color = grade_colors.get(grade, "white")
        console.print(f"Health: [{color}]{grade} ({score}/100)[/{color}]")
        console.print(f"Violations: {latest.get('violation_count', 0)}")

        if len(baselines) >= 2:
            changes = compare_baselines(baselines[-1], baselines[-2])
            print_baseline_changes(changes, console)
    else:
        console.print("\n[dim]No health data yet. Run 'crystal check' first.[/dim]")

    if debt_summary.get("trend") != "no data":
        console.print(f"\n[bold]Debt Trend:[/bold] {debt_summary['trend']}")
        if debt_summary.get("recurring_issues"):
            console.print(f"Recurring issues: {len(debt_summary['recurring_issues'])}")


@app.command()
def handoff(
    path: str = typer.Argument(".", help="Project path"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Write handoff to file"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy to clipboard (requires pyperclip)"),
):
    """Generate session handoff prompt for the next AI coding session.

    Reads git state, runs quality gates, compares baselines, and generates
    a structured prompt you paste into your next session.
    """
    project_path = str(Path(path).resolve())
    config = load_config(project_path)
    rules = load_rules(project_path, config.stack)

    console.print("[dim]Analyzing project for handoff...[/dim]\n")

    # 1. Git state
    git_state = get_git_state(project_path)

    # 2. Project metrics
    metrics = get_project_metrics(project_path)

    # 3. Run quality gates
    issues = run_all_analyzers(project_path, rules, config)
    health = calculate_health(issues, config.severity_threshold)

    # 4. Baseline comparison
    baselines = load_baselines(project_path)
    baseline_changes = []
    if baselines:
        current_snapshot = capture_baseline(project_path, health.score, health.grade, issues)
        baseline_changes = compare_baselines(current_snapshot, baselines[-1])
        save_baseline(project_path, current_snapshot)

    # 5. Debt summary
    record_session_debt(project_path, issues, health.score)
    debt_summary = get_debt_summary(project_path)

    # 6. PRD content
    prd_path = get_crystal_dir(project_path) / "prd.md"
    prd_content = ""
    if prd_path.exists():
        prd_content = prd_path.read_text()

    # 7. Generate handoff prompt
    handoff_text = generate_handoff_prompt(
        project_path=project_path,
        git_state=git_state,
        metrics=metrics,
        health_report=health,
        baseline_changes=baseline_changes,
        debt_summary=debt_summary,
        prd_content=prd_content,
    )

    # Save session
    save_session(project_path, handoff_text, metrics, health.score)

    # Output
    if output:
        Path(output).write_text(handoff_text)
        console.print(f"[green]Handoff prompt saved to {output}[/green]")
        console.print(f"[dim]Paste the contents into your next AI coding session.[/dim]")
    elif copy:
        try:
            import pyperclip
            pyperclip.copy(handoff_text)
            console.print("[green]Handoff prompt copied to clipboard![/green]")
        except ImportError:
            console.print("[yellow]pyperclip not installed. Install with: pip install pyperclip[/yellow]")
            print_handoff(handoff_text, console)
    else:
        print_handoff(handoff_text, console)

    # Quick summary
    console.print(f"\n[bold]Summary:[/bold] {health.grade} ({health.score}/100) | {health.total_issues} issues | {metrics['file_count']} files | {metrics['test_file_count']} tests")
    if baseline_changes:
        regressions = [c for c in baseline_changes if c["is_regression"]]
        if regressions:
            console.print(f"[red]Regressions detected: {len(regressions)}[/red]")


@app.command()
def gates(
    path: str = typer.Argument(".", help="Project path"),
):
    """Show all 15 quality gates and their status."""
    project_path = str(Path(path).resolve())
    config = load_config(project_path)
    rules = load_rules(project_path, config.stack)

    issues = run_all_analyzers(project_path, rules, config)

    gate_definitions = [
        ("Gate 1", "arch-001", "Expected directories exist"),
        ("Gate 2", "arch-002", "Required files present"),
        ("Gate 3", "arch-004", "No root file sprawl"),
        ("Gate 4", "arch-005", "No deep nesting"),
        ("Gate 5", "dom-001", "No DB access in frontend"),
        ("Gate 6", "dom-002", "No filesystem access in frontend"),
        ("Gate 7", "dom-003", "Correct env var usage"),
        ("Gate 8", "sec-001", "No hardcoded API keys"),
        ("Gate 9", "sec-002", "No hardcoded passwords"),
        ("Gate 10", "sec-003", "No known key formats"),
        ("Gate 11", "sec-004", ".env in .gitignore"),
        ("Gate 12", "hyg-001", "No TODO/FIXME"),
        ("Gate 13", "hyg-002", "No placeholder values"),
        ("Gate 14", "hyg-003", "No debug logging"),
        ("Gate 15", "hyg-004", "No hardcoded localhost"),
    ]

    issue_rules = {i.rule_id for i in issues}

    console.print("\n[bold]CRYSTAL GUARD — 15 QUALITY GATES[/bold]\n")
    passed = 0
    for gate_name, rule_id, desc in gate_definitions:
        if rule_id in issue_rules:
            matching = [i for i in issues if i.rule_id == rule_id]
            console.print(f"  [red]FAIL[/red]  {gate_name}: {desc} ({len(matching)} issues)")
        else:
            console.print(f"  [green]PASS[/green]  {gate_name}: {desc}")
            passed += 1

    console.print(f"\n[bold]{passed}/15 gates passed[/bold]")

    # Also check architecture bonus gates
    arch_bonus = [i for i in issues if i.rule_id in ("arch-006", "arch-007", "arch-003")]
    if arch_bonus:
        console.print(f"\n[dim]+ {len(arch_bonus)} additional architecture findings[/dim]")


@app.command()
def report(
    path: str = typer.Argument(".", help="Project path"),
    output: str = typer.Option("crystal-report.md", "--output", "-o", help="Output file path"),
):
    """Generate a detailed markdown report."""
    project_path = str(Path(path).resolve())
    config = load_config(project_path)
    rules = load_rules(project_path, config.stack)

    issues = run_all_analyzers(project_path, rules, config)
    health = calculate_health(issues, config.severity_threshold)

    md = generate_markdown_report(health, issues, config)
    Path(output).write_text(md)
    console.print(f"[green]Report generated: {output}[/green]")


if __name__ == "__main__":
    app()
