# Changelog

All notable changes to Crystal will be documented in this file.

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
