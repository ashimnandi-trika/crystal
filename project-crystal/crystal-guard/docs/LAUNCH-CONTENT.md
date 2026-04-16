# Crystal — Launch Content (Ready to Post)

---

## REDDIT: r/vibecoding

**Title:** I built a CLI that checks your vibe-coded project for problems before you ship

**Body:**

I've been building apps with Cursor for the past few months. It's amazing until session 3, when the AI rewrites something that was already working, or puts database code in a React component, or hardcodes an API key in the frontend.

After losing a weekend to debugging issues I didn't even know existed, I built Crystal.

**What it does:**
- Runs 15 checks on your project (architecture, security, domain purity, code hygiene)
- Gives you a health score from A to F
- When something fails, it generates a paste-ready prompt — you paste it into your AI tool and the issue gets fixed
- Tracks your project across sessions — so your AI knows what happened before
- Generates a handoff prompt at the end of each session so you never start from zero

**The pipeline:**
- `crystal check --stage local` — lenient, you're still building
- `crystal check --stage staging` — strict, catches localhost URLs and missing env vars
- `crystal check --stage production` — zero tolerance, all tests must pass

**Real example:**
I ran Crystal on a todo app built across 4 AI sessions. It found 18 issues including 3 hardcoded API keys, database queries in React components, and no .gitignore (meaning all secrets were committed to git). The project went from F (0/100) to A (100/100) after two fix sessions.

Full case study with before/after: https://github.com/ashimnandi-trika/crystal/blob/main/project-crystal/crystal-guard/examples/case-study-todo-app/CASE-STUDY.md

**Install:**
```
pip install crystal-code
crystal init
crystal check
```

Open source, MIT license, works with any AI coding tool.

GitHub: https://github.com/ashimnandi-trika/crystal
Website: https://build-integrity.emergent.host

Happy to answer any questions. Would love feedback on what checks matter most to you.

---

## REDDIT: r/cursor

**Title:** Made a tool that gives Cursor context about what you built last session (MCP + CLI)

**Body:**

Every time I start a new Cursor session, I spend 10 minutes re-explaining what I built yesterday. The AI has no idea what happened before. It rewrites working code. It creates duplicate files.

So I built Crystal — a CLI + MCP server that solves this:

1. **End of session:** Run `crystal handoff --output handoff.md`
   Crystal reads your git history, counts files, runs 15 quality checks, and generates a structured summary.

2. **Next session:** Paste handoff.md into Cursor.
   The AI now knows exactly what exists, what changed, what's broken, and what to do next.

3. **While coding:** Crystal runs as an MCP server.
   Add this to `.cursor/mcp.json`:
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
   Now Cursor can call Crystal's tools directly — check architecture, validate file placement, get project context.

It also runs 15 quality gates (security, architecture, domain purity) and tracks your project health across sessions.

Install: `pip install crystal-code`

GitHub: https://github.com/ashimnandi-trika/crystal

Open source, MIT. Would love to hear if this is useful for your workflow.

---

## REDDIT: r/webdev

**Title:** Open source CLI that catches hardcoded API keys, wrong file placement, and missing tests in AI-generated code

**Body:**

If you're using AI to write code (Cursor, Claude, Copilot, anything), there's a pattern I keep seeing:

- AI puts database queries in React components
- API keys end up hardcoded in frontend files
- .env file never gets added to .gitignore
- Every session the AI overwrites something that was working
- No tests, ever

I built Crystal to catch all of this automatically. It's a CLI that runs 15 checks:

| Check | What it catches |
|-------|----------------|
| Architecture | Missing directories, no tests folder, file sprawl |
| Domain purity | DB code in frontend, wrong env vars, crypto in browser |
| Security | Hardcoded keys, passwords, exposed .env, CORS wildcard |
| Code hygiene | TODOs, console.logs, localhost URLs, placeholder values |

It also has a stage pipeline:
- `crystal check --stage local` — you're still building, lenient
- `crystal check --stage staging` — stricter, no localhost, env vars validated
- `crystal check --stage production` — zero tolerance, all tests must pass

When something fails, `crystal fix-prompt` generates a paste-ready prompt with the exact fix instructions. No Googling needed.

```
pip install crystal-code
crystal init
crystal check
```

Works with React, Next.js, Vue, Python/FastAPI, Django. Auto-detects your stack.

GitHub: https://github.com/ashimnandi-trika/crystal
MIT license.

---

## TWITTER/X THREAD

**Tweet 1:**
I build apps with AI. Here's the problem nobody talks about:

Every new session starts from zero. The AI has no idea what you built yesterday.

It rewrites files that work. Puts database code in the frontend. Hardcodes API keys.

So I built something to fix it. Thread:

**Tweet 2:**
Crystal is a CLI that runs 15 quality checks on your AI-generated code.

Architecture. Security. Domain purity. Code hygiene.

It gives you a score from A to F and tells you exactly what's wrong in plain English.

`pip install crystal-code && crystal init && crystal check`

**Tweet 3:**
When something fails, Crystal generates a paste-ready fix prompt.

You copy it. Paste into your AI tool. The issue gets fixed.

No Googling. No Stack Overflow. Just: "here's what's wrong, here's why, here's how to fix it."

**Tweet 4:**
The killer feature: session handoff.

Run `crystal handoff` at the end of your session. It reads your git history, file counts, test results, and generates a prompt.

Paste it into your next session. The AI knows exactly where you left off.

Context survives.

**Tweet 5:**
It also has a pipeline:

Local → Staging → Production

Each stage is stricter. Production = zero tolerance. All tests must pass. No TODOs. No debug logs. No hardcoded secrets.

Nothing ships broken.

**Tweet 6:**
Real results from a case study:

Before Crystal: F (0/100) — 7 critical issues, 3 exposed API keys
After Crystal: A (100/100) — zero issues, production ready

Two sessions. That's all it took.

**Tweet 7:**
Crystal is open source. MIT license. Free forever.

Works with Cursor, Claude, VS Code, Bolt, Lovable, Replit, Emergent — any AI coding tool.

GitHub: github.com/ashimnandi-trika/crystal
Website: build-integrity.emergent.host

Try it. Break it. Tell me what you think.

---

## HACKER NEWS: Show HN

**Title:** Show HN: Crystal – 15 quality gates for AI-generated code (CLI + MCP server)

**Body:**
Crystal is an open-source CLI that checks AI-generated code for architectural issues, security problems, and code quality before you ship.

The problem: When non-developers use AI tools (Cursor, Bolt, Claude) to build apps, the code works initially but accumulates structural problems across sessions — hardcoded secrets, wrong separation of concerns, no tests, broken architecture.

Crystal runs 15 static analysis checks specifically designed for patterns that AI coding tools commonly produce:

- Architecture: file structure, missing directories, deep nesting
- Domain purity: database code in frontend, wrong env vars
- Security: hardcoded API keys/passwords, exposed .env, CORS
- Code hygiene: TODOs, debug logs, placeholder values, localhost URLs

It also has:
- Session handoff: generates a structured prompt for your next AI session
- Fix prompts: when checks fail, generates paste-ready AI prompts
- Stage pipeline: local (lenient) → staging (strict) → production (zero tolerance)
- MCP server: plugs into Cursor/Claude for real-time quality checks
- Baseline tracking: tracks metrics across sessions

```
pip install crystal-code
crystal init
crystal check
```

GitHub: https://github.com/ashimnandi-trika/crystal

Built with Python + Typer + Rich + FastMCP. MIT license.
