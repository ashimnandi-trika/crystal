# HACKER NEWS POST — Copy-paste this

## Submit at: https://news.ycombinator.com/submit

### Title:
Show HN: Crystal – CLI that runs 15 quality gates on AI-generated code

### URL:
https://github.com/ashimnandi-trika/crystal

### After posting, add this as the first comment:

---

Hi HN. I built Crystal because I kept shipping broken code from AI coding sessions.

The problem: tools like Cursor, Claude, Bolt generate code fast. But across sessions, things degrade. The AI rewrites working code, puts database queries in React components, hardcodes API keys, and nobody catches it because the code "works" locally.

Crystal is a Python CLI that runs 15 static analysis checks designed specifically for patterns that AI coding tools produce:

**Architecture** (4 gates): Are files organized? Do expected directories exist? Is there a test folder?

**Domain Purity** (3 gates): Is there database code in the frontend? Are env vars used correctly? Is crypto running in the browser?

**Security** (4 gates): Are API keys hardcoded? Passwords in code? .env in .gitignore? CORS wildcard?

**Code Hygiene** (4 gates): TODOs in production? console.log everywhere? localhost URLs? Placeholder values?

Key features beyond the 15 gates:

- **Session handoff**: `crystal handoff` generates a structured prompt you paste into your next AI session. Context survives across sessions and tools.

- **Fix prompts**: When checks fail, `crystal fix-prompt` generates paste-ready prompts with what's wrong, why it matters (in plain English), and step-by-step fix instructions. Designed for people who can't read a stack trace.

- **Stage pipeline**: `crystal check --stage local|staging|production` with escalating strictness. Local is lenient (you're building). Production is zero-tolerance (all tests must pass, no TODOs, no debug logs).

- **MCP server**: `crystal mcp serve` lets AI assistants (Cursor, Claude Desktop) call Crystal's tools directly while coding. Real-time, not after the fact.

- **Test runner**: `crystal test` detects and runs your actual test suite (pytest, npm test), not just checks if test files exist.

I ran Crystal on a real project built across 4 AI sessions. It found 29 issues including 5 critical — hardcoded API keys in 2 files, a MongoDB import in a React component, an exposed .env. The case study with actual terminal output is here: https://github.com/ashimnandi-trika/crystal/blob/main/project-crystal/crystal-guard/examples/case-study/CASE-STUDY.md

Tech stack: Python, Typer, Rich, FastMCP. 10 CLI commands. 5 built-in YAML rule sets (React+Python+Mongo, Next.js+Prisma, Vue+Node, Django, Generic). Rules are YAML so non-developers can contribute.

`pip install crystal-code && crystal init && crystal check`

Live site: https://build-integrity.emergent.host
PyPI: https://pypi.org/project/crystal-code/

Happy to answer questions. Feedback on what checks matter most would be valuable.
