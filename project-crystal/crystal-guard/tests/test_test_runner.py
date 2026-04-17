"""Tests for test_runner detection and output parsing."""
from __future__ import annotations

from types import SimpleNamespace

from crystal_guard.test_runner import _parse_node_tests, _parse_pytest, detect_test_runner


# --- Detection tests ---

def test_detect_pytest_from_requirements(tmp_path):
    (tmp_path / "requirements.txt").write_text("pytest==8.0\n")
    info = detect_test_runner(str(tmp_path))
    assert info["runner"] == "pytest"
    assert info["type"] == "python"


def test_detect_pytest_from_test_dir(tmp_path):
    (tmp_path / "tests").mkdir()
    info = detect_test_runner(str(tmp_path))
    assert info["runner"] == "pytest"


def test_detect_jest(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"scripts": {"test": "jest"}}'
    )
    info = detect_test_runner(str(tmp_path))
    assert info["runner"] == "jest"


def test_detect_vitest(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"scripts": {"test": "vitest"}}'
    )
    info = detect_test_runner(str(tmp_path))
    assert info["runner"] == "vitest"


def test_detect_no_runner(tmp_path):
    info = detect_test_runner(str(tmp_path))
    assert info["runner"] is None


# --- Output parser tests ---

def _proc(stdout="", stderr="", returncode=0):
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def test_parse_pytest_all_passed():
    result = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": []}
    _parse_pytest(result, _proc(stdout="========== 10 passed in 1.2s =========="))
    assert result["passed"] == 10
    assert result["failed"] == 0


def test_parse_pytest_mixed():
    result = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": []}
    _parse_pytest(result, _proc(stdout="5 passed, 2 failed, 1 skipped\nFAILED tests/test_x.py::test_y"))
    assert result["passed"] == 5
    assert result["failed"] == 2
    assert result["skipped"] == 1
    assert result["total"] == 8
    assert any("FAILED" in e for e in result["errors"])


def test_parse_pytest_errors_count_as_failed():
    result = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": []}
    _parse_pytest(result, _proc(stdout="3 passed, 1 error"))
    assert result["failed"] == 1


def test_parse_jest_output():
    result = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": []}
    _parse_node_tests(result, _proc(stdout="Tests:       2 failed, 5 passed, 7 total"))
    assert result["passed"] == 5
    assert result["failed"] == 2
    assert result["total"] == 7


def test_parse_node_empty_but_returncode_zero():
    result = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": []}
    _parse_node_tests(result, _proc(returncode=0))
    assert result["passed"] == 1
    assert result["total"] == 1


def test_parse_node_empty_with_error():
    result = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": []}
    _parse_node_tests(result, _proc(returncode=1))
    assert result["failed"] == 1
    assert result["total"] == 1
