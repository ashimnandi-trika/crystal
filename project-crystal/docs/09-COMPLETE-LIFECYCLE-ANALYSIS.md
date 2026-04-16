# Crystal — Complete Lifecycle Analysis
## What We Have, What's Missing, and the Full Vision

---

## THE COMPLETE JOURNEY (What a vibe coder needs, start to finish)

```
SESSION START                              SESSION END
     |                                          |
     v                                          v
[1. Context]  -->  [2. Build]  -->  [3. Check]  -->  [4. Handoff]
     |                  |               |                |
  "Where am I?"    "Add feature"   "Is it safe?"    "Save state"
     |                  |               |                |
     v                  v               v                v
[5. Local]  -->  [6. Staging]  -->  [7. Production]
     |                  |               |
  "Works here"    "Works there"    "Ships clean"
```

---

## STAGE 1: SESSION START — "Where am I?"

### What this stage needs to do:
You open your AI coding tool. You type "continue building my app."
The AI has NO IDEA what happened before. This is where 80% of vibe coding disasters begin.

Crystal should give the AI everything it needs to understand your project in one paste.

### What we HAVE (built):
| Feature | Command | Status |
|---------|---------|--------|
| Git state reader | `crystal handoff` | BUILT — reads branch, commits, changed files |
| File/test counter | `crystal handoff` | BUILT — counts files, tests, lines, endpoints |
| Health score | `crystal check` | BUILT — A-F grade with issue count |
| PRD reader | `crystal handoff` | BUILT — reads .crystal/prd.md |
| Baseline comparison | `crystal handoff` | BUILT — shows what changed since last session |
| Debt summary | `crystal handoff` | BUILT — shows recurring issues |
| Structured prompt | `crystal handoff --output handoff.md` | BUILT — generates paste-ready prompt |

### What's MISSING:
| Gap | Why it matters | Priority |
|-----|---------------|----------|
| **Stage-aware context** | Handoff doesn't say "you were working on staging" or "local tests were passing" | HIGH |
| **Feature progress tracking** | PRD is manual. Crystal should auto-detect what features exist vs what's planned | MEDIUM |
| **Last session summary** | We track sessions but don't summarize "last session you added auth and fixed 2 security issues" | HIGH |

### How the user experiences it:
```
$ crystal handoff
  Generates: handoff.md

User pastes handoff.md into Cursor/Claude/any AI tool.
AI now knows: what's built, what's broken, what's next.
```

---

## STAGE 2: DURING BUILD — "The AI is writing code"

### What this stage needs to do:
The AI is generating code. RIGHT NOW, before it saves the file, Crystal should be whispering:
"That file goes in the wrong folder."
"That's a hardcoded password."
"You're putting database code in a React component."

### What we HAVE:
| Feature | How it works | Status |
|---------|-------------|--------|
| MCP Server | `crystal mcp serve` — AI tools connect via MCP protocol | BUILT |
| validate_file_placement | AI calls this before creating files | BUILT |
| check_architecture | AI calls after changes | BUILT |
| check_domain_purity | Catches DB in frontend, etc. | BUILT |
| check_security | Catches hardcoded secrets | BUILT |
| get_project_context | AI reads project state | BUILT |
| update_prd | AI records what it built | BUILT |

### What's MISSING:
| Gap | Why it matters | Priority |
|-----|---------------|----------|
| **Pre-save hook** | MCP tools are available but the AI has to CHOOSE to call them. No automatic triggering. | LOW (MCP spec limitation) |
| **Diff review** | Can't review a specific code diff, only scan whole files | MEDIUM |
| **Suggested file location** | We say "wrong place" but don't suggest "put it HERE instead" with full path | BUILT (we do suggest) |

### How the user experiences it:
```
User has Crystal MCP configured in Cursor.
User: "Add a payment feature"
AI writes code, Crystal MCP is available.
AI can call: validate_file_placement("frontend/src/payment.js", "payment processing")
Crystal responds: "WARNING: Payment processing should go in backend/services/payment.py"
AI adjusts automatically.
```

---

## STAGE 3: LOCAL CHECK — "Is it safe to push?"

