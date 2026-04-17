---
marp: true
theme: default
paginate: true
backgroundColor: "#0a0a0a"
color: "#e2e8f0"
style: |
  section { font-family: 'Inter', system-ui, sans-serif; padding: 70px 90px; }
  h1 { color: #ffffff; font-size: 54px; letter-spacing: -1.5px; }
  h2 { color: #ffffff; font-size: 40px; letter-spacing: -1px; }
  h3 { color: #93c5fd; font-size: 24px; }
  strong { color: #ffffff; }
  code { background: #0b1220; color: #e2e8f0; padding: 3px 8px; border-radius: 4px; }
  pre { background: #0b1220; border: 1px solid #1e293b; border-radius: 8px; padding: 18px; }
  a { color: #60a5fa; }
  .metric { font-size: 48px; color: #60a5fa; font-weight: 700; }
  .kicker { color: #60a5fa; font-family: ui-monospace, monospace; font-size: 14px; letter-spacing: 2px; }
---

<!-- _class: lead -->

<span class="kicker">VIBECON · 4-MINUTE PITCH</span>

# Crystal

## Clean code that ships.

The architecture guardian for vibe-coded projects.

**crystalcodes.dev** · open source · MIT

<!--
SPEAKER NOTES (slide 1, ~10s)
Open confident. Don't read the subtitle — let it land. Keep hands visible.
-->

---

<!-- TALK: 0:10 – 0:40 (30s) · PROBLEM -->

<span class="kicker">THE PROBLEM</span>

# AI builds fast. Then things break.

You ship something in Cursor at 11pm. It works.

Next session, you add a feature. **Old stuff breaks.**

A password lands in the frontend. A test disappears. Your handoff prompt is 4 sentences of guesswork.

- **36%** of people using AI to code never test it
- **1.7×** more bugs in AI-written vs human-written code
- **45%** of AI-generated code has security holes

*Not lint. Not CI. These are* ***project-level*** *integrity failures.*

<!--
SPEAKER NOTES (~30s)
Lead with a felt moment, not a chart. The 3 stats are a closer, not a crutch.
Emphasis: "project-level" — differentiates from linters/CI.
-->

---

<!-- TALK: 0:40 – 1:10 (30s) · INSIGHT + WHAT MAKES IT DIFFERENT -->

<span class="kicker">THE INSIGHT</span>

# The bug isn't in one file. It's **between sessions.**

Every linter watches one file. Every CI watches one build.

**Nothing watches your project across AI sessions.**

- Domain boundaries erode (DB code slides into frontend)
- Secrets leak into source (API keys, hardcoded passwords)
- Tests silently disappear
- Context is lost on every new prompt

Crystal is the first tool built for this exact gap — **the handoff, not the file.**

<!--
SPEAKER NOTES (~30s)
This is the originality slide. "The handoff, not the file" — that's your sticky line.
Say it twice if you have the time.
-->

---

<!-- TALK: 1:10 – 1:30 (20s) · WHO / WHY YOU -->

<span class="kicker">WHO IT'S FOR</span>

# Built for vibe coders. By a vibe coder.

### Persona
Anyone shipping a product with Cursor, Claude, Windsurf, Bolt, Replit, or Emergent — solo or in small teams. Not enterprise. **You.**

### Why this team
I shipped this on Emergent. I hit every one of these pain points in the last 30 days. Crystal is the tool I built because I needed it first.

<!--
SPEAKER NOTES (~20s)
Team-product fit. Be specific about YOUR pain. Mention Emergent naturally — judges value that.
-->

---

<!-- DEMO: 1:30 – 4:00 (2:30) · LIVE PRODUCT -->

<span class="kicker">DEMO — LIVE TERMINAL</span>

# One install. Twenty gates. Sixteen commands.

```bash
$ pip install crystal-code
  Installed crystal-code-0.3.0

$ crystal init
  Found: React + Python + MongoDB
  20 quality gates loaded (architecture, domain, security, hygiene, dependencies)
```

*Switch to terminal. Open a real broken repo from your dashboard.*

<!--
SPEAKER NOTES (~20s)
Narrate over the demo: "One pip install. Stack auto-detected. Sixteen gates loaded."
Don't read the slide. Let the terminal do the talking.
-->

---

<!-- DEMO SLIDE 2 -->

<span class="kicker">DEMO — CRYSTAL CHECK</span>

# Health: F (0/100) → A (98/100)

```
$ crystal check examples/case-study/before

[CRITICAL] sec-001  src/config.js:15  Hardcoded API key
[CRITICAL] dom-001  src/App.jsx:8     DB code in frontend
[HIGH]     sec-005  backend/server.py CORS wildcard allows all origins
[HIGH]     arch-002 .gitignore missing — secrets will hit GitHub

Health: F (0/100) · 29 issues · 5 critical · STAGE FAILED
```

*In plain English. No config. No setup.*

<!--
SPEAKER NOTES (~30s)
Real case-study numbers: before = F/0/100/29 issues, after = A/98/100/1 issue.
Call out plain-English suggestions — that's the vibe-coder unlock.
-->

---

<!-- DEMO SLIDE 3 -->

<span class="kicker">DEMO — FIX-PROMPT + AUDIT</span>

# Paste-ready AI prompts. Senior-engineer review.

**`crystal fix-prompt`** → generates a paste-ready prompt for your AI tool, with *why this is dangerous* in plain English.

**`crystal audit --llm`** → Crystal Agent correlates issues across analyzers, finds hotspots, calls Claude/GPT for senior-engineer insight. **Works with your key or the Emergent universal key.**

**`crystal handoff`** → one paste. Your next AI session knows the full context.

<!--
SPEAKER NOTES (~30s)
Run these live. fix-prompt is the "aha" moment — judges will lean in.
audit --llm is the "wow, AI understands AI" moment.
-->

---

<!-- DEMO SLIDE 4 — STAGE-AWARE + MCP -->

<span class="kicker">DEMO — PRODUCTION GATE</span>

# Three stages. Escalating strictness.

```
$ crystal check --stage production
  Tests required: 0 failing allowed
  No localhost URLs
  No TODOs
  All dependencies audited
  Stage: PRODUCTION · BLOCKED · 2 criticals

  Cannot ship. Run crystal fix-prompt to resolve.
```

**MCP-native**: plugs straight into Cursor, Claude Desktop, Windsurf. Your AI sees the gates in real time.

<!--
SPEAKER NOTES (~20s)
Stage-aware = Crystal respects where you are in the lifecycle. MCP integration = not a silo.
-->

---

<!-- DEMO WRAP · EXECUTION/POLISH + EMERGENT -->

<span class="kicker">EXECUTION</span>

# Shipped. Published. Tested.

- **Live on PyPI**: `pip install crystal-code` — v0.3.0, real users can install *right now*
- **161 tests, 82% coverage** — not slideware
- **16 commands, 5 analyzers, MCP server, stage pipeline**
- **crystalcodes.dev** — live landing page with full SEO, OG card, favicon

### Built with Emergent
Full-stack, end-to-end. Landing page + backend API + Python CLI + test suite + MCP server. The `crystal audit --llm` feature **uses Emergent's universal LLM key** — Crystal dogfoods the same AI substrate it protects.

<!--
SPEAKER NOTES (~20s)
Hit the "not slideware" line. Pause after it. Then Emergent — be specific.
Dogfooding line is memorable — use it.
-->

---

<!-- CLOSE · MARKET + ASK -->

<span class="kicker">WHY NOW · WHAT'S NEXT</span>

# Every AI-coded project needs this. None have it.

- **TAM**: 10M+ developers now use AI coding tools (Cursor, Claude, Bolt, Replit, Emergent). Growing ~15% QoQ.
- **Path to 100 users**: PyPI + HackerNews launch, Cursor/Claude marketplace, 5 stack presets ship today.
- **Path to revenue**: team tier ($19/mo) for shared rules + PR dashboard + history across repos.

### What I'm asking from Vibecon judges
Feedback on the two hard trade-offs: **gate strictness defaults** and **LLM cost vs. rule-based depth.**

<br>

## Crystal. Clean code that ships.

**crystalcodes.dev** · `pip install crystal-code` · MIT · built with Emergent

<!--
SPEAKER NOTES (~20s)
Land on the tagline. Don't rush. Hold eye contact on "clean code that ships."
If you have 5s, invite one judge question.
-->

---

<!-- APPENDIX (optional, not shown in 4-min) -->

<span class="kicker">APPENDIX · TECHNICAL DEPTH</span>

## Architecture

- **16** commands · **20** quality gates across **5** analyzers
- **Stage pipeline**: `local` (lenient) → `staging` (strict) → `production` (zero tolerance)
- **Optional LLM layer**: Anthropic / OpenAI / Emergent universal key
- **MCP server**: 8 tools, 3 resources, 2 prompts via FastMCP
- **Per-rule auto-fixers**: idempotent, whitelisted, never touches source code
- **Test suite**: 161 tests across 16 files, 82% coverage, CI-ready

---

<span class="kicker">APPENDIX · CASE STUDY</span>

## Before → After (real numbers)

| Metric | Before | After |
|---|---|---|
| **Grade** | F | **A** |
| **Score** | 0 / 100 | **98 / 100** |
| **Critical issues** | 5 | **0** |
| **High issues** | 3 | **0** |
| **Total issues** | 29 | **1** |
| **Stage gate** | BLOCKED | **PASSED** |

Project: React + FastAPI + MongoDB todo app. Fix time: ~2 hours with `crystal fix-prompt`.
