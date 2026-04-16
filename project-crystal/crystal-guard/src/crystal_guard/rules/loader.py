"""Rules loader — loads built-in and custom YAML rules."""

import yaml
from pathlib import Path
from crystal_guard.config import get_crystal_dir


BUILTIN_RULES_DIR = Path(__file__).parent / "builtin"


def load_builtin_rules(stack_id: str) -> dict:
    """Load built-in rules for a given stack."""
    # Try exact match
    for yaml_file in BUILTIN_RULES_DIR.glob("*.yaml"):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f) or {}
            if data.get("meta", {}).get("stack_id") == stack_id:
                return data
        except (yaml.YAMLError, OSError):
            continue

    # Try partial match (e.g., "react" matches "react_python_mongo")
    stack_parts = set(stack_id.lower().replace("-", "_").split("_"))
    best_match = None
    best_score = 0
    for yaml_file in BUILTIN_RULES_DIR.glob("*.yaml"):
        file_parts = set(yaml_file.stem.lower().split("_"))
        score = len(stack_parts & file_parts)
        if score > best_score:
            best_score = score
            try:
                with open(yaml_file) as f:
                    best_match = yaml.safe_load(f) or {}
            except (yaml.YAMLError, OSError):
                pass

    if best_match and best_score > 0:
        return best_match

    # Fallback to generic
    generic_path = BUILTIN_RULES_DIR / "generic.yaml"
    if generic_path.exists():
        with open(generic_path) as f:
            return yaml.safe_load(f) or {}

    return {}


def load_custom_rules(project_path: str) -> dict:
    """Load custom rules from .crystal/rules.yaml."""
    rules_path = get_crystal_dir(project_path) / "rules.yaml"
    if rules_path.exists():
        try:
            with open(rules_path) as f:
                return yaml.safe_load(f) or {}
        except (yaml.YAMLError, OSError):
            pass
    return {}


def merge_rules(builtin: dict, custom: dict) -> dict:
    """Merge custom rules on top of built-in rules."""
    merged = dict(builtin)

    # Apply overrides
    overrides = custom.get("overrides", {})
    disabled = set(overrides.get("disabled_rules", []))
    severity_overrides = overrides.get("severity_overrides", {})

    # Remove disabled rules from all sections
    for section_key in ["domain_purity", "security", "placeholders"]:
        section = merged.get(section_key, {})
        for sub_key, sub_val in section.items():
            if isinstance(sub_val, dict):
                for check_list_key in ["forbidden", "checks"]:
                    checks = sub_val.get(check_list_key, [])
                    sub_val[check_list_key] = [
                        c for c in checks if c.get("id") not in disabled
                    ]
                    # Apply severity overrides
                    for check in sub_val.get(check_list_key, []):
                        if check.get("id") in severity_overrides:
                            check["severity"] = severity_overrides[check["id"]]

    # Add custom rules to placeholders section
    custom_rules = custom.get("custom_rules", [])
    if custom_rules:
        if "placeholders" not in merged:
            merged["placeholders"] = {}
        if "global" not in merged["placeholders"]:
            merged["placeholders"]["global"] = {"checks": []}
        existing = merged["placeholders"]["global"].get("checks", [])
        existing.extend(custom_rules)
        merged["placeholders"]["global"]["checks"] = existing

    return merged


def load_rules(project_path: str, stack_id: str) -> dict:
    """Load and merge rules for a project."""
    builtin = load_builtin_rules(stack_id)
    custom = load_custom_rules(project_path)
    return merge_rules(builtin, custom)
