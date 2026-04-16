# Crystal — PRD

## Date: January 2026
## Status: Phase 2 Complete

---

## Original Problem Statement
Build "Project Crystal" — open-source tool for vibe coders. MCP servers, agent, landing page, GitHub repo. Python stack. Maintain architecture integrity, domain purity, session continuity. CI/CD verification with audit gates. Platform-agnostic. Simple for non-coders. Renamed from "Crystal Guard" to just "Crystal".

## Branding
- **Name**: Crystal
- **Tagline**: "Your AI coding buddy that protects architecture integrity and domain purity"
- **Sub-tagline**: "So your project ships clean. Every time."

## User Persona
**Primary**: Non-technical person using vibe coding platforms to build real apps.
**Secondary**: Technical developers using AI assistants wanting automated guardrails.

## The 7 Core Features
1. **Session Prompt Generator** — reads git, files, tests; generates paste-ready prompt
2. **15 Quality Gates** — architecture, domain, security, hygiene checks
3. **Baseline Tracking** — tracks metrics across sessions, flags regressions
4. **Session Handoff** — generates handoff doc that works across platforms
5. **MCP Tools** — AI assistant accesses quality tools while coding (LIVE)
6. **Architecture Rules** — architecture.md generated and enforced
7. **Technical Debt Tracker** — logs failures across sessions, shows trends

---

## What's Been Implemented

### Phase 0 — Strategy & Documentation (Complete)
- 11 strategic documents, 10 build prompts, YAML rules spec

### Phase 1 — Crystal Core + CLI (Complete, 100%)
- 4 analyzers implementing 15 quality gates
- Health scoring (A-F), baseline tracking, debt tracker
- Session handoff generator
- 3 reporters (terminal/JSON/markdown), 2 rule sets
- 6 CLI commands: init, check, status, handoff, gates, report

### Phase 2 — MCP Server + Architect + Branding (Complete, 100%)
- **FastMCP Server** (`crystal mcp serve`): 8 tools + 3 resources
  - Tools: check_architecture, check_domain_purity, check_security, run_all_checks, validate_file_placement, get_project_context, get_health_score, update_prd
  - Resources: crystal://health, crystal://rules, crystal://prd
  - Transports: stdio (Cursor/Claude) and HTTP
- **`crystal architect`**: Generates architecture.md with stack info, rules, session instructions
- **Branding**: Renamed to "Crystal", simplified all copy for non-technical users
- **Landing Page**: Complete rewrite with simplified language
  - "Picks Up Where You Left Off", "15 Automatic Checks", "Tracks Your Progress"
  - "Build with AI. Ship with Crystal."
- **8 CLI Commands**: init, check, status, handoff, gates, report, architect, mcp serve

### Repo Structure: `/app/project-crystal/crystal-guard/`
```
src/crystal_guard/
  __init__.py, cli.py, config.py, detector.py
  architect.py, baseline.py, debt.py, handoff.py
  analyzers/ (architecture, domain, security, placeholders)
  scoring/ (health)
  reporters/ (terminal, json, markdown)
  rules/ (loader + builtin YAML)
  mcp/ (server.py — FastMCP)
```

---

## Prioritized Backlog

### P0
- [ ] Publish to PyPI (`pip install crystal-guard` from real PyPI)
- [ ] Test MCP server with Cursor and Claude Desktop
- [ ] Test GitHub Actions workflow on real repo

### P1
- [ ] More stack rules (Next.js, Vue, Django, Rails, Go)
- [ ] `crystal fix --dry-run` auto-fix command
- [ ] Comprehensive test suite (pytest)

### P2
- [ ] Crystal Agent (AI-powered deep analysis)
- [ ] Health badge for README
- [ ] VS Code extension
- [ ] Product Hunt / HN launch

## Next Tasks
1. Publish to PyPI (prepare MANIFEST.in, verify package)
2. Test MCP with real Cursor/Claude Desktop
3. Test CI/CD on real GitHub repo
4. Add more stack rule sets
