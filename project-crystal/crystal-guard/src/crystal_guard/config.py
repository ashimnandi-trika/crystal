"""Configuration management for Crystal Guard."""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field


CRYSTAL_DIR = ".crystal"
CONFIG_FILE = "config.yaml"
BASELINE_FILE = "baseline.json"
DEBT_FILE = "debt.json"
PRD_FILE = "prd.md"
SESSIONS_FILE = "sessions.json"

IGNORE_DIRS = {
    "node_modules", "venv", ".venv", "__pycache__", ".git", "build", "dist",
    ".next", ".nuxt", "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "egg-info", ".eggs", ".tox", "htmlcov", ".crystal",
}

IGNORE_EXTENSIONS = {".pyc", ".pyo", ".so", ".o", ".a", ".dylib", ".wasm", ".map"}

CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte",
    ".go", ".rs", ".rb", ".java", ".kt", ".swift", ".cs",
    ".html", ".css", ".scss", ".less", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".env", ".md", ".txt", ".sql",
    ".sh", ".bash", ".zsh", ".fish", ".dockerfile",
}

TEST_PATTERNS = {
    "test_", "_test.", ".test.", ".spec.", "tests/", "test/",
    "__tests__", "conftest", "pytest", "jest.config", "vitest",
}


@dataclass
class CrystalConfig:
    project_name: str = ""
    stack: str = "generic"
    project_path: str = "."
    severity_threshold: str = "high"
    checks: dict = field(default_factory=lambda: {
        "architecture": True,
        "domain_purity": True,
        "security": True,
        "placeholders": True,
    })
    ignore_files: list = field(default_factory=lambda: [
        "node_modules/**", "venv/**", ".git/**", "build/**", "dist/**",
    ])
    ignore_rules: list = field(default_factory=list)
    custom_rules: list = field(default_factory=list)


def get_crystal_dir(project_path: str = ".") -> Path:
    return Path(project_path) / CRYSTAL_DIR


def load_config(project_path: str = ".") -> CrystalConfig:
    config_path = get_crystal_dir(project_path) / CONFIG_FILE
    config = CrystalConfig(project_path=os.path.abspath(project_path))

    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}

        proj = data.get("project", {})
        config.project_name = proj.get("name", "")
        config.stack = proj.get("stack", "generic")

        checks = data.get("checks", {})
        for k, v in checks.items():
            config.checks[k] = v

        config.severity_threshold = data.get("severity_threshold", "high")

        ignore = data.get("ignore", {})
        config.ignore_files = ignore.get("files", config.ignore_files)
        config.ignore_rules = ignore.get("rules", [])
        config.custom_rules = data.get("custom_rules", [])

    return config


def save_config(config: CrystalConfig, project_path: str = "."):
    crystal_dir = get_crystal_dir(project_path)
    crystal_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "project": {
            "name": config.project_name,
            "stack": config.stack,
        },
        "checks": config.checks,
        "severity_threshold": config.severity_threshold,
        "ignore": {
            "files": config.ignore_files,
            "rules": config.ignore_rules,
        },
    }

    with open(crystal_dir / CONFIG_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def is_ignored(path: Path, project_root: Path) -> bool:
    parts = path.relative_to(project_root).parts
    for part in parts:
        if part in IGNORE_DIRS:
            return True
    if path.suffix in IGNORE_EXTENSIONS:
        return True
    return False


def walk_project_files(project_path: str = ".", extensions: set = None) -> list:
    root = Path(project_path).resolve()
    if extensions is None:
        extensions = CODE_EXTENSIONS
    files = []
    for path in root.rglob("*"):
        if path.is_file() and not is_ignored(path, root):
            if extensions is None or path.suffix in extensions:
                files.append(path)
    return files


def is_test_file(path: Path, project_root: Path = None) -> bool:
    """Check if a file is a test file based on its name and relative path."""
    name = path.name.lower()
    # Only check the filename and immediate parent, not full absolute path
    if project_root:
        try:
            rel = str(path.relative_to(project_root)).lower()
        except ValueError:
            rel = name
    else:
        rel = name

    name_patterns = {"test_", "_test.", ".test.", ".spec.", "conftest"}
    dir_patterns = {"tests/", "test/", "__tests__/"}

    for p in name_patterns:
        if p in name:
            return True

    # Check if the file is directly inside a test directory
    parts = Path(rel).parts
    for part in parts[:-1]:  # Exclude filename itself
        if part.lower() in {"tests", "test", "__tests__", "spec"}:
            return True

    return False
