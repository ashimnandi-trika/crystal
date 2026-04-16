# Project Crystal — Executive Summary

## One-Liner
An open-source "building inspector" for vibe-coded projects — MCP servers + CI/CD gates that keep AI-generated code structurally sound, secure, and maintainable.

## The Problem (Validated by Data)
- **36%** of vibe coders skip QA entirely (arxiv, 2025)
- AI-generated code is **1.7x more likely** to have major logic errors
- **2.74x more prone** to security vulnerabilities vs human code
- **63%** of developers spend more time debugging AI code than writing it
- **45%** of AI-generated code contains security vulnerabilities
- After ~3 months, projects become "black boxes" — unmaintainable

Non-technical users on platforms like Cursor, Bolt, Lovable, Replit, and Emergent are building real apps with no guardrails. The code works today, breaks tomorrow.

## The Solution
Crystal provides **three layers of protection** that any vibe coder can install and use:

### Layer 1: MCP Guardian Server (During Coding)
An MCP server that AI coding assistants connect to. It watches the project in real-time and provides:
- Project structure validation ("you're putting business logic in a UI file")
- Domain boundary enforcement ("this database call shouldn't be in a React component")
- Session continuity ("here's what was built last session, here's what's remaining")
- Architecture blueprint compliance ("your project should follow this structure")

### Layer 2: Crystal CLI (Before Deploy)
A simple command-line tool that runs checks locally:
```
crystal check          # Run all checks
crystal init           # Initialize Crystal for a project
crystal status         # Show project health dashboard
```

### Layer 3: Crystal CI/CD (On Every Push)
GitHub Actions workflow that gates deployments:
- Architecture compliance check
- Security scan (hardcoded secrets, vulnerable patterns)
- Dependency audit (unknown/malicious packages)
- Placeholder detection (TODO, FIXME, example.com)
- Domain purity verification

## What Makes This Different

| Existing Tools | Crystal |
|---|---|
| Require coding knowledge to configure | Works with zero config for common stacks |
| Designed for professional developers | Designed for vibe coders (non-technical users) |
| Generic linting/security | Architecture + domain + session awareness |
| Separate disconnected tools | Unified MCP + CLI + CI/CD pipeline |
| No project context | Maintains project memory across sessions |

## Competitive Landscape
- **No existing MCP server** does architecture validation or project structure enforcement (confirmed via research, Jan 2026)
- Semgrep MCP exists for security scanning — not architecture
- SonarQube does quality gates — but requires developer expertise
- **Crystal fills a gap nobody has addressed yet**

## Target User
**Primary**: Non-technical person using a vibe coding platform (Cursor, Bolt, Lovable, Replit, Emergent, etc.) to build a real application. They don't understand code but want their app to not fall apart.

**Secondary**: Technical developers using AI coding assistants who want automated architectural guardrails.

## Tech Stack
- **MCP Servers**: Python (FastMCP)
- **CLI**: Python (Click or Typer)
- **CI/CD**: GitHub Actions (YAML)
- **Agent**: Python (uses MCP servers as tools)
- **Landing Page**: Static HTML/CSS/JS (or React for the Emergent deployment)

## Success Metrics
1. A non-coder can install Crystal in under 5 minutes
2. Crystal catches at least 80% of common vibe-coding structural issues
3. GitHub repo gets 100+ stars in first month (with proper marketing)
4. Works with at least 3 major vibe coding platforms
