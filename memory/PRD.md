# Crystal (crystal-code) — PRD

## Date: February 2026
## Status: v0.3.0 — Agent + Dependency + Test Suite Complete

---

## What's Built

### 15 CLI Commands
| Command | What it does |
|---------|-------------|
| `crystal init` | Set up Crystal, auto-detect stack |
| `crystal check` | Run quality gates with `--stage local\|staging\|production` |
| `crystal status` | Health dashboard with trends |
| `crystal handoff` | Session handoff prompt generator |
| `crystal gates` | Show all quality gates individually |
| `crystal report` | Markdown report for PRs |
| `crystal architect` | Generate architecture.md |
| `crystal test` | Run actual tests (pytest/npm test) |
| `crystal fix-prompt` | Generate paste-ready AI prompts for every issue |
| `crystal fix` | Auto-fix simple issues (LOW/MEDIUM only) |
| `crystal diff` | Check only files changed since last git commit |
| `crystal audit` | Comprehensive AI-powered project audit |
| `crystal completeness` | Compare PRD checklist with actual implementation |
| `crystal mcp serve` | MCP server for AI assistants |
| `crystal rules list/add/remove` | Manage architecture rules |

### Pipeline: local → staging → production
- **Local**: gates lenient (fails on critical only)
- **Staging**: + env var validation, no localhost (fails on high)
- **Production**: + all tests must pass, zero tolerance (fails on medium)
- Stage progression enforced (can't skip stages)

### v0.3.0 Features (DONE — Feb 2026)
1. **Crystal Agent** (`agent.py`) — AI-powered audit, completeness, refactor. Optional LLM insight via `--llm` flag with priority: `ANTHROPIC_API_KEY` → `OPENAI_API_KEY` → `EMERGENT_LLM_KEY`.
2. **Dependency Analyzer** — pip-audit, npm-audit, unused deps (`dep-003`), duplicate functionality detection (`dep-004`).
3. **New CLI commands**: `diff`, `fix`, `audit`, `completeness`, `rules list/add/remove`.
4. **Enhanced handoff** — session summary, test regression detection.
5. **Critical bug fixes**:
   - Fixed inverted severity threshold logic in scoring.
   - Fixed pipeline.py docstring syntax error (blocked imports).
   - Fixed Jest/Vitest parser (was reading 0 failed when non-zero).
6. **Comprehensive unit test suite** — 132 tests, 80% coverage.
7. **Backend/frontend production hardening**: CORS restricted, pagination, health endpoint, clipboard fallback, async scripts, MongoDB error handling.

### Unit Test Suite (NEW)
- `tests/test_architecture.py` — 4 tests
- `tests/test_domain.py` — 3 tests
- `tests/test_security.py` — 7 tests
- `tests/test_placeholders.py` — 6 tests
- `tests/test_dependencies.py` — 7 tests
- `tests/test_scoring.py` — 12 tests (incl. all threshold edge cases)
- `tests/test_config.py` — 8 tests
- `tests/test_pipeline.py` — 13 tests (stage progression, staging, production)
- `tests/test_handoff.py` — 7 tests
- `tests/test_agent.py` — 9 tests (LLM provider detection, audit, completeness, refactor)
- `tests/test_cli.py` — 19 tests (all commands smoke-tested via Typer CliRunner)
- `tests/test_misc.py` — 16 tests (detector, debt, baseline)
- `tests/test_fix_prompt.py` — 6 tests
- `tests/test_reporters.py` — 4 tests
- `tests/test_test_runner.py` — 11 tests
- **Coverage: 80% overall** (excluding MCP server which needs live runtime)

### Previously Built
- 15+ quality gates (architecture, domain, security, hygiene, dependencies)
- MCP Server (tools + resources + prompts via FastMCP)
- Baseline tracking, debt tracker, session handoff
- 5 stack rule sets (react_python_mongo, nextjs_prisma, vue_node_express, python_django, generic)
- architecture.md generation
- Design masterpiece landing page with full SEO
- PyPI package `crystal-code` (v0.2.0 published; v0.3.0 ready)

---

## P0 Backlog
- **Publish v0.3.0 to PyPI** (needs user's project-scoped PyPI token).
- **Verify all URLs in README/CHANGELOG** use `crystalcodes.dev`.

## P1 Backlog
- Write descriptive Git commit messages for all "Save to Github" pushes (user complained about UUID auto-commits).
- `crystal fix` currently suggests the same fix ("Add .env to .gitignore") for many issue types — needs per-rule fix templates.
- Add CHANGELOG.md entry for v0.3.0.

## P2 / Future
- MCP server integration tests (requires FastMCP harness).
- Increase detector coverage (Ruby, Swift, Kotlin).
- Stack-specific rule packs for more frameworks.
- Web dashboard for multi-project monitoring.

---

## Architecture
```
/app/project-crystal/crystal-guard/
├── pyproject.toml              # crystal-code v0.3.0
├── src/crystal_guard/
│   ├── cli.py                  # 15 commands (Typer)
│   ├── agent.py                # CrystalAgent (audit/completeness/refactor)
│   ├── pipeline.py             # stage-aware checking
│   ├── handoff.py              # session handoff generator
│   ├── baseline.py, debt.py    # trend tracking
│   ├── detector.py             # stack auto-detection
│   ├── test_runner.py          # pytest/jest/vitest wrapper
│   ├── fix_prompt.py           # paste-ready AI fix prompts
│   ├── analyzers/              # architecture, domain, security, placeholders, dependencies
│   ├── rules/                  # YAML rule packs
│   ├── scoring/                # health + grade
│   ├── reporters/              # terminal, markdown, json
│   └── mcp/                    # FastMCP server
└── tests/                      # 132 tests, 80% coverage
    ├── conftest.py             # good_project / bad_project / mixed_project fixtures
    └── fixtures/
```

## LLM Integration
- `crystal audit --llm` enables LLM insight.
- Priority: `ANTHROPIC_API_KEY` > `OPENAI_API_KEY` > `EMERGENT_LLM_KEY`.
- Default model: `claude-sonnet-4-5-20250929` (emergent/anthropic), `gpt-5.1` (openai).
- Uses `emergentintegrations` library for Emergent Universal key.
- Without `--llm`, audit is fully rule-based (works offline, zero cost).
