# Case Study: Saving a Vibe-Coded Todo App

## The Story

Sarah is building a todo app using Cursor. She's not a developer — she's a product manager who describes what she wants and the AI builds it. After 4 sessions across 2 days, her app works. Sort of.

She doesn't know it yet, but her project has:
- An API key sitting directly in the frontend code
- Database queries running in React components
- Zero tests
- 6 TODO comments that never got finished
- localhost URLs hardcoded everywhere
- No .gitignore (her .env with passwords is committed)

**This case study shows how Crystal catches all of this and generates the exact fixes.**

---

## Session 1: Discovery

Sarah installs Crystal and runs it on her project for the first time.

### Step 1: Install and Initialize

```bash
$ pip install crystal-code
$ cd ~/todo-app
$ crystal init
```

**Output:**
```
Detected stack: react-fastapi-mongo (confidence: high)
Detected from: package.json, requirements.txt
Created .crystal/ configuration
Loaded 15 quality gates for react-fastapi-mongo

Run 'crystal check' to analyze your project.
```

Crystal auto-detected her stack. No configuration needed. 30 seconds.

### Step 2: First Health Check

```bash
$ crystal check
```

**Output:**
```
Running LOCAL quality gates...

  FAIL  Architecture (3 issues)
  FAIL  Domain Purity (2 issues)
  FAIL  Security (4 issues)
  FAIL  Code Hygiene (6 issues)

╭─────────────────────────────────────╮
│ CRYSTAL HEALTH SCORE                │
│                                     │
│ F (0/100)                           │
│                                     │
│ Critical issues found.              │
│ Do not deploy until resolved.       │
│                                     │
│ Critical: 7  High: 3               │
│ Medium: 3    Low: 5                │
╰─────────────────────────────────────╯

Tip: Run 'crystal fix-prompt' to get paste-ready fix instructions.
```

**F score. 18 issues. 7 critical.** Sarah had no idea.

### Step 3: See Every Gate

```bash
$ crystal gates
```

**Output:**
```
CRYSTAL — 15 QUALITY GATES

  FAIL  Gate 1: Expected directories exist (1 issue)
  FAIL  Gate 2: Required files present (1 issue)
  PASS  Gate 3: No root file sprawl
  PASS  Gate 4: No deep nesting
  FAIL  Gate 5: No DB access in frontend (1 issue)
  FAIL  Gate 6: No filesystem access in frontend (1 issue)
  PASS  Gate 7: Correct env var usage
  FAIL  Gate 8: No hardcoded API keys (1 issue)
  FAIL  Gate 9: No hardcoded passwords (1 issue)
  FAIL  Gate 10: No known key formats (1 issue)
  FAIL  Gate 11: .env in .gitignore (1 issue)
  FAIL  Gate 12: No TODO/FIXME (3 issues)
  FAIL  Gate 13: No placeholder values (1 issue)
  FAIL  Gate 14: No debug logging (2 issues)
  FAIL  Gate 15: No hardcoded localhost (2 issues)

  4/15 gates passed
```

Now Sarah can see exactly which checks pass and fail.

---

## Session 2: Fixing Critical Issues

### Step 4: Get Fix Prompts

```bash
$ crystal fix-prompt --output fixes.md
```

**Crystal generates 18 paste-ready prompts.** Here's what the first one looks like:

```markdown
## FIX: Hardcoded API key detected.

**File**: frontend/src/config.js, line 8
**Severity**: CRITICAL

**What's wrong**:
Hardcoded API key detected. API keys should be in environment variables, never in code.

**Why this is dangerous**:
Your API key is like a credit card number for a service you use.
Right now it's written directly in your code. If anyone sees your
code (GitHub, a teammate, a hacker), they get your key and can use
your account. You'll get the bill.

**How to fix it**:
Move this key to your .env file and reference it with
process.env.REACT_APP_API_KEY.

**Rules**:
- Only change frontend/src/config.js. Do not modify other files unless the fix requires it.
- Do not rename or move the file.
- Do not rewrite code that is already working.
- After fixing, run `crystal check` to verify the issue is resolved.
```

**Sarah pastes each fix prompt into Cursor.** The AI fixes the exact issue without breaking anything else.

### Step 5: Re-check After Fixes

```bash
$ crystal check
```

**After fixing all critical and high issues:**
```
  PASS  Architecture
  PASS  Domain Purity
  PASS  Security
  FAIL  Code Hygiene (5 issues)

╭─────────────────────────────────────╮
│ CRYSTAL HEALTH SCORE                │
│                                     │
│ B (78/100)                          │
│                                     │
│ Good structure with minor issues.   │
│ Quick fixes recommended.            │
│                                     │
│ Critical: 0  High: 0               │
│ Medium: 2    Low: 3                │
╰─────────────────────────────────────╯
```

