"""Tests for health scoring and severity threshold logic."""
from __future__ import annotations

from crystal_guard.analyzers import Issue, Severity
from crystal_guard.scoring import calculate_health


def mk(sev: str, analyzer: str = "security") -> Issue:
    return Issue(
        analyzer=analyzer,
        severity=sev,
        file="x.py",
        line=1,
        rule_id="r",
        message="m",
        suggestion="s",
    )


def test_perfect_score_no_issues():
    h = calculate_health([])
    assert h.score == 100
    assert h.grade == "A"
    assert h.passed is True


def test_critical_deducts_most_points():
    h = calculate_health([mk("critical")])
    assert h.score == 85
    assert h.critical_count == 1


def test_low_deducts_least_points():
    h = calculate_health([mk("low")])
    assert h.score == 98
    assert h.low_count == 1


def test_score_floors_at_zero():
    issues = [mk("critical") for _ in range(20)]
    h = calculate_health(issues)
    assert h.score == 0
    assert h.grade == "F"


def test_grade_boundaries():
    # Zero issues → A
    assert calculate_health([]).grade == "A"
    # 1 critical (-15 → 85) → B
    assert calculate_health([mk("critical")]).grade == "B"
    # 3 criticals (-45 → 55) → D
    assert calculate_health([mk("critical")] * 3).grade == "D"
    # 5 criticals (-75 → 25) → F
    assert calculate_health([mk("critical")] * 5).grade == "F"


def test_threshold_high_blocks_critical_and_high():
    """With threshold=high, CRITICAL and HIGH issues must block."""
    assert calculate_health([mk("critical")], threshold="high").passed is False
    assert calculate_health([mk("high")], threshold="high").passed is False
    assert calculate_health([mk("medium")], threshold="high").passed is True
    assert calculate_health([mk("low")], threshold="high").passed is True


def test_threshold_critical_only_blocks_critical():
    assert calculate_health([mk("critical")], threshold="critical").passed is False
    assert calculate_health([mk("high")], threshold="critical").passed is True
    assert calculate_health([mk("low")], threshold="critical").passed is True


def test_threshold_low_blocks_everything():
    """threshold=low means even LOW issues block (strictest stage)."""
    assert calculate_health([mk("low")], threshold="low").passed is False
    assert calculate_health([mk("medium")], threshold="low").passed is False
    assert calculate_health([mk("high")], threshold="low").passed is False


def test_top_issues_sorted_by_severity():
    issues = [mk("low"), mk("critical"), mk("medium"), mk("high")]
    h = calculate_health(issues)
    assert h.top_issues[0].severity == "critical"
    assert h.top_issues[1].severity == "high"


def test_breakdown_has_all_analyzers():
    h = calculate_health([mk("high", "security"), mk("high", "architecture")])
    assert set(h.breakdown.keys()) >= {"architecture", "domain", "security", "placeholders"}
    assert h.breakdown["security"] < 25
    assert h.breakdown["architecture"] < 30


def test_severity_points():
    assert Severity.CRITICAL.points == 15
    assert Severity.HIGH.points == 8
    assert Severity.MEDIUM.points == 4
    assert Severity.LOW.points == 2


def test_severity_rank_order():
    assert Severity.CRITICAL.rank < Severity.HIGH.rank < Severity.MEDIUM.rank < Severity.LOW.rank
