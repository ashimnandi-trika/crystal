"""Health Score Calculator."""

from dataclasses import dataclass, asdict
from crystal_guard.analyzers import Issue, Severity


@dataclass
class HealthReport:
    score: int
    grade: str
    summary: str
    breakdown: dict
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    top_issues: list
    total_issues: int
    passed: bool

    def to_dict(self) -> dict:
        d = asdict(self)
        d["top_issues"] = [i.to_dict() if isinstance(i, Issue) else i for i in self.top_issues]
        return d


def calculate_health(issues: list[Issue], threshold: str = "high") -> HealthReport:
    score = 100
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    by_analyzer = {}

    for issue in issues:
        sev = Severity(issue.severity)
        score -= sev.points
        counts[issue.severity] += 1
        by_analyzer.setdefault(issue.analyzer, 0)
        by_analyzer[issue.analyzer] += sev.points

    score = max(0, score)

    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 40:
        grade = "D"
    else:
        grade = "F"

    summaries = {
        "A": "Excellent structure. Ship with confidence.",
        "B": "Good structure with minor issues. Quick fixes recommended.",
        "C": f"Needs attention. {counts['critical']} critical and {counts['high']} high-severity issues found.",
        "D": "Significant structural problems detected. Fix before deploying.",
        "F": "Critical issues found. Do not deploy until resolved.",
    }
    summary = summaries[grade]

    # Sort issues by severity for top issues
    sorted_issues = sorted(issues, key=lambda i: Severity(i.severity).rank)
    top_issues = sorted_issues[:5]

    # Determine pass/fail
    threshold_rank = Severity(threshold).rank if threshold in [s.value for s in Severity] else 1
    passed = all(Severity(i.severity).rank > threshold_rank for i in issues)
    if counts["critical"] > 0:
        passed = False

    # Breakdown per analyzer
    breakdown = {}
    analyzer_max = {"architecture": 30, "domain": 25, "security": 25, "placeholders": 20}
    for analyzer, max_pts in analyzer_max.items():
        lost = by_analyzer.get(analyzer, 0)
        breakdown[analyzer] = max(0, max_pts - lost)

    return HealthReport(
        score=score,
        grade=grade,
        summary=summary,
        breakdown=breakdown,
        critical_count=counts["critical"],
        high_count=counts["high"],
        medium_count=counts["medium"],
        low_count=counts["low"],
        top_issues=top_issues,
        total_issues=len(issues),
        passed=passed,
    )
