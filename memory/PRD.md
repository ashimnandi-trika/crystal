# Project Crystal — PRD

## Date: January 2026
## Status: Phase 1 Complete

---

## Original Problem Statement
Build "Project Crystal" — an open-source project management tool for vibe coders. MCP servers and agent with landing page. Python stack. Help maintain architecture integrity, domain purity, session continuity. CI/CD verification with audit gates. Platform-agnostic. Simple for non-coders, effective for real issues.

## User Persona
**Primary**: Non-technical person using vibe coding platforms to build real apps.
**Secondary**: Technical developers using AI assistants who want automated guardrails.

## Core Requirements — The 7 Features
1. **Session Prompt Generator** — reads git, files, tests; generates structured prompt for next AI session
2. **Quality Gates** — 15 automated checks (architecture, domain, security, hygiene)
3. **Baseline Tracking** — tracks file count, test count, endpoints, violations across sessions
4. **Session Handoff** — generates handoff document with what was built/changed/next
5. **MCP Tools** — AI assistant gets direct access to quality tools during coding
6. **Architecture Rules** — rules file that survives session resets and platform switches
7. **Technical Debt Tracker** — logs every failure across sessions, shows where debt grows

---

## What's Been Implemented

### Phase 0 — Strategy & Landing Page (Complete)
- 11 strategic documents in `/app/project-crystal/docs/`
- 10 build prompts in `/app/project-crystal/prompts/`
- YAML rules specification
- Landing page (React) — hero, stats, pillars, quick start, features, commands, footer

### Phase 1 — Crystal Guard Python CLI (Complete, tested 98%)
- **Package**: `/app/project-crystal/crystal-guard/` — installable via `pip install -e .`
- **Stack Detector**: Auto-detects React, Next.js, Python, Node, MongoDB, PostgreSQL
- **4 Analyzers** implementing 15 quality gates:
  - `architecture.py` — gates 1-4 (dirs, files, sprawl, nesting)
  - `domain.py` — gates 5-7 (DB in frontend, env vars, crypto in frontend)
  - `security.py` — gates 8-11 (API keys, passwords, key formats, .env exposure)
  - `placeholders.py` — gates 12-15 (TODO, placeholders, debug logs, localhost)
- **Health Scoring**: A-F grades, 100-point system, weighted by severity
- **Baseline Tracking**: `.crystal/baseline.json` — cross-session metric snapshots
- **Technical Debt Tracker**: `.crystal/debt.json` — recurring issue accumulation
- **Session Handoff Generator**: `crystal handoff` — structured prompt with git state, metrics, gates, debt, PRD
- **3 Reporters**: Terminal (Rich), JSON (CI/CD), Markdown (PR comments)
- **2 Rule Sets**: react-python-mongo, generic (YAML, extensible)
- **6 CLI Commands**: init, check, status, handoff, gates, report
- **GitHub Actions Workflow**: `.github/workflows/crystal.yml`
- **Test Fixtures**: good_project (A/100), bad_project (F/0)
- **README.md**, **LICENSE** (MIT)

### Landing Page Updates
- Updated features section to show all 7 features
- Updated commands table with handoff and gates
- Updated hero terminal preview

---

## Prioritized Backlog

### P0 (Next Session)
- [ ] **Phase 2**: Build Crystal MCP Server (FastMCP)
  - Expose analyzers as MCP tools
  - crystal://prd, crystal://rules, crystal://health resources
  - Platform config guides (Cursor, Claude Desktop, VS Code)
- [ ] `crystal architect` command — generate architecture.md from rules

### P1
- [ ] **Phase 3**: CI/CD Integration
  - Test the GitHub Actions workflow on a real repo
  - PR comment integration
- [ ] PyPI package publication (`pip install crystal-guard` from PyPI)
- [ ] More stack rules (Next.js, Vue, Django, Rails)

### P2
- [ ] **Phase 4**: Crystal Agent (AI-powered deep analysis)
- [ ] `crystal fix --dry-run` auto-fix command
- [ ] Health badge for README (shield.io style)
- [ ] VS Code extension
- [ ] Product Hunt / HN launch

## Next Tasks
1. Build MCP server (Phase 2) — expose all tools via FastMCP
2. Publish to PyPI for real `pip install crystal-guard`
3. Create `crystal architect` command
4. Test CI/CD workflow on real GitHub repo
