# Changelog

All notable changes to Crystal will be documented in this file.

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
