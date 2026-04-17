"""Test Runner — Executes actual test suites (pytest, npm test, etc.)

Crystal doesn't just check if test files exist. It RUNS your tests
and reports which ones pass and which ones fail.
"""

import subprocess
import json
from pathlib import Path


def detect_test_runner(project_path: str) -> dict:
    """Auto-detect which test runner the project uses."""
    root = Path(project_path).resolve()

    # Check for Python test runners
    for req_path in [root / "requirements.txt", root / "backend" / "requirements.txt"]:
        if req_path.exists():
            content = req_path.read_text().lower()
            if "pytest" in content:
                return {"runner": "pytest", "command": ["python", "-m", "pytest", "--tb=short", "-q"], "type": "python"}

    # Check if pytest is importable
    if (root / "tests").exists() or list(root.rglob("test_*.py")):
        return {"runner": "pytest", "command": ["python", "-m", "pytest", "--tb=short", "-q"], "type": "python"}

    # Check for Node test runners
    pkg_paths = [root / "package.json", root / "frontend" / "package.json"]
    for pkg_path in pkg_paths:
        if pkg_path.exists():
            try:
                with open(pkg_path) as f:
                    pkg = json.load(f)
                scripts = pkg.get("scripts", {})
                if "test" in scripts:
                    test_cmd = scripts["test"]
                    if "vitest" in test_cmd:
                        return {"runner": "vitest", "command": ["npx", "vitest", "run"], "type": "node", "cwd": str(pkg_path.parent)}
                    elif "jest" in test_cmd or "react-scripts test" in test_cmd:
                        return {"runner": "jest", "command": ["npx", "react-scripts", "test", "--watchAll=false", "--ci"], "type": "node", "cwd": str(pkg_path.parent)}
                    else:
                        return {"runner": "npm-test", "command": ["npm", "test", "--", "--watchAll=false"], "type": "node", "cwd": str(pkg_path.parent)}
            except (json.JSONDecodeError, OSError):
                pass

    return {"runner": None, "command": None, "type": None}


def run_tests(project_path: str) -> dict:
    """Run the project's test suite and return results."""
    root = Path(project_path).resolve()
    runner_info = detect_test_runner(project_path)

    result = {
        "runner": runner_info["runner"],
        "ran": False,
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": [],
        "pass_rate": 0,
        "output": "",
    }

    if not runner_info["command"]:
        result["output"] = "No test runner detected."
        return result

    cwd = runner_info.get("cwd", str(root))

    try:
        proc = subprocess.run(
            runner_info["command"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=120,
        )
        result["ran"] = True
        result["output"] = proc.stdout + proc.stderr

        # Parse pytest output
        if runner_info["runner"] == "pytest":
            _parse_pytest(result, proc)
        # Parse jest/vitest output
        elif runner_info["type"] == "node":
            _parse_node_tests(result, proc)

    except subprocess.TimeoutExpired:
        result["ran"] = True
        result["output"] = "Tests timed out after 120 seconds."
        result["errors"].append("Test suite timed out.")
    except FileNotFoundError:
        result["output"] = f"Test runner '{runner_info['runner']}' not found. Install it first."
    except OSError as e:
        result["output"] = f"Failed to run tests: {e}"

    # Calculate pass rate
    if result["total"] > 0:
        result["pass_rate"] = round((result["passed"] / result["total"]) * 100)

    return result


def _parse_pytest(result: dict, proc):
    """Parse pytest output for test counts."""
    output = proc.stdout + proc.stderr

    # pytest summary line: "5 passed, 2 failed, 1 skipped" or "=== 5 passed ==="
    import re
    for line in output.split("\n"):
        line = line.strip()
        m = re.search(r'(\d+)\s+passed', line)
        if m:
            result["passed"] = int(m.group(1))
        m = re.search(r'(\d+)\s+failed', line)
        if m:
            result["failed"] = int(m.group(1))
        m = re.search(r'(\d+)\s+skipped', line)
        if m:
            result["skipped"] = int(m.group(1))
        m = re.search(r'(\d+)\s+error', line)
        if m:
            result["failed"] += int(m.group(1))

    result["total"] = result["passed"] + result["failed"] + result["skipped"]

    # If we couldn't parse, check return code
    if result["total"] == 0 and proc.returncode == 0:
        result["passed"] = 1
        result["total"] = 1
    elif result["total"] == 0 and proc.returncode != 0:
        result["failed"] = 1
        result["total"] = 1

    # Capture failure details
    if result["failed"] > 0:
        for line in output.split("\n"):
            if line.strip().startswith("FAILED"):
                result["errors"].append(line.strip())


def _parse_node_tests(result: dict, proc):
    """Parse Jest/Vitest output."""
    output = proc.stdout + proc.stderr

    for line in output.split("\n"):
        line = line.strip()
        # Jest: "Tests: 2 failed, 5 passed, 7 total"
        if "Tests:" in line and "total" in line:
            parts = line.split(",")
            for part in parts:
                part = part.strip()
                words = part.split()
                if len(words) < 1:
                    continue
                try:
                    val = int(words[0])
                except (ValueError, IndexError):
                    continue
                if "passed" in part:
                    result["passed"] = val
                elif "failed" in part:
                    result["failed"] = val
                elif "skipped" in part or "pending" in part:
                    result["skipped"] = val
                elif "total" in part:
                    result["total"] = val

    if result["total"] == 0:
        result["total"] = result["passed"] + result["failed"] + result["skipped"]

    if result["total"] == 0:
        if proc.returncode == 0:
            result["passed"] = 1
            result["total"] = 1
        else:
            result["failed"] = 1
            result["total"] = 1
            result["errors"].append("Test suite failed (non-zero exit code).")