### What this stage needs to do:
You finished coding. Before you push ANYTHING, Crystal runs every check locally.
If something's wrong, it tells you WHAT, WHERE, WHY, and HOW to fix it.

### What we HAVE:
| Gate | Rule ID | What it checks | WHY it matters (for vibe coders) |
|------|---------|---------------|----------------------------------|
| 1 | arch-001 | Expected directories exist | "Your project needs organized folders. Without them, your AI tool will put files in random places next session." |
| 2 | arch-002 | Required files (.gitignore) | "Without .gitignore, your passwords and API keys get uploaded to GitHub for anyone to see." |
| 3 | arch-004 | No root file sprawl | "Too many files in the root folder means your project is getting messy. Things will break as it grows." |
| 4 | arch-005 | No deep nesting (>6 levels) | "If folders go too deep, nobody (including AI) can find anything." |
| 5 | dom-001 | No DB access in frontend | "Database code in your website's front end means anyone can see and hack your database. Critical security risk." |
| 6 | dom-002 | No filesystem access in frontend | "Your website runs in a browser. Browsers can't read files from a server. This code will crash." |
| 7 | dom-003 | Correct env variable usage | "Your secret keys won't load because the browser can only see variables starting with REACT_APP_." |
| 8 | sec-001 | No hardcoded API keys | "If your API key is in the code, anyone who sees the code gets your key. They can run up your bill or steal data." |
| 9 | sec-002 | No hardcoded passwords | "Same as API keys. Never put passwords directly in code. Use environment variables." |
| 10 | sec-003 | No known key formats | "Crystal recognizes Stripe, OpenAI, GitHub, and AWS key patterns. Even if you renamed the variable." |
| 11 | sec-004 | .env in .gitignore | "Your .env file has all your secrets. If it's not in .gitignore, it gets uploaded to GitHub." |
| 12 | hyg-001 | No TODO/FIXME | "TODO means 'I'll fix this later.' In production, 'later' never comes. Fix it now or remove it." |
| 13 | hyg-002 | No placeholder values | "example.com in your code means something wasn't configured properly. Real users will see broken links." |
| 14 | hyg-003 | No debug logging | "console.log in production slows your app and can leak sensitive data to anyone who opens browser tools." |
| 15 | hyg-004 | No hardcoded localhost | "localhost only works on your computer. When you deploy, everything pointing to localhost breaks." |

### What's MISSING:
| Gap | Why it matters | Priority |
|-----|---------------|----------|
| **Run actual tests** | We check IF tests exist but don't RUN them (pytest, npm test). A test file could be empty or failing. | CRITICAL |
| **Fix prompt generation** | When checks fail, we say what's wrong. But we should generate a PASTE-READY prompt the user gives to their AI: "Fix this specific issue in this specific file." | CRITICAL |
| **WHY explanations in output** | Our terminal output shows the issue but not the "why it matters" column from above. Non-coders need this. | HIGH |
| **Staging vs production strictness** | All 15 gates run the same way. Staging should be stricter than local. Production should be strictest. | HIGH |

### How the user experiences it (CURRENT):
```
$ crystal check
  PASS  Architecture
  FAIL  Security (1 issue)
  PASS  Domain Purity
  PASS  Code Hygiene

  Health: B (82/100)
  [CRITICAL] sec-001: Hardcoded API key in src/config.js:15
  Fix: Move this key to your .env file
```

### How it SHOULD work (VISION):
```
$ crystal check

  PASS  Architecture       "Your project structure looks good"
  FAIL  Security           "1 problem found that could expose your data"
  PASS  Domain Purity      "All code is in the right place"  
  PASS  Code Hygiene       "Your code is clean"

  Health: B (82/100)

  WHAT'S WRONG:
  Your file src/config.js (line 15) contains an API key directly in the code.

  WHY THIS IS DANGEROUS:
  Anyone who can see your code (GitHub, a teammate, a hacker) gets your API key.
  They can use it to access your services, run up bills, or steal data.

  HOW TO FIX IT:
  1. Create a .env file and add: API_KEY=your-key-here
  2. In your code, replace the key with: process.env.REACT_APP_API_KEY
  3. Make sure .env is in your .gitignore

  Or paste this into your AI tool:
  ┌──────────────────────────────────────────────────┐
  │ Fix the hardcoded API key in src/config.js       │
  │ line 15. Move it to a .env file and reference    │
  │ it using process.env.REACT_APP_API_KEY. Do not   │
  │ change any other code in the file.               │
  └──────────────────────────────────────────────────┘
```

