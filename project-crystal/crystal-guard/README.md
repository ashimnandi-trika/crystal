<div align="center">

# Crystal

**Clean code that ships.**

Your AI coding buddy that protects architecture integrity and domain purity,
from first commit to production.

[![PyPI version](https://img.shields.io/pypi/v/crystal-code?color=blue&label=pypi)](https://pypi.org/project/crystal-code/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

[Website](https://crystalcodes.dev) · [Getting Started](#getting-started) · [Commands](#commands) · [Contributing](#contributing)

</div>

---

## What is Crystal?

You build apps with AI. Cursor, Claude, Bolt, Emergent — whatever tool you use.
It works great. Until it doesn't.

**The problem:** Every new AI session starts from zero. The AI rewrites files that were already working. Passwords end up in the code. Database queries appear in the frontend. Tests disappear. Nobody notices until production breaks.

**Crystal fixes this.** It watches your project structure, enforces rules across sessions, and tells you exactly what's wrong before you ship. In plain English.

```bash
pip install crystal-code
crystal init
crystal check
```

---

## What Crystal Does

| # | Feature | What it does |
|---|---------|-------------|
| 1 | **Session Handoff** | Reads your project and generates a prompt for your next AI session. Paste it in. The AI knows where you left off. |
| 2 | **15 Quality Gates** | Checks architecture, security, domain purity, and code hygiene. Tells you exactly what's wrong and how to fix it. |
| 3 | **Fix Prompts** | When checks fail, generates a paste-ready prompt with what's wrong, why it matters, and step-by-step fix instructions. |
| 4 | **Stage Pipeline** | Different strictness for local, staging, and production. Gets stricter as you get closer to real users. |
| 5 | **Test Runner** | Actually runs your tests (pytest, npm test). Not just checks if test files exist. |
| 6 | **Baseline Tracking** | Tracks file count, test count, endpoints across sessions. If anything goes backwards, you see it immediately. |
| 7 | **Architecture Rules** | Generates an architecture.md that every AI tool reads. Rules survive session resets and platform switches. |
| 8 | **Debt Tracker** | Logs every failure across sessions. Shows where problems are piling up so you fix the right things first. |
| 9 | **MCP Server** | Plugs into your AI tool (Cursor, Claude, VS Code). The AI can check quality while it writes code. Real-time. |

---

## Getting Started

### Install

```bash
pip install crystal-code
```

### Initialize (auto-detects your tech stack)

```bash
crystal init
```

### Run all 15 quality gates

```bash
crystal check
```

### That's it.

You'll see a health score from A to F. Red items need fixing. Green means you're good.

---

## Commands

| Command | What it does |
|---------|-------------|
| `crystal init` | Set up Crystal for your project. Auto-detects your stack. |
| `crystal check` | Run all 15 quality gates. See your health score (A to F). |
| `crystal check --stage staging` | Stricter checks for staging (no localhost, env vars validated). |
| `crystal check --stage production` | Zero tolerance. All tests must pass. No TODOs. No debug logs. |
| `crystal test` | Run your actual tests (pytest, npm test). Report pass/fail. |
| `crystal fix-prompt` | Generate paste-ready AI prompts to fix every issue found. |
| `crystal handoff` | Generate a session handoff prompt for your next AI coding session. |
| `crystal status` | Quick health dashboard with score, trends, and changes. |
| `crystal gates` | Show all 15 gates individually with pass/fail. |
| `crystal architect` | Generate architecture.md with your project rules. |
| `crystal report` | Generate a detailed markdown report for sharing or PRs. |
| `crystal mcp serve` | Start the MCP server so your AI tool gets real-time quality checks. |

---

## The 15 Quality Gates

| Gate | What it checks | Why it matters |
|------|---------------|----------------|
| 1 | Expected directories exist | So your AI puts files in the right place |
| 2 | Required files (.gitignore) | So your secrets don't end up on GitHub |
| 3 | No root file sprawl | So your project stays organized |
| 4 | No deep nesting | So files are easy to find |
| 5 | No database in frontend | So hackers can't see your database queries |
| 6 | No filesystem in frontend | Because browsers can't read server files |
| 7 | Correct env variables | So your config actually loads |
| 8 | No hardcoded API keys | So nobody steals your keys from GitHub |
| 9 | No hardcoded passwords | Same reason. Never put passwords in code. |
| 10 | No known key formats | Crystal recognizes Stripe, OpenAI, AWS, GitHub key patterns |
| 11 | .env in .gitignore | So your secrets file doesn't get committed |
| 12 | No TODO/FIXME | Because "later" means "never" in production |
| 13 | No placeholder values | So users don't see example.com in your app |
| 14 | No debug logging | So console.log doesn't leak data in production |
| 15 | No hardcoded localhost | Because localhost breaks when you deploy |

---

## Pipeline: Local → Staging → Production

Crystal gets stricter as you get closer to real users:

```bash
# Local: lenient. You're still building.
crystal check --stage local

# Staging: strict. No localhost. Env vars must exist.
crystal check --stage staging

# Production: zero tolerance. All tests pass. No TODOs. No debug logs.
crystal check --stage production
```

Each stage must pass before you can run the next one.

---

## Fix Prompts

When something fails, Crystal writes the fix for you:

```bash
crystal fix-prompt
```

This generates a prompt for each issue that includes:
- **What's wrong** — the specific problem
- **Why it's dangerous** — explained like you've never coded before
- **How to fix it** — step by step
- **What not to touch** — so the AI doesn't break other things

Paste it into your AI tool. The issue gets fixed.

---

## Session Handoff

At the end of your coding session:

```bash
crystal handoff --output handoff.md
```

This captures:
- What files exist, how many tests, what endpoints
- What changed since last session (baseline comparison)
- Quality gate results
- Technical debt that's piling up
- Your project requirements document

**Paste handoff.md into your next AI session. Context survives.**

Works across tools. Start in Cursor, continue in Claude, finish in Emergent.

---

## MCP Server

Crystal plugs into your AI tool so it can check quality while it codes.

### Cursor
Create `.cursor/mcp.json`:
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

### VS Code / Windsurf
```json
{
  "mcp": {
    "servers": {
      "crystal": {
        "type": "stdio",
        "command": "crystal",
        "args": ["mcp", "serve"]
      }
    }
  }
}
```

The AI gets access to 8 tools: check architecture, check security, validate file placement, get project context, run all checks, get health score, update PRD, check domain purity.

---

## Supported Stacks

Crystal auto-detects your stack:

| Stack | How it detects |
|-------|---------------|
| React + Python/FastAPI + MongoDB | `package.json` with react + `requirements.txt` with fastapi + pymongo |
| Next.js + Prisma + PostgreSQL | `next.config.js` + prisma in dependencies |
| Vue + Node/Express | `package.json` with vue + express |
| Python Django | `manage.py` + django in requirements |
| Generic | Fallback rules for any project |

---

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

---

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

---

## CI/CD

Add `.github/workflows/crystal.yml` to your repo:

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
      - run: crystal init --ci .
      - run: crystal check --format json --output crystal-report.json .
      - run: crystal report --output crystal-report.md .
        if: always()
```

Every push gets checked. Bad code can't merge.

---

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Easy first contributions:**
- Add rules for a new stack (just YAML, no Python needed)
- Improve error messages and WHY explanations (just strings)
- Add test fixtures (just create sample project files)
- Improve documentation

---

## License

MIT — free forever. See [LICENSE](LICENSE).

---

## Links

- **Website**: [crystalcodes.dev](https://crystalcodes.dev)
- **PyPI**: [pypi.org/project/crystal-code](https://pypi.org/project/crystal-code/)
- **Issues**: [github.com/ashimnandi-trika/crystal/issues](https://github.com/ashimnandi-trika/crystal/issues)

---

<div align="center">
<sub>Built for people who build with AI.</sub>
</div>
