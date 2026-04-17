# Crystal v0.3.0 — GitHub Release Notes

**Copy-paste this into GitHub → Releases → Draft a new release.**

**Tag**: `v0.3.0`
**Target**: `main`
**Title**: `v0.3.0 — Crystal Agent, Dependency Analyzer, 20 Quality Gates`

---

## 🎉 Crystal v0.3.0 is here

Crystal v0.3.0 is a major expansion: **AI-powered audit**, **dependency analysis**, **safe auto-fix**, and a **161-test suite** taking coverage to 82%. If you're shipping products with AI coding tools, this release is the one you've been waiting for.

```bash
pip install --upgrade crystal-code
```

---

## ✨ New Commands

- **`crystal audit [--llm]`** — Correlates issues across analyzers, identifies hotspots, and emits recommendations. `--llm` adds a natural-language senior-engineer review using Claude Sonnet 4.5, GPT, or the Emergent universal key.
- **`crystal completeness`** — Parses your PRD checklist and reports progress against actual implementation.
- **`crystal fix`** — Safe, whitelisted auto-fixes for filesystem/config issues. Never modifies source code. Dry-run by default, `--apply` to commit.
- **`crystal diff`** — Checks only files changed since your last git commit. Perfect for CI.
- **`crystal badge`** — Generates a shields.io-compatible health badge in markdown, SVG, JSON, or URL. Drop it in your README.
- **`crystal rules list | add | remove`** — Manage architecture rules directly from the CLI.

## 🛡️ New Gates

Crystal now runs **20 quality gates** (up from 15):

- **Dependency Analyzer** (3 new gates): `pip-audit` + `npm-audit` vulnerability scanning, unused dependency detection, duplicate-functionality detection (catches axios + node-fetch, moment + dayjs).
- **Stage-specific gates** (2 new): no localhost URLs at staging+, all env vars defined at staging+.

## 🤖 Crystal Agent

The new `CrystalAgent` brings AI-powered analysis as an optional layer:

- **Audit**: hotspot correlation across all 5 analyzers
- **Completeness**: PRD-vs-reality gap analysis
- **Refactor**: duplicate filename + oversized file detection
- LLM provider auto-detected: `ANTHROPIC_API_KEY` > `OPENAI_API_KEY` > `EMERGENT_LLM_KEY`

## 🐛 Critical Bug Fixes

- Fixed **inverted severity threshold** in scoring — `threshold=high` now correctly blocks critical+high (was reversed).
- Fixed **syntax error** in `pipeline.py` that broke all imports.
- Fixed **Jest/Vitest parser** reading `failed=0` on failing suites.
- Fixed **`crystal fix`** suggesting the same `.gitignore` patch for every issue regardless of rule type. Now dispatches per-rule with deduplication.
- Fixed **`crystal rules list`** crashing on nested f-string braces.
- Fixed **74 Ruff lint errors** blocking clean execution.

## 🧪 Test Suite

- **161 tests** across 16 test files
- **82% coverage** (excluding FastMCP server runtime)
- Full pytest + cov reporting: `pytest --cov=src/crystal_guard`

## 🏗️ Infrastructure Hardening

- Backend CORS restricted to known origins
- `/health` endpoint for liveness checks
- MongoDB connection wrapped in try/except
- Frontend: clipboard fallback for non-HTTPS contexts, async script loads

---

## Upgrade Path

```bash
# Upgrade
pip install --upgrade crystal-code

# Verify
crystal --version   # should show 0.3.0

# Run on your project
crystal check
crystal audit --llm      # optional AI insight
crystal badge --format markdown   # health badge for your README
```

## Breaking Changes

**None.** v0.3.0 is fully backward compatible with v0.2.0 configs.

## Full Changelog

See [CHANGELOG.md](https://github.com/ashimnandi-trika/crystal/blob/main/project-crystal/crystal-guard/CHANGELOG.md).

## Credits

Built by [@ashimnandi-trika](https://github.com/ashimnandi-trika) using [Emergent](https://emergent.sh).
Crystal's own `crystal audit --llm` dogfoods the Emergent universal LLM key — the tool uses the same AI substrate it protects.

---

**Try it now**: [crystalcodes.dev](https://crystalcodes.dev) · [PyPI](https://pypi.org/project/crystal-code/) · [Case Study](https://github.com/ashimnandi-trika/crystal/blob/main/project-crystal/crystal-guard/docs/CASE-STUDY-VIBECON.md)