---

## STAGE 4: STAGING — "Does it work outside my computer?"

### What this stage needs to do:
Code passed local checks. Now it goes to a staging environment (test server).
Different things can break here: wrong URLs, missing env vars, CORS issues.

### What we HAVE:
| Feature | Status |
|---------|--------|
| GitHub Actions workflow | BUILT — runs Crystal checks on every push |
| JSON output for CI | BUILT — crystal check --format json |
| Markdown PR comments | BUILT — crystal report generates PR comment |

### What's MISSING:
| Gap | Why it matters | Priority |
|-----|---------------|----------|
| **`crystal check --stage staging`** | Different rules for staging: no localhost URLs allowed, CORS must be configured, all env vars must exist | HIGH |
| **Env var validator** | Check that every env var referenced in code actually exists in the environment | HIGH |
| **Endpoint health check** | After deploy to staging, verify all endpoints return 200 | MEDIUM |
| **Staging-specific rules** | "In staging, DEBUG must be False", "No wildcard CORS", "HTTPS required" | HIGH |

### How it SHOULD work:
```
$ crystal check --stage staging

  Running STAGING checks (stricter than local)...

  PASS  Architecture
  PASS  Domain Purity
  PASS  Security
  FAIL  Staging Readiness    "2 issues found"

  [HIGH] No localhost URLs allowed in staging
         Found: backend/config.py:8 → "http://localhost:3000"
         Fix: Use environment variable FRONTEND_URL instead

  [HIGH] Environment variable STRIPE_KEY not found
         Referenced in: backend/services/payment.py:3
         Fix: Add STRIPE_KEY to your staging .env
```

---

## STAGE 5: PRODUCTION — "Ship it?"

### What this stage needs to do:
Staging passed. Final check before real users see your code.
This is the strictest gate. Everything must be perfect.

### What we HAVE:
| Feature | Status |
|---------|--------|
| Health score threshold | BUILT — configurable via severity_threshold |
| CI/CD fail on issues | BUILT — exit code 1 when checks fail |

### What's MISSING:
| Gap | Why it matters | Priority |
|-----|---------------|----------|
| **`crystal check --stage production`** | Zero tolerance: no TODOs, no debug logs, no placeholders, all tests pass, security clean | HIGH |
| **Production checklist** | "SSL configured? Error monitoring set up? Backup strategy?" | MEDIUM |
| **Rollback awareness** | "Last production deploy was 3 days ago. 47 files changed since then. Review carefully." | LOW |

### How it SHOULD work:
```
$ crystal check --stage production

  Running PRODUCTION checks (zero tolerance)...

  PASS  Architecture         15/15 gates passed
  PASS  Domain Purity        No boundary violations
  PASS  Security             No secrets exposed
  PASS  Code Hygiene         No TODOs, no debug logs
  PASS  Tests                12/12 tests passing
  PASS  Staging Verified     All staging checks passed

  PRODUCTION READY ✓
  Health: A (100/100)
  
  Deploy with confidence.
```

---

## STAGE 6: WHEN THINGS FAIL — "Smart Fix Prompts"

### What this stage needs to do:
Something failed. The vibe coder doesn't know how to fix it.
Crystal should generate the EXACT prompt they paste into their AI tool.

### What we HAVE:
| Feature | Status |
|---------|--------|
| Issue detection | BUILT — finds the problem |
| Suggestion text | BUILT — one-line suggestion |

### What's MISSING:
| Gap | Why it matters | Priority |
|-----|---------------|----------|
| **`crystal fix-prompt`** | Generates a complete, paste-ready AI prompt for each issue. Not just "move the key" but "Here's the exact prompt to paste into Claude/Cursor to fix this." | CRITICAL |
| **Context-aware fix** | The fix prompt should include file content, project rules, and what NOT to change | HIGH |
| **Batch fix prompt** | One prompt that fixes ALL issues at once, in the right order | MEDIUM |

