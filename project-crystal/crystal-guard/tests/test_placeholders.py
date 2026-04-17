"""Tests for the placeholder / code hygiene analyzer."""
from __future__ import annotations

from crystal_guard.analyzers import placeholders
from crystal_guard.config import load_config
from crystal_guard.rules.loader import load_rules


def _rules(path: str):
    return load_rules(path, load_config(path).stack)


def test_good_project_hygiene_low_noise(good_project):
    issues = placeholders.analyze(good_project, _rules(good_project))
    # Good project may have hyg-002 in architecture.md (example.com reference) — that's okay.
    critical_or_high = [i for i in issues if i.severity in ("critical", "high")]
    assert len(critical_or_high) == 0


def test_bad_project_flags_todo(bad_project):
    issues = placeholders.analyze(bad_project, _rules(bad_project))
    assert any(i.rule_id == "hyg-001" for i in issues)


def test_bad_project_flags_console_log(bad_project):
    issues = placeholders.analyze(bad_project, _rules(bad_project))
    assert any(i.rule_id == "hyg-003" for i in issues)


def test_bad_project_flags_localhost(bad_project):
    issues = placeholders.analyze(bad_project, _rules(bad_project))
    assert any(i.rule_id == "hyg-004" for i in issues)


def test_cap_at_3_per_file(tmp_path):
    """hyg check caps at 3 matches per file to avoid spam."""
    (tmp_path / "x.py").write_text("\n".join([f"# TODO: item {i}" for i in range(10)]))
    issues = placeholders.analyze(str(tmp_path), {})
    todos = [i for i in issues if i.rule_id == "hyg-001"]
    assert len(todos) <= 3


def test_skips_test_files(tmp_path):
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_foo.py").write_text("# TODO: fix this")
    issues = placeholders.analyze(str(tmp_path), {})
    assert not any("test_foo.py" in i.file for i in issues)
