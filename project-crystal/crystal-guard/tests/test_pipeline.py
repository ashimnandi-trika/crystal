"""Tests for pipeline stage progression and thresholds."""
from __future__ import annotations

from crystal_guard.pipeline import (
    STAGE_THRESHOLDS,
    STAGES,
    check_stage_progression,
    get_production_issues,
    get_staging_issues,
    load_pipeline_state,
    save_pipeline_state,
)


def test_stage_thresholds_get_stricter():
    """Each subsequent stage should have a stricter (lower-ranked) threshold."""
    from crystal_guard.analyzers import Severity

    local = Severity(STAGE_THRESHOLDS["local"]).rank
    staging = Severity(STAGE_THRESHOLDS["staging"]).rank
    production = Severity(STAGE_THRESHOLDS["production"]).rank
    # lower rank number = stricter severity → but threshold represents the *minimum blocker*.
    # local blocks at critical only (rank 0), staging blocks down to high (rank 1),
    # production blocks down to medium (rank 2). So thresholds get HIGHER rank as stricter.
    assert local < staging < production


def test_stages_order():
    assert STAGES == ["local", "staging", "production"]


def test_progression_local_always_runs(tmp_path):
    assert check_stage_progression(str(tmp_path), "local") is None


def test_progression_staging_blocked_without_local(tmp_path):
    err = check_stage_progression(str(tmp_path), "staging")
    assert err is not None
    assert "local" in err.lower()


def test_progression_production_blocked_without_staging(tmp_path):
    save_pipeline_state(str(tmp_path), "local", passed=True, score=95, issue_count=0)
    err = check_stage_progression(str(tmp_path), "production")
    assert err is not None
    assert "staging" in err.lower()


def test_progression_production_allowed_after_staging_pass(tmp_path):
    save_pipeline_state(str(tmp_path), "local", passed=True, score=95, issue_count=0)
    save_pipeline_state(str(tmp_path), "staging", passed=True, score=90, issue_count=2)
    err = check_stage_progression(str(tmp_path), "production")
    assert err is None


def test_failure_invalidates_higher_stages(tmp_path):
    save_pipeline_state(str(tmp_path), "local", passed=True, score=95, issue_count=0)
    save_pipeline_state(str(tmp_path), "staging", passed=True, score=90, issue_count=0)
    # Now fail local → staging/production should be invalidated
    save_pipeline_state(str(tmp_path), "local", passed=False, score=40, issue_count=5)
    state = load_pipeline_state(str(tmp_path))
    assert state["staging"] is None
    assert state["production"] is None


def test_staging_flags_localhost_urls(tmp_path):
    (tmp_path / "backend").mkdir()
    (tmp_path / "backend" / "config.py").write_text('URL = "http://localhost:8000/api"')
    issues = get_staging_issues(str(tmp_path))
    assert any(i.rule_id == "stg-001" for i in issues)


def test_staging_flags_missing_env_var(tmp_path):
    (tmp_path / "app.py").write_text('import os\nx = os.environ.get("MY_SECRET")')
    issues = get_staging_issues(str(tmp_path))
    assert any(i.rule_id == "stg-002" and "MY_SECRET" in i.message for i in issues)


def test_staging_ignores_defined_env_var(tmp_path):
    (tmp_path / ".env").write_text("MY_SECRET=x\n")
    (tmp_path / "app.py").write_text('import os\nx = os.environ.get("MY_SECRET")')
    issues = get_staging_issues(str(tmp_path))
    assert not any(i.rule_id == "stg-002" and "MY_SECRET" in i.message for i in issues)


def test_production_requires_passing_tests():
    issues = get_production_issues(".", test_results={"ran": True, "passed": 5, "failed": 2})
    assert any(i.rule_id == "prod-001" and i.severity == "critical" for i in issues)


def test_production_allows_all_tests_passing():
    issues = get_production_issues(".", test_results={"ran": True, "passed": 10, "failed": 0})
    assert not any(i.rule_id == "prod-001" for i in issues)


def test_production_flags_no_test_results():
    issues = get_production_issues(".", test_results=None)
    assert any(i.rule_id == "prod-001" for i in issues)