### How it SHOULD work:
```
$ crystal fix-prompt

  Found 3 issues. Generating fix prompts...

  ── Issue 1 of 3 (CRITICAL) ──────────────────────────
  
  Paste this into your AI coding tool:
  
  ┌─────────────────────────────────────────────────────┐
  │ TASK: Fix hardcoded API key                         │
  │                                                     │
  │ FILE: src/config.js, line 15                        │
  │ PROBLEM: The API key "sk-abc..." is directly in     │
  │ the code. This is a security risk.                  │
  │                                                     │
  │ WHAT TO DO:                                         │
  │ 1. Create .env file with: REACT_APP_API_KEY=sk-abc  │
  │ 2. In src/config.js line 15, replace the key with:  │
  │    process.env.REACT_APP_API_KEY                    │
  │ 3. Add .env to .gitignore if not already there      │
  │                                                     │
  │ DO NOT change any other code in the file.           │
  │ DO NOT rename or move the file.                     │
  │ DO NOT modify any other files.                      │
  └─────────────────────────────────────────────────────┘

  ── Issue 2 of 3 (HIGH) ──────────────────────────────
  ...
```

---

## STAGE 7: SESSION END — "Save everything"

### What this stage needs to do:
You're done coding for today. Crystal saves the state so tomorrow's session
picks up exactly where you left off.

### What we HAVE:
| Feature | Command | Status |
|---------|---------|--------|
| Session handoff | `crystal handoff` | BUILT |
| Baseline snapshot | Auto-saved on `crystal check` | BUILT |
| Debt recording | Auto-saved on `crystal check` | BUILT |
| Session log | Auto-saved on `crystal handoff` | BUILT |
| Architecture rules | `crystal architect` | BUILT |

### What's MISSING:
| Gap | Why it matters | Priority |
|-----|---------------|----------|
| **Auto session summary** | "This session you: added 5 files, fixed 2 security issues, health went from C to B" | HIGH |
| **PRD auto-update** | Crystal should auto-update the PRD with what was built, not require manual edits | MEDIUM |
| **Next session priorities** | "Next session: fix the 1 remaining TODO, add tests for payment module" | HIGH |

---

## COMPLETE GAP ANALYSIS — WHAT'S MISSING

### CRITICAL (Must build — the product is incomplete without these)

| # | Feature | What it does | Why |
|---|---------|-------------|-----|
| 1 | **`crystal test`** | Runs actual tests (pytest/npm test), not just checks if test files exist | Without this, "15 gates passed" is misleading. Tests could be failing. |
| 2 | **`crystal fix-prompt`** | Generates paste-ready AI prompts for every issue | This is the killer feature for vibe coders. They can't fix issues themselves. |
| 3 | **Stage-aware checking** | `crystal check --stage local/staging/production` with escalating strictness | Without stages, there's no pipeline. Just one flat check everywhere. |

### HIGH (Should build — significantly improves the product)

| # | Feature | What it does |
|---|---------|-------------|
| 4 | **WHY explanations** | Every issue includes a simple "Why this matters" paragraph |
| 5 | **Auto session summary** | End of session generates "what you did" summary automatically |
| 6 | **Next session priorities** | Handoff includes "start with these tasks" based on issues and PRD |
| 7 | **Env var validator** | Checks that all referenced env vars actually exist |
| 8 | **Test regression detection** | "Test file X existed last session but is missing now" |

### MEDIUM (Nice to have — polish)

| # | Feature | What it does |
|---|---------|-------------|
| 9 | **Batch fix prompt** | One prompt that fixes all issues in priority order |
| 10 | **Production checklist** | Final deploy checklist (SSL, monitoring, backups) |
| 11 | **Diff review** | Review specific file changes, not just full scan |
| 12 | **Feature tracking** | Auto-detect which features exist vs what's in the PRD |

---

## THE PIPELINE — How It All Connects

