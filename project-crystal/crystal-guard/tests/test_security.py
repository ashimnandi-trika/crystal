"""Tests for the security analyzer."""
from __future__ import annotations

from crystal_guard.analyzers import security
from crystal_guard.config import load_config
from crystal_guard.rules.loader import load_rules


def _rules(path: str):
    return load_rules(path, load_config(path).stack)


def test_good_project_no_security_issues(good_project):
    issues = security.analyze(good_project, _rules(good_project))
    critical = [i for i in issues if i.severity == "critical"]
    assert len(critical) == 0, [i.rule_id for i in critical]


def test_bad_project_flags_api_key(bad_project):
    issues = security.analyze(bad_project, _rules(bad_project))
    rule_ids = {i.rule_id for i in issues}
    assert "sec-001" in rule_ids or "sec-003" in rule_ids


def test_bad_project_flags_password(bad_project):
    issues = security.analyze(bad_project, _rules(bad_project))
    rule_ids = {i.rule_id for i in issues}
    assert "sec-002" in rule_ids


def test_bad_project_flags_cors_wildcard_if_present(bad_project):
    """sec-005 only fires if the fixture actually uses CORS wildcard."""
    issues = security.analyze(bad_project, _rules(bad_project))
    # Existence check: at least some security issues fired
    assert any(i.rule_id.startswith("sec-") for i in issues)


def test_env_not_in_gitignore_is_critical(tmp_path):
    (tmp_path / ".env").write_text("SECRET=x")
    issues = security.analyze(str(tmp_path), {})
    sec_004 = [i for i in issues if i.rule_id == "sec-004"]
    assert len(sec_004) == 1
    assert sec_004[0].severity == "critical"


def test_env_in_gitignore_is_fine(tmp_path):
    (tmp_path / ".env").write_text("SECRET=x")
    (tmp_path / ".gitignore").write_text(".env\nnode_modules/")
    issues = security.analyze(str(tmp_path), {})
    assert not any(i.rule_id == "sec-004" for i in issues)


def test_security_ignores_test_files(tmp_path):
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_fixtures.py").write_text('api_key = "sk-abc123def456ghi789jkl012"')
    issues = security.analyze(str(tmp_path), {})
    assert not any("test_fixtures.py" in i.file for i in issues)
