"""Per-rule auto-fixers for `crystal fix`.

Each fixer handles ONE rule_id. It must:
- be idempotent (running twice is a no-op)
- never modify source code (only config / filesystem scaffolding)
- fail loudly via OSError on IO issues

Supported rules (LOW/MEDIUM severity only, safe ops only):
- arch-001: create missing expected directory
- arch-002: create missing .gitignore (with sensible defaults)
- arch-003: create missing recommended file/dir (README.md, tests/)
- arch-006: append .env to existing .gitignore
- arch-007: create tests/ directory with a placeholder
- sec-004: append .env to existing .gitignore (same as arch-006)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from crystal_guard.analyzers import Issue


DEFAULT_GITIGNORE = """# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
.ruff_cache/
venv/
.venv/

# Node
node_modules/
dist/
build/
.next/

# Env
.env
.env.local

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
"""

DEFAULT_README_TEMPLATE = """# {name}

## Getting started

Describe how to install, configure, and run the project.

## Development

Document the architecture decisions and project layout here.

## Testing

Add test instructions here.
"""


@dataclass
class Fixer:
    """A per-rule auto-fixer."""
    describe: Callable[[Issue], str]
    target_key: Callable[[Path, Issue], str]
    already_done: Callable[[Path, Issue], bool]
    apply: Callable[[Path, Issue], None]


# --- arch-001: create missing expected directory ---

def _arch001_apply(root: Path, issue: Issue) -> None:
    (root / issue.file).mkdir(parents=True, exist_ok=True)


def _arch001_done(root: Path, issue: Issue) -> bool:
    return (root / issue.file).exists()


# --- arch-002 / arch-003 (.gitignore): create with sensible defaults ---

def _create_gitignore(root: Path, _: Issue) -> None:
    gi = root / ".gitignore"
    if not gi.exists():
        gi.write_text(DEFAULT_GITIGNORE)


def _gitignore_exists(root: Path, _: Issue) -> bool:
    return (root / ".gitignore").exists()


# --- arch-003: create missing recommended file/dir (README.md, tests/) ---

def _arch003_apply(root: Path, issue: Issue) -> None:
    target = root / issue.file.rstrip("/")
    if issue.file.endswith("/") or target.suffix == "":
        target.mkdir(parents=True, exist_ok=True)
        # Add a gitkeep or placeholder so the dir is checked-in
        if target.is_dir() and not any(target.iterdir()):
            (target / ".gitkeep").write_text("")
    elif target.name.lower() == "readme.md":
        target.write_text(DEFAULT_README_TEMPLATE.format(name=root.name))
    else:
        target.touch()


def _arch003_done(root: Path, issue: Issue) -> bool:
    return (root / issue.file.rstrip("/")).exists()


# --- arch-006 / sec-004: append .env to existing .gitignore ---

def _ensure_env_in_gitignore(root: Path, _: Issue) -> None:
    gi = root / ".gitignore"
    if gi.exists():
        lines = gi.read_text().splitlines()
        if ".env" not in lines:
            # Append with a newline guard
            with open(gi, "a") as f:
                if lines and lines[-1].strip():
                    f.write("\n")
                f.write(".env\n")
    else:
        gi.write_text(DEFAULT_GITIGNORE)


def _env_in_gitignore(root: Path, _: Issue) -> bool:
    gi = root / ".gitignore"
    if not gi.exists():
        return False
    return ".env" in gi.read_text().splitlines()


# --- arch-007: create tests/ directory placeholder ---

def _arch007_apply(root: Path, _: Issue) -> None:
    tests = root / "tests"
    tests.mkdir(parents=True, exist_ok=True)
    placeholder = tests / "test_placeholder.py"
    if not placeholder.exists():
        placeholder.write_text(
            "def test_placeholder():\n"
            "    \"\"\"Replace me with a real test.\"\"\"\n"
            "    assert True\n"
        )


def _arch007_done(root: Path, _: Issue) -> bool:
    return (root / "tests").exists() and any((root / "tests").glob("test_*.py"))


AUTO_FIXERS: dict[str, Fixer] = {
    "arch-001": Fixer(
        describe=lambda i: f"Create missing directory '{i.file}'",
        target_key=lambda root, i: str(i.file),
        already_done=_arch001_done,
        apply=_arch001_apply,
    ),
    "arch-002": Fixer(
        describe=lambda i: f"Create required file '{i.file}' with sensible defaults",
        target_key=lambda root, i: str(i.file),
        already_done=_gitignore_exists,
        apply=_create_gitignore,
    ),
    "arch-003": Fixer(
        describe=lambda i: f"Create recommended '{i.file}'",
        target_key=lambda root, i: str(i.file),
        already_done=_arch003_done,
        apply=_arch003_apply,
    ),
    "arch-006": Fixer(
        describe=lambda i: "Append '.env' to .gitignore",
        target_key=lambda root, i: ".env:.gitignore",
        already_done=_env_in_gitignore,
        apply=_ensure_env_in_gitignore,
    ),
    "arch-007": Fixer(
        describe=lambda i: "Create tests/ directory with a placeholder test",
        target_key=lambda root, i: "tests/",
        already_done=_arch007_done,
        apply=_arch007_apply,
    ),
    "sec-004": Fixer(
        describe=lambda i: "Append '.env' to .gitignore (prevent secret leak)",
        target_key=lambda root, i: ".env:.gitignore",
        already_done=_env_in_gitignore,
        apply=_ensure_env_in_gitignore,
    ),
}
