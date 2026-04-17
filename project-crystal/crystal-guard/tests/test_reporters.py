"""Tests for markdown + json reporters."""
from __future__ import annotations

import json

from crystal_guard.analyzers import Issue
from crystal_guard.config import CrystalConfig
from crystal_guard.reporters.markdown import generate_markdown_report
from crystal_guard.reporters.json_reporter import generate_json_report
from crystal_guard.scoring import calculate_health


def mk(sev="high"):
    return Issue(
        analyzer="security", severity=sev, file="x.py", line=10,
        rule_id="sec-001", message="leaked", suggestion="fix",
    )


def test_markdown_report_passing():
    h = calculate_health([])
    md = generate_markdown_report(h, [], config=CrystalConfig(project_name="X", stack="generic"))
    assert "Crystal Guard" in md
    assert "passed" in md.lower() or "A" in md


def test_markdown_report_failing():
    issues = [mk("critical")]
    h = calculate_health(issues)
    md = generate_markdown_report(h, issues, config=CrystalConfig(project_name="X"))
    assert "FAILED" in md
    assert "sec-001" in md


def test_markdown_groups_by_severity():
    issues = [mk("critical"), mk("high"), mk("medium"), mk("low")]
    h = calculate_health(issues)
    md = generate_markdown_report(h, issues)
    # All 4 severity headers
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        assert sev in md


def test_json_reporter_serializable():
    issues = [mk("high")]
    h = calculate_health(issues)
    out = generate_json_report(h, issues)
    parsed = json.loads(out)
    assert "health" in parsed
    assert parsed["health"]["grade"] in "ABCDF"
    assert parsed["passed"] is False
    assert len(parsed["issues"]) == 1
