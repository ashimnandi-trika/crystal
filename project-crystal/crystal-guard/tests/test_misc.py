"""Tests for stack detection, technical debt tracking, and baseline comparison."""
from __future__ import annotations

from crystal_guard.analyzers import Issue
from crystal_guard.baseline import (
    capture_baseline,
    compare_baselines,
    load_baselines,
    save_baseline,
)
from crystal_guard.debt import (
    get_debt_summary,
    load_debt,
    record_session_debt,
    save_debt,
)
from crystal_guard.detector import detect_stack


# --- Detector tests ---

def test_detect_explicit_config(bad_project):
    # bad_project has .crystal/config.yaml with stack=react-fastapi-mongo
    result = detect_stack(bad_project)
    assert result["stack_id"] == "react-fastapi-mongo"
    assert result["confidence"] == "high"


def test_detect_generic_when_empty(tmp_path):
    result = detect_stack(str(tmp_path))
    assert result["stack_id"] == "generic"
    assert result["confidence"] == "low"


def test_detect_react_frontend(tmp_path):
    (tmp_path / "package.json").write_text('{"dependencies": {"react": "18.0.0"}}')
    result = detect_stack(str(tmp_path))
    assert result["frontend"] == "react"


def test_detect_nextjs_frontend(tmp_path):
    (tmp_path / "package.json").write_text('{"dependencies": {"next": "14.0.0"}}')
    result = detect_stack(str(tmp_path))
    assert result["frontend"] == "nextjs"


def test_detect_fastapi_backend(tmp_path):
    (tmp_path / "requirements.txt").write_text("fastapi==0.100\npymongo==4.0\n")
    result = detect_stack(str(tmp_path))
    assert result["backend"] == "python-fastapi"
    assert result["database"] == "mongodb"


def test_detect_go_backend(tmp_path):
    (tmp_path / "go.mod").write_text("module foo\n")
    result = detect_stack(str(tmp_path))
    assert result["backend"] == "go"


# --- Debt tracker tests ---

def _mk_issue(rule_id="sec-001", file="app.py", sev="critical"):
    return Issue(
        analyzer="security", severity=sev, file=file, line=1,
        rule_id=rule_id, message="x", suggestion="s",
    )


def test_debt_load_empty(tmp_path):
    debt = load_debt(str(tmp_path))
    assert debt == {"entries": [], "recurring": {}}


def test_debt_record_session(tmp_path):
    issues = [_mk_issue()]
    debt = record_session_debt(str(tmp_path), issues, health_score=80)
    assert len(debt["entries"]) == 1
    assert debt["entries"][0]["health_score"] == 80


def test_debt_detects_recurring(tmp_path):
    issue = _mk_issue()
    record_session_debt(str(tmp_path), [issue], health_score=80)
    record_session_debt(str(tmp_path), [issue], health_score=75)
    summary = get_debt_summary(str(tmp_path))
    # Same rule+file appearing twice → recurring
    assert len(summary["recurring_issues"]) == 1
    assert summary["recurring_issues"][0]["count"] == 2


def test_debt_trend_improving(tmp_path):
    """6 sessions with rising scores should show 'improving' trend."""
    for score in [60, 62, 64, 75, 80, 85]:
        record_session_debt(str(tmp_path), [], health_score=score)
    summary = get_debt_summary(str(tmp_path))
    assert summary["trend"] == "improving"


def test_debt_trend_degrading(tmp_path):
    for score in [90, 85, 82, 70, 60, 55]:
        record_session_debt(str(tmp_path), [], health_score=score)
    summary = get_debt_summary(str(tmp_path))
    assert summary["trend"] == "degrading"


def test_debt_caps_at_500(tmp_path):
    debt = {"entries": [{"health_score": 80}] * 600, "recurring": {}}
    save_debt(str(tmp_path), debt)
    loaded = load_debt(str(tmp_path))
    assert len(loaded["entries"]) == 500


# --- Baseline tests ---

def test_capture_baseline(good_project):
    snap = capture_baseline(good_project, 95, "A", [])
    assert snap["file_count"] > 0
    assert snap["health_score"] == 95
    assert snap["violation_count"] == 0


def test_save_and_load_baseline(good_project):
    snap = capture_baseline(good_project, 90, "A", [])
    save_baseline(good_project, snap)
    loaded = load_baselines(good_project)
    assert len(loaded) >= 1


def test_compare_detects_regression():
    prev = {"file_count": 10, "health_score": 90, "violation_count": 2, "test_file_count": 5, "endpoint_count": 3}
    curr = {"file_count": 12, "health_score": 80, "violation_count": 5, "test_file_count": 4, "endpoint_count": 3}
    changes = compare_baselines(curr, prev)
    regressions = [c for c in changes if c["is_regression"]]
    # health dropped, violations rose, tests dropped → 3 regressions
    assert len(regressions) >= 3


def test_compare_no_changes():
    same = {"file_count": 10, "health_score": 90, "violation_count": 0, "test_file_count": 5, "endpoint_count": 3}
    assert compare_baselines(same, same) == []
