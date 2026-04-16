# Crystal — PRD

## Date: January 2026
## Status: Sprint 1 Complete — All Critical Gaps Closed

---

## What's Built (100% of core vision)

### 10 CLI Commands
| Command | What it does |
|---------|-------------|
| `crystal init` | Set up Crystal, auto-detect stack |
| `crystal check` | Run quality gates with `--stage local\|staging\|production` |
| `crystal test` | Run actual tests (pytest/npm test) |
| `crystal fix-prompt` | Generate paste-ready AI prompts for every issue |
| `crystal status` | Health dashboard with trends |
| `crystal handoff` | Session handoff prompt generator |
| `crystal gates` | Show all 15 gates individually |
| `crystal report` | Markdown report for PRs |
| `crystal architect` | Generate architecture.md |
| `crystal mcp serve` | MCP server for AI assistants |

### Pipeline: local → staging → production
- **Local**: 15 gates, lenient (fail on critical only)
- **Staging**: + env var validation, no localhost, CORS check (fail on high)
- **Production**: + all tests must pass, zero tolerance (fail on medium)
- Stage progression enforced (can't skip stages)

### Sprint 1 Features (DONE)
1. `crystal test` — detects and runs pytest/npm test, parses results
2. `crystal fix-prompt` — WHY explanations for every rule, paste-ready prompts
3. `--stage` flag — escalating strictness pipeline

### Previously Built
- 15 quality gates (architecture, domain, security, hygiene)
- MCP Server (8 tools + 3 resources via FastMCP)
- Baseline tracking, debt tracker, session handoff
- 5 stack rule sets, architecture.md generation
- Design masterpiece landing page with full SEO
- PyPI package ready (twine checked)

## Next Steps (User Actions)
1. **PyPI publish**: `cd crystal-guard && twine upload dist/*`
2. **GitHub**: Push repo, enable Actions
3. **Domain**: Deploy landing page to custom domain
4. **Test MCP**: Connect Cursor/Claude Desktop
