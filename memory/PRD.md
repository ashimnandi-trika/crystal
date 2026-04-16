# Crystal — PRD

## Date: January 2026
## Status: Foundation Complete — 3 Critical Gaps Identified

---

## What's Built (70% of FAANG-grade vision)
- 8 CLI commands (init, check, status, handoff, gates, report, architect, mcp serve)
- 15 quality gates across 4 analyzers
- MCP Server (8 tools + 3 resources via FastMCP)
- Baseline tracking, debt tracker, session handoff
- 5 stack rule sets, 3 documentation guides
- Landing page (design masterpiece, full SEO)
- PyPI package ready (twine checked)

## What's Missing (30% — the difference between useful and FAANG-grade)

### CRITICAL (Sprint 1)
1. **crystal test** — Run actual tests (pytest/npm test), not just check if files exist
2. **crystal fix-prompt** — Generate paste-ready AI prompts for every issue with WHY + HOW
3. **--stage local|staging|production** — Escalating strictness pipeline

### HIGH (Sprint 2)
4. WHY explanations on every gate (plain English for non-coders)
5. Auto session summary ("this session you added 5 files, fixed 2 issues")
6. Env var validator (check all referenced vars exist)
7. Next session priorities in handoff

### MEDIUM (Sprint 3)
8. Test regression detection ("test X disappeared")
9. Batch fix prompts (one doc, all fixes, priority order)
10. Production checklist (SSL, monitoring, backups)

## Pipeline Vision
```
Local → Staging → Production
(lenient)  (strict)  (zero tolerance)

Each stage: check → if fail: fix-prompt → fix → re-check → proceed
```

## Next Build Session
Build Sprint 1: crystal test, crystal fix-prompt, --stage flag
Follow prompts in /app/project-crystal/prompts/SPRINT-1-PROMPTS.md
