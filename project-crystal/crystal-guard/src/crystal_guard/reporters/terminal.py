"""Terminal reporter using Rich."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from crystal_guard.analyzers import Issue


SEVERITY_COLORS = {
    "critical": "bold red",
    "high": "red",
    "medium": "yellow",
    "low": "blue",
}

SEVERITY_ICONS = {
    "critical": "X",
    "high": "!",
    "medium": "~",
    "low": "-",
}


def print_health(health_report, console: Console = None):
    if console is None:
        console = Console()

    grade_colors = {"A": "green", "B": "cyan", "C": "yellow", "D": "red", "F": "bold red"}
    color = grade_colors.get(health_report.grade, "white")

    panel = Panel(
        f"[{color}]{health_report.grade}[/{color}] ({health_report.score}/100)\n\n"
        f"{health_report.summary}\n\n"
        f"[red]Critical: {health_report.critical_count}[/red]  "
        f"[yellow]High: {health_report.high_count}[/yellow]  "
        f"[blue]Medium: {health_report.medium_count}[/blue]  "
        f"[dim]Low: {health_report.low_count}[/dim]",
        title="[bold]CRYSTAL HEALTH SCORE[/bold]",
        border_style=color,
        padding=(1, 2),
    )
    console.print(panel)


def print_issues(issues: list[Issue], console: Console = None):
    if console is None:
        console = Console()

    if not issues:
        console.print("[green]No issues found![/green]")
        return

    table = Table(show_header=True, header_style="bold", border_style="dim")
    table.add_column("Sev", width=8)
    table.add_column("Rule", width=10)
    table.add_column("File", width=30)
    table.add_column("Message", ratio=1)

    sorted_issues = sorted(issues, key=lambda i: (
        {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(i.severity, 4)
    ))

    for issue in sorted_issues:
        color = SEVERITY_COLORS.get(issue.severity, "white")
        icon = SEVERITY_ICONS.get(issue.severity, " ")
        loc = issue.file
        if issue.line:
            loc += f":{issue.line}"

        table.add_row(
            Text(f"[{icon}] {issue.severity.upper()}", style=color),
            Text(issue.rule_id, style="dim"),
            Text(loc, style="cyan"),
            Text(issue.message),
        )

    console.print(table)


def print_gates(gate_results: dict, console: Console = None):
    if console is None:
        console = Console()

    console.print()
    for gate_name, count in gate_results.items():
        if count == 0:
            console.print(f"  [green]PASS[/green]  {gate_name}")
        else:
            console.print(f"  [red]FAIL[/red]  {gate_name} ({count} issues)")
    console.print()


def print_baseline_changes(changes: list, console: Console = None):
    if console is None:
        console = Console()

    if not changes:
        console.print("[dim]No baseline changes.[/dim]")
        return

    console.print("\n[bold]SINCE LAST SESSION[/bold]")
    for change in changes:
        arrow = "+" if change["delta"] > 0 else ""
        color = "red" if change["is_regression"] else "green"
        flag = " [REGRESSION]" if change["is_regression"] else ""
        console.print(
            f"  [{color}]{change['metric']}: {change['previous']} -> {change['current']} "
            f"({arrow}{change['delta']}){flag}[/{color}]"
        )


def print_handoff(handoff_text: str, console: Console = None):
    if console is None:
        console = Console()

    panel = Panel(
        handoff_text,
        title="[bold]SESSION HANDOFF PROMPT[/bold]",
        subtitle="[dim]Copy and paste this into your next AI coding session[/dim]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)
