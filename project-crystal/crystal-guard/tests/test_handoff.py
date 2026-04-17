"""Tests for handoff prompt generation and project metrics."""
from __future__ import annotations

from crystal_guard.handoff import (
    generate_handoff_prompt,
    get_git_state,
    get_project_metrics,
    save_session,
)
from crystal_guard.scoring import calculate_health


def test_metrics_counts_files(good_project):
    m = get_project_metrics(good_project)
    assert m["file_count"] > 0
    assert m["test_file_count"] >= 1  # good_project has a test


def test_metrics_counts_endpoints(good_project):
    m = get_project_metrics(good_project)
    assert isinstance(m["endpoint_count"], int)


def test_git_state_detected(good_project):
    g = get_git_state(good_project)
    assert g["has_git"] is True
    assert g["branch"]


def test_git_state_missing(tmp_path):
    g = get_git_state(str(tmp_path))
    assert g["has_git"] is False


def test_handoff_prompt_non_empty(good_project):
    metrics = get_project_metrics(good_project)
    git = get_git_state(good_project)
    health = calculate_health([])
    text = generate_handoff_prompt(
        good_project, git, metrics, health,
        baseline_changes=[], debt_summary={"total": 0, "by_category": {}},
    )
    assert "SESSION HANDOFF" in text
    assert health.grade in text


def test_handoff_includes_regression_warning(good_project):
    metrics = get_project_metrics(good_project)
    git = get_git_state(good_project)
    health = calculate_health([])
    regression = [{
        "metric": "test files", "previous": 10, "current": 5,
        "delta": -5, "is_regression": True,
    }]
    text = generate_handoff_prompt(
        good_project, git, metrics, health,
        baseline_changes=regression, debt_summary={"total": 0, "by_category": {}},
    )
    assert "REGRESSION" in text.upper() or "regression" in text.lower()


def test_save_session_writes_file(good_project):
    metrics = get_project_metrics(good_project)
    save_session(good_project, "handoff content", metrics, health_score=80)
    from pathlib import Path
    sessions = Path(good_project) / ".crystal" / "sessions.json"
    assert sessions.exists()
