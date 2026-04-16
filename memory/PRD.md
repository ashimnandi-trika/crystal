# Project Crystal — PRD (Product Requirements Document)

## Date: January 2026
## Status: Phase 0 Complete

---

## Original Problem Statement
Build "Project Crystal" — an open-source project management tool for vibe coders and AI-assisted development. MCP servers and an agent with landing page and GitHub repo. Stack: Python for MCP and agent. Goal: help create project management, build architecture, maintain integrity, domain purity. CI/CD verification system with audit gates and checks. Should work with any vibe coding platform. Simple enough for non-coders, effective for real-world issues.

## User Persona
**Primary**: Non-technical person using vibe coding platforms (Cursor, Bolt, Lovable, Replit, Emergent) to build real apps. Doesn't understand code but wants quality.
**Secondary**: Technical developers using AI assistants who want automated guardrails.

## Core Requirements (Static)
1. MCP Guardian Server — real-time architecture guidance during AI coding sessions
2. CLI Tool — local checks before deployment (crystal init, check, status, fix, report)
3. CI/CD Gates — GitHub Actions workflow for automated quality verification
4. Session Memory — PRD tracking across coding sessions
5. Stack-aware rules — auto-detect and apply appropriate rules
6. Landing Page — informative showcase website
7. Open Source — MIT license, community-friendly

---

## What's Been Implemented (Phase 0)

### Strategic Documentation (Complete)
- Executive Summary (`00-EXECUTIVE-SUMMARY.md`)
- Problem Deep Dive with 7 core problems (`01-PROBLEM-DEEP-DIVE.md`)
- Architecture Overview with system diagrams (`02-ARCHITECTURE-OVERVIEW.md`)
- Phased Delivery Plan (5 phases) (`03-PHASED-DELIVERY-PLAN.md`)
- Detailed Component Specs for all 6 components (`04-COMPONENT-SPECS.md`)
- GitHub Repo Structure with pyproject.toml (`05-GITHUB-REPO-STRUCTURE.md`)
- Consistency & Quality Rules (`06-CONSISTENCY-RULES.md`)
- Strategic Recommendations & Launch Plan (`07-RECOMMENDATIONS.md`)
- Session Workflow & Platform Integration Guide (`08-SESSION-WORKFLOW.md`)
- Complete YAML Rules Specification (`specs/RULES-SPECIFICATION.md`)
- 10 Copy-Paste Build Prompts (`prompts/BUILD-PROMPTS.md`)

### Landing Page (Complete - Tested 98%)
- Hero with title, tagline, terminal preview
- Problem stats section (4 validated data points)
- Solution pillars (MCP, CLI, CI/CD)
- Quick Start terminal with copy button
- Features grid (6 cards)
- Use Cases (3 cards)
- Commands reference table (6 commands)
- Platform compatibility strip (8 platforms)
- Footer CTA
- Dark theme, Outfit/IBM Plex Sans/JetBrains Mono fonts
- Responsive design, scroll animations

---

## Prioritized Backlog

### P0 (Critical for Launch)
- [ ] **Phase 1**: Build Crystal Core + CLI (Python, Typer, PyYAML)
  - Stack detector, architecture analyzer, domain analyzer, security analyzer
  - Placeholder detector, health scorer, CLI commands
- [ ] **Phase 2**: Build Crystal MCP Server (FastMCP)
  - Expose tools, resources, prompts via MCP protocol
  - Platform configuration guides

### P1 (Important)
- [ ] **Phase 3**: Crystal CI/CD Gates (GitHub Actions)
  - Workflow YAML, PR comment integration
- [ ] GitHub repo setup with README, CONTRIBUTING, LICENSE
- [ ] PyPI package publication

### P2 (Nice to Have)
- [ ] **Phase 4**: Crystal Agent (AI-powered deep analysis)
- [ ] **Phase 5**: Polish & Launch (Product Hunt, marketing)
- [ ] Health badge for README
- [ ] Additional stack rules (Vue, Angular, Next.js, Django, Rails)
- [ ] VS Code extension

## Next Tasks
1. Start Phase 1: Build Crystal Core in Python — begin with stack detector and architecture analyzer
2. Set up GitHub repository with documented structure
3. Create test fixtures (good_project, bad_project, mixed_project)
