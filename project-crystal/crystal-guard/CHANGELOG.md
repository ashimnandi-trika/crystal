# Changelog

All notable changes to Crystal will be documented in this file.

## [0.3.0] - 2026-02

### Added
- **Crystal Agent** (`agent.py`): `crystal audit [--llm]` correlates issues
  across analyzers, identifies hotspots, and emits recommendations.
  `--llm` adds a natural-language insight section. Provider auto-detected:
  `ANTHROPIC_API_KEY` > `OPENAI_API_KEY` > `EMERGENT_LLM_KEY`.
- `crystal completeness` — parses PRD checklist items and reports progress
  against current project metrics.
- **Dependency Analyzer** (`analyzers/dependencies.py`) — pip-audit / npm-audit
  integration (`dep-001`), unused Python deps (`dep-003`), duplicate-
  functionality packages like axios+node-fetch (`dep-004`).
- `crystal diff` — checks only files changed since last git commit.
- `crystal fix` — per-rule auto-fixers (`fixers.py`) for `arch-001`,
  `arch-002`, `arch-003`, `arch-006`, `arch-007`, `sec-004`. Idempotent,
  never modifies source code, deduped by `(rule_id, target)`.
- `crystal rules list | add | remove` — manage architecture rules from CLI.
- `crystal badge` — generates shields.io-compatible Crystal health badge
  (markdown / svg / json / url) linking back to crystalcodes.dev.
- Session handoff enhancements (`handoff.py`) — "this session" summary
  line and test-regression detection.
- MCP prompts (`crystal-review`, `crystal-plan`) and
  `crystal://session-log` resource.
- **Unit test suite** (`tests/`) — 161 tests, 82% coverage.

### Fixed
- **Critical**: inverted severity threshold in `scoring/__init__.py`;
  `threshold=high` now correctly blocks critical+high (not the reverse).
- **Critical**: syntax error in `pipeline.py` (mangled docstring) that
  blocked all imports of the CLI.
- **High**: `test_runner.py` was passing `env=None` to `subprocess.run`,
  wiping the system PATH on some platforms.
- **High**: Jest/Vitest parser was reading `failed=0` on failing suites
  because the "Tests:" prefix broke the first comma segment's int-parse.
- **Medium**: `crystal fix` was suggesting "Add .env to .gitignore" for
  every single issue regardless of rule type. Now dispatches per-rule
  via a safe whitelist and deduplicates outputs.
- `crystal rules list` crashed with f-string syntax error on nested braces.
- Backend hardening (`server.py`): CORS restricted to `localhost:3000`,
  paginated `/api/status`, `/health` endpoint, MongoDB try/except, pinned
  `requirements.txt`.
- Frontend: clipboard fallback for non-HTTPS contexts, async script loads,
  `use-toast` delay fixed, GitHub URL corrected.
- `.gitignore` deduplicated.
- 74 Ruff lint errors cleaned up across `agent.py`, `cli.py`, `handoff.py`.

### Changed
- `CrystalAgent.__init__(use_llm=True/False)` for opt-in LLM usage.
- `crystal fix` now ignores severity and relies on the explicit
  `AUTO_FIXERS` whitelist — so it can auto-fix CRITICAL `sec-004`
  (env-not-in-gitignore), which is always safe.
- `pyproject.toml`: added `[tool.ruff]` (excludes test fixtures),
  `[tool.pytest.ini_options]` with `pythonpath = ["src"]`,
  `[tool.coverage.run]` omitting the MCP server module.

## [0.2.0] - 2026-01-16

### Added
- `crystal test` — runs actual test suites (pytest, npm test), not just checks if files exist
- `crystal fix-prompt` — generates paste-ready AI prompts with WHY explanations for every issue
- `--stage local|staging|production` flag on `crystal check` — escalating strictness pipeline
- Stage progression enforcement (staging requires local pass, production requires staging pass)
- Staging-specific gates: localhost URL detection, env var validation
- Production-specific gates: all tests must pass
- Config ignore patterns now properly filter scan results (fnmatch support)
- Real case study with reproducible project files in examples/case-study/

### Fixed
- `is_ignored()` now respects config ignore file patterns (was only using hardcoded list)
- 14 unused imports removed across 6 modules
- 4 unused variables removed
- 16 style violations fixed (one-liner try/except rewritten)
- Case study docs no longer contain literal secret values
- Full ruff lint pass: 0 errors

### Changed
- Total CLI commands: 10 (was 8)
- `run_all_analyzers()` now filters issues from ignored directories

## [0.1.0] - 2026-01-15

### Added
- Initial release
- 10 CLI commands: init, check, test, fix-prompt, status, handoff, gates, report, architect, mcp serve
- 15 quality gates across 4 analyzers (architecture, domain purity, security, code hygiene)
- Stage-aware pipeline: local, staging, production with escalating strictness
- Test runner: auto-detects and runs pytest / npm test
- Fix prompt generator: paste-ready AI prompts with WHY explanations for every issue
- Session handoff: structured prompt for next AI coding session
- Baseline tracking: cross-session metric snapshots with regression detection
- Technical debt tracker: recurring issue logging with trend analysis
- MCP server: 8 tools + 3 resources via FastMCP (stdio and HTTP transport)
- Architecture rules generator: crystal architect command
- 5 built-in stack rule sets: React+Python+MongoDB, Next.js+Prisma, Vue+Node, Django, Generic
- Health scoring: A-F grades with weighted severity scoring
- 3 output formats: terminal (Rich), JSON (CI/CD), Markdown (PR comments)
- GitHub Actions workflow template
- Full documentation: README, CONTRIBUTING, MCP-SETUP, CI-CD-SETUP, PUBLISHING
