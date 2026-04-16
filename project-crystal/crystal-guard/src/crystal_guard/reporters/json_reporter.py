"""JSON reporter for CI/CD integration."""

import json
from datetime import datetime, timezone


def generate_json_report(health_report, issues: list, config=None) -> str:
    return json.dumps({
        "crystal_guard_version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project": config.project_name if config else "",
        "stack": config.stack if config else "generic",
        "health": health_report.to_dict(),
        "issues": [i.to_dict() for i in issues],
        "passed": health_report.passed,
    }, indent=2)
