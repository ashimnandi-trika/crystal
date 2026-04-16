"""Technical Debt Tracker — Feature 7.

Logs every gate failure, skipped check, and warning across sessions.
Builds a picture of accumulating debt over time.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from crystal_guard.config import get_crystal_dir
from crystal_guard.analyzers import Issue


def load_debt(project_path: str) -> dict:
    """Load the debt tracker."""
    debt_path = get_crystal_dir(project_path) / "debt.json"
    if debt_path.exists():
        try:
            with open(debt_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"entries": [], "recurring": {}}


def save_debt(project_path: str, debt: dict):
    """Save the debt tracker."""
    crystal_dir = get_crystal_dir(project_path)
    crystal_dir.mkdir(parents=True, exist_ok=True)

    # Keep last 500 entries
    if len(debt.get("entries", [])) > 500:
        debt["entries"] = debt["entries"][-500:]

    with open(crystal_dir / "debt.json", "w") as f:
        json.dump(debt, f, indent=2)


def record_session_debt(project_path: str, issues: list[Issue], health_score: int):
    """Record issues from a session into the debt tracker."""
    debt = load_debt(project_path)
    timestamp = datetime.now(timezone.utc).isoformat()

    # Create session entry
    session_entry = {
        "timestamp": timestamp,
        "health_score": health_score,
        "issue_count": len(issues),
        "issues_by_severity": {},
        "issue_ids": [],
    }

    severity_counts = {}
    for issue in issues:
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        session_entry["issue_ids"].append(issue.rule_id)

        # Track recurring issues
        key = f"{issue.rule_id}:{issue.file}"
        if key not in debt["recurring"]:
            debt["recurring"][key] = {
                "rule_id": issue.rule_id,
                "file": issue.file,
                "message": issue.message,
                "severity": issue.severity,
                "first_seen": timestamp,
                "last_seen": timestamp,
                "count": 0,
            }
        debt["recurring"][key]["last_seen"] = timestamp
        debt["recurring"][key]["count"] += 1

    session_entry["issues_by_severity"] = severity_counts
    debt["entries"].append(session_entry)

    save_debt(project_path, debt)
    return debt


def get_debt_summary(project_path: str) -> dict:
    """Get a summary of accumulated technical debt."""
    debt = load_debt(project_path)

    if not debt["entries"]:
        return {"total_sessions": 0, "recurring_issues": [], "trend": "no data"}

    # Find recurring issues (appeared 3+ times)
    recurring = []
    for key, info in debt["recurring"].items():
        if info["count"] >= 2:
            recurring.append(info)

    recurring.sort(key=lambda x: x["count"], reverse=True)

    # Calculate trend
    entries = debt["entries"]
    trend = "stable"
    if len(entries) >= 2:
        recent_scores = [e["health_score"] for e in entries[-3:]]
        older_scores = [e["health_score"] for e in entries[-6:-3]] if len(entries) >= 6 else [entries[0]["health_score"]]
        avg_recent = sum(recent_scores) / len(recent_scores)
        avg_older = sum(older_scores) / len(older_scores)
        if avg_recent > avg_older + 5:
            trend = "improving"
        elif avg_recent < avg_older - 5:
            trend = "degrading"

    return {
        "total_sessions": len(entries),
        "recurring_issues": recurring[:10],
        "trend": trend,
        "latest_score": entries[-1]["health_score"] if entries else None,
    }
