"""Tests for CrystalAgent (audit, completeness, refactor)."""
from __future__ import annotations

from crystal_guard.agent import CrystalAgent


def test_agent_audit_runs(bad_project):
    agent = CrystalAgent(bad_project, use_llm=False)
    report = agent.audit()
    assert "Crystal Audit Report" in report
    assert "Health" in report


def test_agent_audit_no_llm_by_default(bad_project):
    agent = CrystalAgent(bad_project, use_llm=False)
    assert agent.llm_key is None
    assert agent.llm_provider is None


def test_agent_respects_opt_out(bad_project, monkeypatch):
    monkeypatch.setenv("EMERGENT_LLM_KEY", "fake")
    agent = CrystalAgent(bad_project, use_llm=False)
    assert agent.llm_provider is None


def test_agent_detects_emergent_key(bad_project, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("EMERGENT_LLM_KEY", "sk-emergent-test")
    agent = CrystalAgent(bad_project, use_llm=True)
    assert agent.llm_provider == "emergent"
    assert agent.llm_key == "sk-emergent-test"


def test_agent_prefers_anthropic_over_emergent(bad_project, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "ant-key")
    monkeypatch.setenv("EMERGENT_LLM_KEY", "emg-key")
    agent = CrystalAgent(bad_project, use_llm=True)
    assert agent.llm_provider == "anthropic"


def test_agent_completeness_without_prd(tmp_path):
    agent = CrystalAgent(str(tmp_path), use_llm=False)
    result = agent.completeness()
    assert "No PRD" in result


def test_agent_completeness_with_prd(good_project):
    # good_project already has a PRD
    agent = CrystalAgent(good_project, use_llm=False)
    result = agent.completeness()
    assert "Completeness" in result or "Metrics" in result


def test_agent_refactor(good_project):
    agent = CrystalAgent(good_project, use_llm=False)
    result = agent.refactor()
    assert "Refactoring" in result


def test_agent_audit_includes_hotspots(bad_project):
    agent = CrystalAgent(bad_project, use_llm=False)
    report = agent.audit()
    # bad_project has issues clustered in server.py and App.jsx
    assert "server.py" in report or "App.jsx" in report
