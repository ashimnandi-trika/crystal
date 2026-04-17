"""Tests for the architecture analyzer."""
from __future__ import annotations

from crystal_guard.analyzers import architecture
from crystal_guard.config import load_config
from crystal_guard.rules.loader import load_rules


def _rules(path: str):
    return load_rules(path, load_config(path).stack)


def test_good_project_has_minimal_arch_issues(good_project):
    issues = architecture.analyze(good_project, _rules(good_project))
    critical = [i for i in issues if i.severity in ("critical", "high")]
    assert len(critical) == 0, [i.rule_id for i in critical]


def test_bad_project_flags_env_not_in_gitignore(bad_project):
    issues = architecture.analyze(bad_project, _rules(bad_project))
    rule_ids = {i.rule_id for i in issues}
    # bad_project has no .gitignore → arch-002 fires
    assert "arch-002" in rule_ids


def test_bad_project_flags_missing_tests(bad_project):
    issues = architecture.analyze(bad_project, _rules(bad_project))
    assert any(i.rule_id == "arch-007" for i in issues)


def test_arch_returns_issue_dataclass(bad_project):
    issues = architecture.analyze(bad_project, _rules(bad_project))
    for i in issues:
        assert i.analyzer == "architecture"
        assert i.severity in ("critical", "high", "medium", "low")
        assert i.rule_id
        assert i.message
