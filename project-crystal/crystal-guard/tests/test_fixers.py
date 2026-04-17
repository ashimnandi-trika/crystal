"""Tests for per-rule auto-fixers."""
from __future__ import annotations

from crystal_guard.analyzers import Issue
from crystal_guard.fixers import AUTO_FIXERS


def mk(rule_id: str, file: str = ".", sev: str = "medium") -> Issue:
    return Issue(
        analyzer="architecture", severity=sev, file=file, line=None,
        rule_id=rule_id, message="m", suggestion="s",
    )


def test_whitelist_is_non_empty():
    assert len(AUTO_FIXERS) > 0
    # Core fixes must be present
    for rid in ["arch-001", "arch-002", "arch-003", "arch-006", "sec-004"]:
        assert rid in AUTO_FIXERS


def test_arch001_creates_missing_directory(tmp_path):
    issue = mk("arch-001", file="backend")
    fixer = AUTO_FIXERS["arch-001"]
    assert fixer.already_done(tmp_path, issue) is False
    fixer.apply(tmp_path, issue)
    assert (tmp_path / "backend").is_dir()
    assert fixer.already_done(tmp_path, issue) is True


def test_arch002_creates_gitignore_with_defaults(tmp_path):
    issue = mk("arch-002", file=".gitignore")
    fixer = AUTO_FIXERS["arch-002"]
    fixer.apply(tmp_path, issue)
    gi = tmp_path / ".gitignore"
    assert gi.exists()
    content = gi.read_text()
    # Sensible defaults should be present
    assert ".env" in content
    assert "node_modules" in content
    assert "__pycache__" in content


def test_arch003_creates_readme(tmp_path):
    issue = mk("arch-003", file="README.md")
    fixer = AUTO_FIXERS["arch-003"]
    fixer.apply(tmp_path, issue)
    readme = tmp_path / "README.md"
    assert readme.exists()
    assert tmp_path.name in readme.read_text()


def test_arch003_creates_directory_with_gitkeep(tmp_path):
    issue = mk("arch-003", file="tests/")
    fixer = AUTO_FIXERS["arch-003"]
    fixer.apply(tmp_path, issue)
    assert (tmp_path / "tests").is_dir()
    # Empty dir should get a .gitkeep so git tracks it
    assert (tmp_path / "tests" / ".gitkeep").exists()


def test_arch006_appends_env_to_gitignore(tmp_path):
    (tmp_path / ".gitignore").write_text("node_modules/\n")
    issue = mk("arch-006", file=".gitignore")
    fixer = AUTO_FIXERS["arch-006"]
    assert fixer.already_done(tmp_path, issue) is False
    fixer.apply(tmp_path, issue)
    content = (tmp_path / ".gitignore").read_text()
    assert ".env" in content.splitlines()
    assert "node_modules/" in content  # Existing content preserved
    assert fixer.already_done(tmp_path, issue) is True


def test_arch006_is_idempotent(tmp_path):
    """Running the fixer twice should not duplicate .env."""
    (tmp_path / ".gitignore").write_text("node_modules/\n.env\n")
    issue = mk("arch-006")
    fixer = AUTO_FIXERS["arch-006"]
    fixer.apply(tmp_path, issue)
    fixer.apply(tmp_path, issue)
    lines = (tmp_path / ".gitignore").read_text().splitlines()
    assert lines.count(".env") == 1


def test_arch006_creates_gitignore_if_missing(tmp_path):
    """When .gitignore is absent, arch-006 should create one with defaults."""
    issue = mk("arch-006")
    fixer = AUTO_FIXERS["arch-006"]
    fixer.apply(tmp_path, issue)
    assert (tmp_path / ".gitignore").exists()
    assert ".env" in (tmp_path / ".gitignore").read_text()


def test_sec004_same_as_arch006(tmp_path):
    """sec-004 is critical; fixer must still work regardless of severity."""
    (tmp_path / ".gitignore").write_text("")
    issue = mk("sec-004", sev="critical")
    fixer = AUTO_FIXERS["sec-004"]
    fixer.apply(tmp_path, issue)
    assert ".env" in (tmp_path / ".gitignore").read_text()


def test_arch007_creates_tests_with_placeholder(tmp_path):
    issue = mk("arch-007", file="tests/", sev="high")
    fixer = AUTO_FIXERS["arch-007"]
    assert fixer.already_done(tmp_path, issue) is False
    fixer.apply(tmp_path, issue)
    assert (tmp_path / "tests").is_dir()
    test_files = list((tmp_path / "tests").glob("test_*.py"))
    assert len(test_files) == 1
    assert fixer.already_done(tmp_path, issue) is True


def test_describe_mentions_rule_action():
    # Sanity check: each fixer describes what it will do
    for rule_id, fixer in AUTO_FIXERS.items():
        desc = fixer.describe(mk(rule_id))
        assert isinstance(desc, str)
        assert len(desc) > 5
