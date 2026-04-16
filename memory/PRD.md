# Crystal — PRD

## Date: January 2026
## Status: Phase 3 Complete — Design Masterpiece + PyPI + Stack Rules

---

## Branding
- **Name**: Crystal
- **Line 1**: Crystal (massive hero text)
- **Line 2**: Clean code that ships. (bold punch line)
- **Line 3**: Your AI coding buddy that protects architecture integrity and domain purity.

## What's Been Implemented (Cumulative)

### Phase 0 — Strategy & Documentation
- 11 strategic documents, 10 build prompts, YAML rules spec

### Phase 1 — Crystal Core + CLI
- 4 analyzers (15 quality gates), health scoring, baseline tracking
- Debt tracker, session handoff generator, 3 reporters
- 6 CLI commands: init, check, status, handoff, gates, report

### Phase 2 — MCP Server + Architect
- FastMCP server (8 tools + 3 resources, stdio/HTTP)
- `crystal architect` command (generates architecture.md)
- Rebranded to "Crystal"

### Phase 3 — Design Masterpiece + PyPI + Stack Rules (CURRENT)
- **Landing page redesign**: Picasso-precise typography hierarchy
  - Hero: Crystal (160px) -> Clean code that ships (44px) -> descriptor (21px)
  - Authentic terminal windows with macOS dots and glow effect
  - card-lift hover animations, stat-line top borders, generous spacing
  - Every text readable, nothing wimpy
- **SEO**: Full meta tags (OG, Twitter Cards, keywords, description, robots)
- **PyPI ready**: `python -m build` produces .whl + .tar.gz with all YAML rules
- **5 stack rule sets**: react-python-mongo, generic, nextjs-prisma, vue-node-express, python-django
- **Dog-fooding**: Crystal checks itself at A (100/100)
- **8 CLI commands**: init, check, status, handoff, gates, report, architect, mcp serve

### Architecture: `/app/project-crystal/crystal-guard/`
```
src/crystal_guard/
  cli.py, config.py, detector.py, architect.py
  baseline.py, debt.py, handoff.py
  analyzers/ (architecture, domain, security, placeholders)
  scoring/
  reporters/ (terminal, json, markdown)
  rules/builtin/ (5 YAML files)
  mcp/server.py (FastMCP)
```

---

## Prioritized Backlog

### P0
- [ ] Publish to PyPI (need PyPI account + `twine upload dist/*`)
- [ ] Deploy to custom domain with real SEO
- [ ] Test MCP with Cursor / Claude Desktop
- [ ] Test GitHub Actions on real repo

### P1
- [ ] More stack rules (Rails, Go, Rust)
- [ ] `crystal fix --dry-run` auto-fix
- [ ] Comprehensive pytest test suite
- [ ] `crystal onboard` interactive wizard

### P2
- [ ] Crystal Agent (AI-powered deep analysis)
- [ ] Health badge for README
- [ ] VS Code extension
- [ ] Product Hunt / HN launch
