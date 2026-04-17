"""Tests for fix prompt generation and markdown reporters."""
from __future__ import annotations

from crystal_guard.analyzers import Issue
from crystal_guard.fix_prompt import generate_all_fix_prompts, generate_fix_prompt


def mk(rule_id="sec-001", sev="critical") -> Issue:
    return Issue(
        analyzer="security", severity=sev, file="app.py", line=42,
        rule_id=rule_id, message="API key leaked", suggestion="Move to .env",
    )


def test_fix_prompt_includes_location():
    out = generate_fix_prompt(mk())
    assert "app.py" in out
    assert "42" in out


def test_fix_prompt_uses_why_explanation():
    out = generate_fix_prompt(mk("sec-001"))
    # sec-001 has a canned WHY explanation
    assert "API key" in out


def test_fix_prompt_falls_back_to_issue_why():
    issue = Issue(
        analyzer="x", severity="low", file="f", line=1, rule_id="zz-999",
        message="m", suggestion="s", why="custom reason",
    )
    out = generate_fix_prompt(issue)
    assert "custom reason" in out


def test_generate_all_empty():
    assert "No issues" in generate_all_fix_prompts([])


def test_generate_all_orders_by_severity():
    issues = [mk("hyg-001", "low"), mk("sec-001", "critical"), mk("sec-005", "high")]
    out = generate_all_fix_prompts(issues)
    # Critical should appear before HIGH which should appear before LOW
    crit_pos = out.find("CRITICAL")
    high_pos = out.find("HIGH")
    low_pos = out.find("LOW")
    assert crit_pos < high_pos < low_pos


def test_generate_all_includes_project_context():
    ctx = "My React project"
    out = generate_all_fix_prompts([mk()], project_context=ctx)
    assert "React project" in out
