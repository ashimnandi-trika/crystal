"""Stack auto-detection for Crystal Guard."""

import json
from pathlib import Path


def detect_stack(project_path: str = ".") -> dict:
    """Auto-detect the tech stack of a project by examining its files."""
    root = Path(project_path).resolve()
    result = {
        "frontend": None,
        "backend": None,
        "database": None,
        "stack_id": "generic",
        "confidence": "low",
        "detected_from": [],
    }

    # Check explicit Crystal config first
    config_path = root / ".crystal" / "config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}
        stack = data.get("project", {}).get("stack")
        if stack:
            result["stack_id"] = stack
            result["confidence"] = "high"
            result["detected_from"].append(".crystal/config.yaml")
            return result

    # Detect frontend
    pkg_json = root / "package.json"
    frontend_pkg = root / "frontend" / "package.json"
    pkg_path = frontend_pkg if frontend_pkg.exists() else (pkg_json if pkg_json.exists() else None)

    if pkg_path:
        try:
            with open(pkg_path) as f:
                pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            dep_keys = set(deps.keys())

            if "next" in dep_keys:
                result["frontend"] = "nextjs"
            elif "react" in dep_keys or "react-dom" in dep_keys:
                result["frontend"] = "react"
            elif "vue" in dep_keys:
                result["frontend"] = "vue"
            elif "@angular/core" in dep_keys:
                result["frontend"] = "angular"
            elif "svelte" in dep_keys:
                result["frontend"] = "svelte"

            # Detect Node backend
            if "express" in dep_keys:
                result["backend"] = "node-express"
            elif "@nestjs/core" in dep_keys:
                result["backend"] = "node-nest"

            # Detect DB from JS deps
            if "mongoose" in dep_keys or "mongodb" in dep_keys:
                result["database"] = "mongodb"
            elif "prisma" in dep_keys or "@prisma/client" in dep_keys:
                result["database"] = "postgresql"

            result["detected_from"].append(str(pkg_path.relative_to(root)))
        except (json.JSONDecodeError, OSError):
            pass

    # Detect Python backend
    for req_path in [root / "requirements.txt", root / "backend" / "requirements.txt"]:
        if req_path.exists():
            try:
                content = req_path.read_text().lower()
                if "fastapi" in content:
                    result["backend"] = "python-fastapi"
                elif "flask" in content:
                    result["backend"] = "python-flask"
                elif "django" in content:
                    result["backend"] = "python-django"

                if "pymongo" in content or "motor" in content or "mongoengine" in content:
                    result["database"] = "mongodb"
                elif "sqlalchemy" in content or "psycopg" in content:
                    result["database"] = "postgresql"
                elif "mysqlclient" in content or "pymysql" in content:
                    result["database"] = "mysql"

                result["detected_from"].append(str(req_path.relative_to(root)))
            except OSError:
                pass

    # Check for other indicators
    if (root / "go.mod").exists():
        result["backend"] = "go"
        result["detected_from"].append("go.mod")
    elif (root / "Cargo.toml").exists():
        result["backend"] = "rust"
        result["detected_from"].append("Cargo.toml")
    elif (root / "Gemfile").exists():
        result["backend"] = "ruby-rails"
        result["detected_from"].append("Gemfile")

    # Build stack_id
    parts = []
    if result["frontend"]:
        parts.append(result["frontend"])
    if result["backend"]:
        parts.append(result["backend"].split("-")[-1])
    if result["database"]:
        db_short = {"mongodb": "mongo", "postgresql": "postgres", "mysql": "mysql"}
        parts.append(db_short.get(result["database"], result["database"]))

    if parts:
        result["stack_id"] = "-".join(parts)
        result["confidence"] = "high" if len(parts) >= 2 else "medium"
    else:
        result["stack_id"] = "generic"
        result["confidence"] = "low"

    return result
