"""Tests for the dependency analyzer."""
from __future__ import annotations

from crystal_guard.analyzers import dependencies


def test_analyze_runs_on_good_project(good_project):
    # Should not crash
    issues = dependencies.analyze(good_project)
    assert isinstance(issues, list)


def test_duplicate_http_clients_flagged(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"dependencies": {"axios": "1.0.0", "node-fetch": "3.0.0"}}'
    )
    issues = dependencies.analyze(str(tmp_path))
    dep_004 = [i for i in issues if i.rule_id == "dep-004"]
    assert len(dep_004) == 1
    assert "HTTP client" in dep_004[0].message


def test_no_duplicates_when_single_http_client(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"dependencies": {"axios": "1.0.0"}}'
    )
    issues = dependencies.analyze(str(tmp_path))
    assert not any(i.rule_id == "dep-004" for i in issues)


def test_duplicate_date_libraries(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"dependencies": {"moment": "1.0.0", "dayjs": "1.0.0", "date-fns": "1.0.0"}}'
    )
    issues = dependencies.analyze(str(tmp_path))
    assert any(i.rule_id == "dep-004" and "Date library" in i.message for i in issues)


def test_unused_python_dep_flagged(tmp_path):
    # requirements includes unused_lib, no code imports it
    (tmp_path / "requirements.txt").write_text("unused_lib==1.0\n")
    (tmp_path / "app.py").write_text("print('hi')\n")
    issues = dependencies.analyze(str(tmp_path))
    assert any(i.rule_id == "dep-003" for i in issues)


def test_used_python_dep_not_flagged(tmp_path):
    (tmp_path / "requirements.txt").write_text("requests==1.0\n")
    (tmp_path / "app.py").write_text("import requests\n")
    issues = dependencies.analyze(str(tmp_path))
    dep_003 = [i for i in issues if i.rule_id == "dep-003" and "requests" in i.message]
    assert len(dep_003) == 0


def test_framework_deps_not_flagged_as_unused(tmp_path):
    (tmp_path / "requirements.txt").write_text("uvicorn==1.0\npytest==8.0\n")
    (tmp_path / "app.py").write_text("print('hi')\n")
    issues = dependencies.analyze(str(tmp_path))
    # uvicorn/pytest should not be flagged as unused
    assert not any(
        i.rule_id == "dep-003" and ("uvicorn" in i.message or "pytest" in i.message)
        for i in issues
    )