**F → B in one session.** Critical issues gone. Remaining items are TODOs and console.logs — things she can clean up later.

---

## Session 3: Testing and Staging

### Step 6: Run Actual Tests

```bash
$ crystal test
```

**Output:**
```
Runner: pytest
Tests: 3/5 passing (60%)

Failed (2):
  FAILED test_create_todo: AssertionError: expected 201, got 500
  FAILED test_delete_todo: ConnectionError: database not available
```

Crystal doesn't just check if tests exist — it **runs them** and shows what's broken.

### Step 7: Try Staging Check

```bash
$ crystal check --stage staging
```

**Output:**
```
Running STAGING quality gates...

  PASS  Architecture
  PASS  Domain Purity
  PASS  Security
  FAIL  Staging (2 issues)
  FAIL  Code Hygiene (5 issues)

[HIGH] stg-001: Localhost URL found in backend/config.py:8
       Staging needs real URLs, not localhost.

[MEDIUM] stg-002: Environment variable STRIPE_KEY used in code but not defined.

Tip: Run 'crystal fix-prompt' to get paste-ready fix instructions.
```

Staging catches things local doesn't — localhost URLs and missing env vars.

### Step 8: Fix Staging Issues and Retry

After fixing localhost URLs and adding STRIPE_KEY to .env:

```bash
$ crystal check --stage staging
```

```
  PASS  Architecture
  PASS  Domain Purity
  PASS  Security
  PASS  Staging
  PASS  Code Hygiene

STAGING READY
Health: A (94/100)
```

---

## Session 4: Production and Handoff

### Step 9: Production Check

```bash
$ crystal check --stage production
```

```
Running PRODUCTION quality gates...

  PASS  Architecture
  PASS  Domain Purity
  PASS  Security
  PASS  Staging
  FAIL  Tests (2 failing)

[CRITICAL] prod-001: 2 test(s) failing. Production requires 100% pass rate.
```

Production won't let her ship with failing tests. She fixes them, retests:

```bash
$ crystal test
Tests: 5/5 passing (100%)

$ crystal check --stage production
PRODUCTION READY
Health: A (100/100)
Deploy with confidence.
```

### Step 10: Generate Architecture Rules

```bash
$ crystal architect
```

Creates `architecture.md` — a file every AI tool reads. Sarah's rules are now permanent:
- Database code stays in backend
- No secrets in code
- All env vars use REACT_APP_ prefix

### Step 11: Session Handoff

```bash
$ crystal handoff --output handoff.md
```

**Generated handoff includes:**
- Project state: 23 files, 5 tests, 4 endpoints
- Health: A (100/100)
- Pipeline: local PASSED, staging PASSED, production PASSED
- What was built in this session
- No regressions from baseline

**Tomorrow, Sarah pastes handoff.md into her AI tool. Context survives.**

---

## The Results

| Metric | Before Crystal | After Crystal |
|--------|---------------|--------------|
| Health Score | F (0/100) | A (100/100) |
| Critical Issues | 7 | 0 |
| Tests Passing | 0/0 (no tests) | 5/5 (100%) |
| Hardcoded Secrets | 3 | 0 |
| DB Code in Frontend | Yes | No |
| .env Protected | No | Yes |
| Session Context | Lost every time | Preserved via handoff |
| Time to Fix | Unknown | 2 sessions |

---

## Commands Used

| Command | When | What it did |
|---------|------|------------|
| `crystal init` | Start | Auto-detected stack, created config |
| `crystal check` | After coding | Ran 15 quality gates, showed health score |
| `crystal gates` | Discovery | Showed each gate individually |
| `crystal fix-prompt` | When issues found | Generated paste-ready AI prompts |
| `crystal test` | Before staging | Ran actual pytest, found 2 failures |
| `crystal check --stage staging` | Before staging deploy | Caught localhost URLs, missing env vars |
| `crystal check --stage production` | Before production | Enforced 100% test pass rate |
| `crystal architect` | After cleanup | Generated architecture.md with project rules |
| `crystal handoff` | End of session | Created context for next AI session |

---

## What Sarah Learned

1. **"I didn't know my API key was visible"** — Crystal caught it before anyone else did
2. **"The fix prompts saved me hours"** — She didn't have to figure out how to fix anything
3. **"Staging check caught things I'd never think of"** — localhost URLs would have broken everything
4. **"The handoff means I never start from zero"** — Every session picks up where the last one left off
5. **"It took 30 seconds to set up"** — pip install, crystal init, crystal check. That's it.

---

*This case study uses a real project structure analyzed by Crystal v0.1.0.*
*Try it yourself: `pip install crystal-code && crystal init && crystal check`*
