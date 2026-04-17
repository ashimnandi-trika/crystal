"""Tests for the config loader and helpers."""
from __future__ import annotations

from pathlib import Path

from crystal_guard.config import (
    CrystalConfig,
    get_crystal_dir,
    is_ignored,
    is_test_file,
    load_config,
    save_config,
    walk_project_files,
)


def test_load_config_good(good_project):
    config = load_config(good_project)
    assert config.project_name
    assert config.stack
    assert isinstance(config.checks, dict)
    assert config.severity_threshold in {"critical", "high", "medium", "low"}


def test_load_config_missing_returns_defaults(tmp_path):
    config = load_config(str(tmp_path))
    assert isinstance(config, CrystalConfig)
    assert config.stack == "generic"
    assert config.severity_threshold == "high"


def test_save_and_roundtrip(tmp_path):
    cfg = CrystalConfig(project_name="demo", stack="mern")
    save_config(cfg, str(tmp_path))
    loaded = load_config(str(tmp_path))
    assert loaded.project_name == "demo"
    assert loaded.stack == "mern"


def test_get_crystal_dir(tmp_path):
    assert get_crystal_dir(str(tmp_path)) == tmp_path / ".crystal"


def test_is_ignored_rejects_node_modules(tmp_path):
    (tmp_path / "node_modules").mkdir()
    f = tmp_path / "node_modules" / "x.js"
    f.write_text("x")
    assert is_ignored(f, tmp_path) is True


def test_is_ignored_accepts_plain_file(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("x")
    assert is_ignored(f, tmp_path) is False


def test_is_test_file_detects_pytest():
    assert is_test_file(Path("tests/test_x.py"), Path("."))
    assert is_test_file(Path("src/foo_test.py"), Path("."))
    assert is_test_file(Path("__tests__/x.js"), Path("."))
    assert not is_test_file(Path("src/server.py"), Path("."))


def test_walk_project_files_skips_ignored(good_project):
    files = walk_project_files(good_project)
    for f in files:
        assert "node_modules" not in str(f)
        assert ".git" not in str(f)
