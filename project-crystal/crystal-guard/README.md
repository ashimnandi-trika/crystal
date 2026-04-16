# Crystal Guard

**Architecture guardian for vibe-coded projects.**

MCP servers + CLI + CI/CD gates that keep AI-generated code structurally sound, secure, and maintainable.

```
pip install crystal-code
crystal init
crystal check
```

---

## What is Crystal Guard?

Every vibe coder starts a new AI chat from zero. The AI has no idea what happened before. Files get rewritten. Working features break. Hours wasted re-explaining.

Crystal Guard solves this with **7 features**:

| # | Feature | What it does |
|---|---------|-------------|
| 1 | **Session Prompt Generator** | Reads your project automatically and writes a prompt for your next AI session |
| 2 | **Quality Gates** | 15 automated checks before anything ships |
| 3 | **Baseline Tracking** | Tracks file count, test count, endpoints across sessions |
| 4 | **Session Handoff** | Generates handoff document with what was built, what changed, what's next |
| 5 | **MCP Tools** | AI assistant gets direct access to quality tools while coding |
| 6 | **Architecture Rules** | Rules file that survives session resets and platform switches |
| 7 | **Technical Debt Tracker** | Logs every failure across sessions, shows where debt is growing |

## Quick Start

```bash
# Install
pip install crystal-code

# Initialize (auto-detects your stack)
crystal init

# Run all 15 quality gates
crystal check

# See project health dashboard
crystal status

# Generate handoff prompt for next session
crystal handoff

# See all 15 gates individually
crystal gates

# Generate markdown report
crystal report --output report.md
```

## The 15 Quality Gates

| Gate | Check | Severity |
|------|-------|----------|
| 1 | Expected directories exist | Medium |
| 2 | Required files present (.gitignore) | High |
| 3 | No root file sprawl | Medium |
| 4 | No deep nesting (>6 levels) | Low |
| 5 | No database access in frontend | Critical |
| 6 | No filesystem access in frontend | Critical |
| 7 | Correct environment variable usage | High |
| 8 | No hardcoded API keys | Critical |
| 9 | No hardcoded passwords | Critical |
| 10 | No known API key formats (sk-, ghp_) | Critical |
| 11 | .env in .gitignore | Critical |
| 12 | No TODO/FIXME in production code | Low |
| 13 | No placeholder values (example.com) | Medium |
| 14 | No debug logging (console.log) | Low |
| 15 | No hardcoded localhost URLs | Medium |

## Session Handoff

The killer feature. Run `crystal handoff` at the end of your coding session:

```bash
crystal handoff --output handoff.md
```

This generates a structured prompt that includes:
- Project state (files, tests, health score)
- Recent git changes
- Baseline comparison (what changed since last session)
- Quality gate results
- Recurring technical debt
- PRD context
- Instructions for the next AI session

**Paste it into your next AI chat. The AI knows exactly where you left off.**

## Baseline Tracking

Crystal tracks your project metrics across sessions:

```
SINCE LAST SESSION
  files: 42 -> 47 (+5)
  test files: 8 -> 7 (-1) [REGRESSION]
  endpoints: 12 -> 14 (+2)
  health score: 82 -> 78 (-4) [REGRESSION]
  violations: 3 -> 5 (+2) [REGRESSION]
```

If anything goes backwards, you see it immediately.

## Supported Stacks

Crystal auto-detects your stack and loads appropriate rules:

| Stack | Detection |
|-------|-----------|
| React + Python/FastAPI + MongoDB | `package.json` + `requirements.txt` |
| React + Node/Express + MongoDB | `package.json` with express |
| Next.js + Prisma | `next.config.js` + prisma |
| Python/FastAPI standalone | `requirements.txt` with fastapi |
| Generic | Fallback rules for any project |

## CI/CD Setup

Copy this to `.github/workflows/crystal.yml`:

```yaml
name: Crystal Quality Gates
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  crystal-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install crystal-code
      - run: crystal init --ci
      - run: crystal check --format json --output crystal-report.json
      - run: crystal report --output crystal-report.md
        if: always()
```

## MCP Server Setup

### Cursor (.cursor/mcp.json)
```json
{
  "mcpServers": {
    "crystal": {
      "command": "crystal",
      "args": ["mcp", "serve"]
    }
  }
}
```

### Claude Desktop
```json
{
  "mcpServers": {
    "crystal": {
      "command": "crystal",
      "args": ["mcp", "serve"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

## Configuration

After `crystal init`, customize `.crystal/config.yaml`:

```yaml
project:
  name: My App
  stack: react-fastapi-mongo

checks:
  architecture: true
  domain_purity: true
  security: true
  placeholders: true

severity_threshold: high

ignore:
  files:
    - node_modules/**
    - venv/**
  rules:
    - hyg-003  # We use console.log intentionally
```

## Custom Rules

Add to `.crystal/rules.yaml`:

```yaml
overrides:
  disabled_rules:
    - hyg-003
  severity_overrides:
    hyg-001: medium

custom_rules:
  - id: custom-001
    name: No Inline Styles
    pattern: 'style=\{\{'
    files: ["**/*.jsx"]
    message: "Use CSS classes instead of inline styles."
    severity: low
```

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Easy first contributions:
- Add rules for new stacks (just YAML)
- Improve error messages (just strings)
- Add test fixtures (just files)
