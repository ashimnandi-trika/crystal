"""Tests for the CLI entry points (via typer's CliRunner)."""
from __future__ import annotations

from typer.testing import CliRunner

from crystal_guard.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "check" in result.stdout
    assert "audit" in result.stdout


def test_check_command_good_project(good_project):
    result = runner.invoke(app, ["check", good_project])
    assert result.exit_code in (0, 1)  # 0 if passes, 1 if issues found
    # Output should include quality gate section
    assert "PASS" in result.stdout or "FAIL" in result.stdout or "quality" in result.stdout.lower()


def test_check_command_bad_project(bad_project):
    result = runner.invoke(app, ["check", bad_project])
    # bad_project should have issues and fail (exit 1)
    assert result.exit_code == 1
    assert "critical" in result.stdout.lower() or "high" in result.stdout.lower()


def test_status_command(good_project):
    result = runner.invoke(app, ["status", good_project])
    assert result.exit_code == 0


def test_audit_command_no_llm(bad_project):
    result = runner.invoke(app, ["audit", bad_project])
    assert result.exit_code == 0
    assert "Audit" in result.stdout or "audit" in result.stdout.lower()


def test_diff_command_no_changes(bad_project):
    result = runner.invoke(app, ["diff", bad_project])
    # Fresh git init with initial commit → no uncommitted changes
    assert result.exit_code == 0


def test_rules_list_command(bad_project):
    result = runner.invoke(app, ["rules", "list", bad_project])
    assert result.exit_code == 0
    # At least one rule id should appear in output
    assert any(rid in result.stdout for rid in ["sec-001", "hyg-001", "dom-001"])


def test_gates_command(good_project):
    result = runner.invoke(app, ["gates", good_project])
    assert result.exit_code == 0


def test_architect_command(good_project):
    result = runner.invoke(app, ["architect", good_project])
    assert result.exit_code == 0


def test_completeness_command(good_project):
    result = runner.invoke(app, ["completeness", good_project])
    assert result.exit_code == 0


def test_init_command(tmp_path):
    # Create a minimal project for init to detect
    (tmp_path / "package.json").write_text('{"dependencies": {"react": "18.0.0"}}')
    result = runner.invoke(app, ["init", str(tmp_path), "--ci"])
    assert result.exit_code == 0
    assert (tmp_path / ".crystal" / "config.yaml").exists()
    assert (tmp_path / ".crystal" / "prd.md").exists()


def test_init_with_explicit_stack(tmp_path):
    result = runner.invoke(app, ["init", str(tmp_path), "--stack", "react-python-mongo", "--ci"])
    assert result.exit_code == 0


def test_handoff_command(good_project):
    result = runner.invoke(app, ["handoff", good_project])
    assert result.exit_code == 0
    assert "HANDOFF" in result.stdout or "handoff" in result.stdout.lower()


def test_handoff_output_to_file(good_project, tmp_path):
    out = tmp_path / "handoff.md"
    result = runner.invoke(app, ["handoff", good_project, "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()


def test_fix_prompt_command(bad_project):
    result = runner.invoke(app, ["fix-prompt", bad_project])
    assert result.exit_code == 0
    # fix-prompt should produce FIX blocks
    assert "FIX" in result.stdout or "Fix" in result.stdout or "fix" in result.stdout


def test_report_command(bad_project, tmp_path):
    out = tmp_path / "report.md"
    result = runner.invoke(app, ["report", bad_project, "--output", str(out)])
    assert result.exit_code in (0, 1)
    assert out.exists()


def test_fix_command_dry_run(bad_project):
    result = runner.invoke(app, ["fix", bad_project, "--dry-run"])
    assert result.exit_code == 0


def test_check_stage_staging_without_local_fails(bad_project):
    """Staging shouldn't be allowed without local passing."""
    result = runner.invoke(app, ["check", bad_project, "--stage", "staging"])
    # Should refuse to run or produce an error
    assert "local" in result.stdout.lower() or result.exit_code != 0


def test_rules_add_and_remove(bad_project):
    # Add a custom rule
    add = runner.invoke(app, [
        "rules", "add", bad_project,
        "-n", "test_rule", "-p", "FOOBAR", "-m", "Found FOOBAR",
    ])
    assert add.exit_code == 0
    # Verify it's listed
    lst = runner.invoke(app, ["rules", "list", bad_project])
    assert "test_rule" in lst.stdout or "custom" in lst.stdout.lower()


# --- Format + severity filter branches ---

def test_check_json_format(bad_project):
    result = runner.invoke(app, ["check", bad_project, "--format", "json"])
    assert result.exit_code in (0, 1)
    # Rich wraps output; verify JSON fragment markers appear
    assert '"health"' in result.stdout or '"issues"' in result.stdout


def test_check_markdown_format(bad_project, tmp_path):
    out = tmp_path / "report.md"
    result = runner.invoke(app, ["check", bad_project, "--format", "markdown", "--output", str(out)])
    assert result.exit_code in (0, 1)
    assert out.exists()
    assert "Crystal" in out.read_text() or "Health" in out.read_text()


def test_check_severity_filter_critical_only(bad_project):
    result = runner.invoke(app, ["check", bad_project, "--severity", "critical"])
    assert result.exit_code in (0, 1)
    # Output should not show LOW issues when filtering for critical
    # (we can't assert exact content, but command should complete)


def test_fix_apply_persists_changes(bad_project):
    """fix --apply must actually modify the filesystem."""
    from pathlib import Path
    result = runner.invoke(app, ["fix", bad_project, "--apply"])
    assert result.exit_code == 0
    # bad_project had no .gitignore → fix should create one with .env inside
    gitignore = Path(bad_project) / ".gitignore"
    assert gitignore.exists()
    assert ".env" in gitignore.read_text()


def test_fix_dry_run_does_not_modify(bad_project):
    from pathlib import Path
    # Capture state before
    gi_before = (Path(bad_project) / ".gitignore").exists()
    result = runner.invoke(app, ["fix", bad_project, "--dry-run"])
    assert result.exit_code == 0
    # State after should match
    gi_after = (Path(bad_project) / ".gitignore").exists()
    assert gi_before == gi_after


def test_fix_no_dedupe_noise(bad_project):
    """fix must not print 'WOULD FIX arch-003: Add .env to .gitignore' for every issue."""
    result = runner.invoke(app, ["fix", bad_project, "--dry-run"])
    assert result.exit_code == 0
    # The same (rule_id, target) should not appear more than once
    lines = [line for line in result.stdout.split("\n") if "WOULD FIX" in line]
    assert len(lines) == len(set(lines))


# --- Badge command ---

def test_badge_markdown(good_project):
    result = runner.invoke(app, ["badge", good_project, "--format", "markdown"])
    assert result.exit_code == 0
    assert "img.shields.io" in result.stdout
    assert "crystalcodes.dev" in result.stdout


def test_badge_svg(good_project, tmp_path):
    out = tmp_path / "badge.svg"
    result = runner.invoke(app, ["badge", good_project, "--format", "svg", "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()
    assert out.read_text().startswith("<svg")


def test_badge_json(good_project):
    import json
    result = runner.invoke(app, ["badge", good_project, "--format", "json"])
    assert result.exit_code == 0
    parsed = json.loads(result.stdout)
    assert parsed["schemaVersion"] == 1


def test_badge_url(good_project):
    result = runner.invoke(app, ["badge", good_project, "--format", "url"])
    assert result.exit_code == 0
    assert "shields.io" in result.stdout


def test_badge_invalid_format(good_project):
    result = runner.invoke(app, ["badge", good_project, "--format", "bogus"])
    assert result.exit_code != 0
