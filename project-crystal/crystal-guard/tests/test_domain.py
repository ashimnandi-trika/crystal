"""Tests for the domain purity analyzer."""
from __future__ import annotations

from crystal_guard.analyzers import domain
from crystal_guard.config import load_config
from crystal_guard.rules.loader import load_rules


def _rules(path: str):
    return load_rules(path, load_config(path).stack)


def test_good_project_no_domain_violations(good_project):
    issues = domain.analyze(good_project, _rules(good_project))
    critical = [i for i in issues if i.severity == "critical"]
    assert len(critical) == 0, [i.rule_id for i in critical]


def test_bad_project_flags_db_in_frontend(bad_project):
    issues = domain.analyze(bad_project, _rules(bad_project))
    # bad_project has mongodb import in App.jsx
    assert any(i.rule_id.startswith("dom-") for i in issues), [i.rule_id for i in issues]


def test_issues_have_file_and_line(bad_project):
    issues = domain.analyze(bad_project, _rules(bad_project))
    for i in issues:
        assert i.analyzer == "domain"
        assert i.file
        assert i.line is None or i.line > 0
