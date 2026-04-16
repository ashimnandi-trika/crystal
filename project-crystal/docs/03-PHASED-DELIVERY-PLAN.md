# Phased Delivery Plan

## Philosophy
Build the simplest thing that solves a real problem first. Ship it. Get feedback. Iterate.

Each phase is a self-contained deliverable — if we stop at any phase, what's built is still useful.

---

## Phase 0: Foundation (This Session)
**Goal**: Organize, strategize, document everything so building is systematic
**Deliverables**:
- [x] Executive Summary
- [x] Problem Deep Dive
- [x] Architecture Overview
- [x] Phased Delivery Plan (this document)
- [x] Component Specs (detailed specs for each component)
- [x] Build Prompts (copy-paste prompts for AI-assisted building)
- [x] Landing Page Design Spec
- [x] GitHub Repo Structure
- [ ] Landing Page (basic informative site)

**Status**: IN PROGRESS

---

## Phase 1: Crystal Core + CLI (MVP)
**Goal**: A working CLI tool that anyone can install and run
**Timeline**: 1-2 sessions
**Deliverables**:
- Stack auto-detection (React, Python, Node, etc.)
- Architecture check (file structure validation)
- Domain purity check (forbidden patterns per layer)
- Security scan (hardcoded secrets, common vulnerabilities)
- Placeholder detection (TODO, FIXME, example.com)
- Health score (A-F grade with plain-English explanations)
- `crystal init` / `crystal check` / `crystal status` commands

**User Story**: "I run `pip install crystal-guard && crystal init && crystal check` and I get a report telling me what's wrong with my project in plain English."

**What's NOT included**: MCP server, CI/CD, agent

---

## Phase 2: Crystal MCP Server
**Goal**: AI assistants can connect to Crystal for real-time guidance
**Timeline**: 1 session
**Deliverables**:
- FastMCP server exposing Crystal Core as MCP tools
- Tools: check_architecture, check_domain, get_context, validate_file, get_health
- Resources: crystal://prd, crystal://rules, crystal://health
- Prompts: crystal-review, crystal-plan
- Configuration guide for Cursor, Windsurf, Claude Desktop

**User Story**: "I add Crystal MCP to my Cursor config and now my AI assistant knows about my project's architecture rules."

**What's NOT included**: CI/CD, agent

---

## Phase 3: Crystal CI/CD Gates
**Goal**: Automated quality gates on GitHub
**Timeline**: 1 session
**Deliverables**:
- GitHub Actions workflow file (crystal.yml)
- Runs Crystal CLI checks on every PR/push to main
- Configurable pass/fail thresholds
- Clear markdown report as PR comment
- Setup documentation

**User Story**: "I copy one YAML file to my repo and now every push gets checked before it can be merged."

**What's NOT included**: Agent

---

## Phase 4: Crystal Agent
**Goal**: Deeper AI-powered analysis using MCP servers
**Timeline**: 1 session
**Deliverables**:
- Python agent using MCP client
- Comprehensive project audit
- Multi-step analysis (feature completeness, consistency check)
- Detailed report generation
- Works with OpenAI/Anthropic/local LLMs

**User Story**: "I run `crystal audit` and get a detailed report about my project's health, completeness, and recommendations."

---

## Phase 5: Polish & Launch
**Goal**: Production-ready open-source release
**Timeline**: 1-2 sessions
**Deliverables**:
- Comprehensive README with GIFs/screenshots
- PyPI package (pip install crystal-guard)
- MCP marketplace listing
- Landing page with documentation
- Example projects showing Crystal in action
- Contributing guide
- Launch on Product Hunt / Hacker News / Reddit

---

## What We DON'T Build (Scope Boundaries)
- Crystal does NOT generate code (that's the AI platform's job)
- Crystal does NOT manage deployments (that's the platform's job)
- Crystal does NOT replace testing frameworks (it checks structure, not logic)
- Crystal does NOT require a database or cloud service (fully local)
- Crystal does NOT require coding knowledge to use (plain-English output)
