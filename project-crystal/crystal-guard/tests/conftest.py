"""Shared pytest fixtures for Crystal tests."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

FIXTURES_ROOT = Path(__file__).parent / "fixtures"


def _clone(name: str, dest_root: Path) -> str:
    src = FIXTURES_ROOT / name
    dest = dest_root / name
    shutil.copytree(src, dest)
    # Initialize git so handoff/diff tests have a git state
    subprocess.run(["git", "init", "-q"], cwd=dest, check=False)
    subprocess.run(["git", "config", "user.email", "t@test"], cwd=dest, check=False)
    subprocess.run(["git", "config", "user.name", "test"], cwd=dest, check=False)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=False)
    subprocess.run(["git", "commit", "-qm", "init", "--allow-empty"], cwd=dest, check=False)
    return str(dest)


@pytest.fixture
def good_project(tmp_path: Path) -> str:
    return _clone("good_project", tmp_path)


@pytest.fixture
def bad_project(tmp_path: Path) -> str:
    return _clone("bad_project", tmp_path)


@pytest.fixture
def mixed_project(tmp_path: Path) -> str:
    return _clone("mixed_project", tmp_path)