```
┌─────────────────────────────────────────────────────────────┐
│                    CRYSTAL PIPELINE                          │
│                                                             │
│  SESSION START                                              │
│  ├─ crystal handoff (paste into AI)                         │
│  ├─ crystal status (quick health check)                     │
│  └─ AI reads architecture.md (knows your rules)             │
│                                                             │
│  DURING BUILD                                               │
│  ├─ MCP Server running (real-time guidance)                 │
│  └─ AI has access to all Crystal tools                      │
│                                                             │
│  LOCAL CHECK                                                │
│  ├─ crystal check --stage local                             │
│  │   ├─ 15 quality gates                                    │
│  │   ├─ crystal test (run actual tests)          ← MISSING  │
│  │   └─ Baseline comparison                                 │
│  ├─ If FAIL: crystal fix-prompt                  ← MISSING  │
│  └─ If PASS: push to staging                                │
│                                                             │
│  STAGING CHECK                                              │
│  ├─ crystal check --stage staging                ← MISSING  │
│  │   ├─ Everything from local +                             │
│  │   ├─ No localhost URLs                                   │
│  │   ├─ Env vars validated                       ← MISSING  │
│  │   └─ CORS configured                                    │
│  ├─ If FAIL: crystal fix-prompt                  ← MISSING  │
│  └─ If PASS: promote to production                          │
│                                                             │
│  PRODUCTION CHECK                                           │
│  ├─ crystal check --stage production             ← MISSING  │
│  │   ├─ Everything from staging +                           │
│  │   ├─ Zero TODOs/FIXMEs                                   │
│  │   ├─ Zero debug logging                                  │
│  │   ├─ All tests pass                           ← MISSING  │
│  │   └─ Zero critical/high issues                           │
│  └─ DEPLOY                                                  │
│                                                             │
│  SESSION END                                                │
│  ├─ crystal handoff --output handoff.md                     │
│  ├─ crystal architect (update rules)                        │
│  ├─ Auto session summary                         ← MISSING  │
│  └─ Baseline saved for next session                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## WHAT "FAANG GRADE" MEANS FOR US

1. **Every feature has a WHY** — Not just "this is a security issue" but "here's what happens to YOUR app if you ignore this"
2. **Every failure has a FIX** — Not just "something's wrong" but "here's the exact prompt to fix it"
3. **Progressive strictness** — Local is lenient, staging is strict, production is zero-tolerance
4. **Tests are real** — We actually run tests, not just check if test files exist
5. **Nothing is random** — Each gate runs in logical order, each stage builds on the previous
6. **The user never feels lost** — Every message explains what's happening and what to do next
7. **Context survives everything** — Session resets, tool switches, team changes — Crystal remembers

---

## RECOMMENDED BUILD ORDER

### Sprint 1: Fix the 3 critical gaps
1. `crystal test` — execute actual test suites
2. `crystal fix-prompt` — generate paste-ready fix prompts
3. `--stage local|staging|production` — stage-aware pipeline

### Sprint 2: Polish the experience
4. WHY explanations on every issue
5. Auto session summary
6. Env var validator
7. Next session priorities in handoff

### Sprint 3: Complete the pipeline
8. Test regression detection
9. Batch fix prompts
10. Production checklist

---

## CURRENT STATE SUMMARY

| Component | Status | Grade |
|-----------|--------|-------|
| Session handoff / prompt generator | BUILT | B+ (needs stage awareness, auto-summary) |
| 15 quality gates | BUILT | A (solid, covers real issues) |
| Baseline tracking | BUILT | A (tracks metrics across sessions) |
| MCP Server | BUILT | A (8 tools, 3 resources) |
| Architecture rules | BUILT | A (crystal architect generates architecture.md) |
| Debt tracker | BUILT | A (logs recurring issues, shows trends) |
| Test execution | NOT BUILT | F (checks if tests exist, doesn't RUN them) |
| Fix prompt generation | NOT BUILT | F (shows suggestions, no paste-ready prompts) |
| Stage pipeline | NOT BUILT | F (no local/staging/production differentiation) |
| WHY explanations | PARTIAL | C (some suggestions, no plain-English "why") |

**Overall: 70% complete. The 30% that's missing is the difference between "useful tool" and "FAANG-grade product."**
