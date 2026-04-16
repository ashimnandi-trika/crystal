"""Baseline Tracking — Feature 3.

Tracks project metrics across sessions so you can see if things are getting
better or worse. Stores snapshots in .crystal/baseline.json.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from crystal_guard.config import (
    get_crystal_dir, walk_project_files, is_test_file, CODE_EXTENSIONS
)


@staticmethod
def _count_endpoints(project_path: str) -> int:
    """Count API endpoints by looking for route decorators."""
    root = Path(project_path).resolve()
    count = 0
    route_patterns = [
        "@app.", "@router.", "app.get", "app.post", "app.put", "app.delete", "app.patch",
        "router.get", "router.post", "router.put", "router.delete",
        "@api_view", "path(", "re_path(",
    ]
    for f in walk_project_files(project_path, {".py", ".js", ".ts"}):
        if is_test_file(f, root):
            continue
        try:
            content = f.read_text(errors="ignore")
            for pattern in route_patterns:
                count += content.count(pattern)
        except OSError:
            pass
    return count


def capture_baseline(project_path: str, health_score: int, grade: str, issues: list) -> dict:
    """Capture current project metrics as a baseline snapshot."""
    root = Path(project_path).resolve()

    all_files = walk_project_files(project_path, CODE_EXTENSIONS)
    test_files = [f for f in all_files if is_test_file(f, Path(project_path).resolve())]

    # Count lines of code
    total_lines = 0
    for f in all_files:
        try:
            total_lines += len(f.read_text(errors="ignore").split("\n"))
        except OSError:
            pass

    # Count endpoints
    endpoint_count = 0
    route_patterns = [
        "@app.", "@router.", "app.get(", "app.post(", "app.put(", "app.delete(",
        "router.get(", "router.post(", "router.put(", "router.delete(",
    ]
    for f in walk_project_files(project_path, {".py", ".js", ".ts"}):
        if is_test_file(f, root):
            continue
        try:
            content = f.read_text(errors="ignore")
            for pattern in route_patterns:
                endpoint_count += content.count(pattern)
        except OSError:
            pass

    # Count violations by severity
    violation_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for issue in issues:
        violation_counts[issue.severity] = violation_counts.get(issue.severity, 0) + 1

    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "file_count": len(all_files),
        "test_file_count": len(test_files),
        "total_lines": total_lines,
        "endpoint_count": endpoint_count,
        "health_score": health_score,
        "grade": grade,
        "violation_count": sum(violation_counts.values()),
        "violations": violation_counts,
    }
    return snapshot


def load_baselines(project_path: str) -> list:
    """Load all baseline snapshots."""
    baseline_path = get_crystal_dir(project_path) / "baseline.json"
    if baseline_path.exists():
        try:
            with open(baseline_path) as f:
                data = json.load(f)
            return data if isinstance(data, list) else [data]
        except (json.JSONDecodeError, OSError):
            pass
    return []


def save_baseline(project_path: str, snapshot: dict):
    """Append a new baseline snapshot."""
    crystal_dir = get_crystal_dir(project_path)
    crystal_dir.mkdir(parents=True, exist_ok=True)

    baselines = load_baselines(project_path)
    baselines.append(snapshot)

    # Keep last 100 snapshots
    if len(baselines) > 100:
        baselines = baselines[-100:]

    with open(crystal_dir / "baseline.json", "w") as f:
        json.dump(baselines, f, indent=2)


def compare_baselines(current: dict, previous: dict) -> list[dict]:
    """Compare two baselines and return a list of changes."""
    changes = []
    metrics = [
        ("file_count", "files"),
        ("test_file_count", "test files"),
        ("endpoint_count", "endpoints"),
        ("health_score", "health score"),
        ("violation_count", "violations"),
    ]

    for key, label in metrics:
        curr_val = current.get(key, 0)
        prev_val = previous.get(key, 0)
        delta = curr_val - prev_val

        if delta != 0:
            direction = "increased" if delta > 0 else "decreased"
            # For violations and some metrics, increase is bad
            is_regression = False
            if key == "violation_count" and delta > 0:
                is_regression = True
            elif key == "health_score" and delta < 0:
                is_regression = True
            elif key == "test_file_count" and delta < 0:
                is_regression = True

            changes.append({
                "metric": label,
                "previous": prev_val,
                "current": curr_val,
                "delta": delta,
                "direction": direction,
                "is_regression": is_regression,
            })

    return changes
