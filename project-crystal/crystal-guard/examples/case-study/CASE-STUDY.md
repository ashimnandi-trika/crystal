# Case Study: From F to A — Saving a Real Vibe-Coded Project

> A complete, reproducible walkthrough. Every command shown here was run on the
> actual project files included in this directory. You can clone this repo and
> run them yourself.

---

## The Project

A todo app built across 4 AI coding sessions using Cursor. The developer (Sarah)
is a product manager, not an engineer. She described what she wanted, the AI built it.

The app works on her laptop. She's about to push it to GitHub and deploy it.

**What she doesn't know:**
- Her OpenAI API key is hardcoded in two files
- Her database password is written directly in the backend code
- There's a MongoDB import in a React component
- The .env file (with all her secrets) will be committed to GitHub
- There are zero tests
- CORS is set to accept requests from any website
- There are 7 unfinished TODO items and 4 console.log debug statements

Crystal finds all of this in 3 seconds.

---

## Step 1: Install Crystal

```bash
pip install crystal-code
```

## Step 2: Initialize

```bash
cd examples/case-study/before
crystal init
```

**Real output:**
```
Detected stack: react-fastapi-mongo (confidence: high)
Detected from: package.json, requirements.txt
Created .crystal/ configuration
Loaded 15 rules for react-fastapi-mongo
```

Crystal reads the project files, figures out the tech stack automatically,
and loads the right rules. No configuration. 2 seconds.

## Step 3: Run Quality Gates

```bash
crystal check
```

**Real output:**
```
Running LOCAL quality gates...

  FAIL  Architecture (4 issues)
  FAIL  Domain Purity (2 issues)
  FAIL  Security (5 issues)
  FAIL  Code Hygiene (18 issues)

  CRYSTAL HEALTH SCORE
  F (0/100)
  Critical issues found. Do not deploy until resolved.
  Critical: 5  High: 4  Medium: 7  Low: 13
```

**29 issues. 5 critical. Score: F.**

## Step 4: See Every Gate

```bash
crystal gates
```

**Real output:**
```
CRYSTAL — 15 QUALITY GATES

  PASS  Gate 1: Expected directories exist
  FAIL  Gate 2: Required files present (1 issues)
  PASS  Gate 3: No root file sprawl
  PASS  Gate 4: No deep nesting
  FAIL  Gate 5: No DB access in frontend (1 issues)
  PASS  Gate 6: No filesystem access in frontend
  FAIL  Gate 7: Correct env var usage (1 issues)
  FAIL  Gate 8: No hardcoded API keys (2 issues)
  FAIL  Gate 9: No hardcoded passwords (1 issues)
  PASS  Gate 10: No known key formats
  FAIL  Gate 11: .env in .gitignore (1 issues)
  FAIL  Gate 12: No TODO/FIXME (7 issues)
  FAIL  Gate 13: No placeholder values (2 issues)
  FAIL  Gate 14: No debug logging (4 issues)
  FAIL  Gate 15: No hardcoded localhost (5 issues)

  5/15 gates passed
```

10 out of 15 gates failed. Here's what each failure means:

| Gate | What Crystal Found | Risk |
|------|-------------------|------|
| 2 | No .gitignore file | All secrets will be committed to GitHub |
| 5 | `import MongoClient from 'mongodb'` in App.jsx | Anyone can see database access code in browser |
| 7 | `process.env.MONGO_PASSWORD` in frontend | Server env vars don't work in browsers |
| 8 | API key in App.jsx line 6 AND server.py line 18 | Anyone sees the key, uses your OpenAI account |
| 9 | `password = "..."` written directly in server.py | Database password visible to anyone reading code |
| 11 | .env not in .gitignore | Stripe key, OpenAI key, DB password all exposed |
| 12 | 7 TODO/FIXME comments | Unfinished features that will break in production |
| 13 | "example.com" and "test@test.com" in code | Users will see placeholder text |
| 14 | 4 console.log statements | Debug output visible in production |
| 15 | 5 hardcoded localhost URLs | Every URL breaks when deployed |

## Step 5: Get Fix Prompts

```bash
crystal fix-prompt
```

Crystal generates a paste-ready prompt for each issue. Here's what the first one looks like:

```
## FIX: Database access detected in frontend code.

File: frontend/src/App.jsx, line 3
Severity: CRITICAL

What's wrong:
Database access detected in frontend code. Frontend should only
communicate with backend via API calls.

Why this is dangerous:
Your website runs in people's browsers. If database code is in the
frontend, anyone can open browser developer tools and see exactly
how to access your database. They could read, change, or delete
all your data.

How to fix it:
Move database operations to a backend service file and create an API endpoint.

Rules:
- Only change frontend/src/App.jsx
- Do not rewrite code that is already working
- After fixing, run `crystal check` to verify
```

**Sarah pastes each prompt into Cursor. The AI fixes each issue without breaking other things.**

## Step 6: Generate Architecture Rules

```bash
crystal architect
```

Creates `architecture.md` — a permanent rules file that every AI tool reads:

```markdown
# todo-app — Architecture Rules

> Every AI tool should read this file before making changes.

## Rules — DO NOT VIOLATE

### Frontend
- All frontend code lives in frontend/src/
- DO NOT put database queries in frontend files
- DO NOT use environment variables without the REACT_APP_ prefix

### Backend
- All backend code lives in backend/
- Route files handle HTTP requests only
- DO NOT put React/Vue/Angular code in backend files

### Security — CRITICAL
- NEVER hardcode API keys, passwords, or secrets in code
- ALWAYS use environment variables for sensitive values
- ALWAYS add .env to .gitignore
```

This file travels with the project. Every fork carries it. Every session reads it.

## Step 7: Session Handoff

```bash
crystal handoff --output handoff.md
```

Crystal generates a structured prompt with:
- Project state: file count, test count, health score
- Git changes since last session
- Quality gate results
- Technical debt accumulating
- What to work on next

**Tomorrow, Sarah pastes handoff.md into Cursor. Context survives.**

---

## The Results

| Metric | Before Crystal | After Fixing |
|--------|---------------|-------------|
| Health Score | **F (0/100)** | **A (100/100)** |
| Critical Issues | 5 | 0 |
| Total Issues | 29 | 0 |
| Gates Passing | 5/15 | 15/15 |
| Hardcoded Secrets | 3 (API key, password, in 2 files) | 0 |
| DB Code in Frontend | Yes (MongoDB import in React) | No |
| .env Protected | No (.env not in .gitignore) | Yes |
| Tests | 0 | Tests added |
| TODO/FIXME | 7 unfinished items | 0 |
| Debug Logs | 4 console.log statements | 0 |
| Localhost URLs | 5 hardcoded | 0 (env vars) |
| Session Context | Lost every time | Preserved via handoff |

---

## Try It Yourself

```bash
# Clone the repo
git clone https://github.com/ashimnandi-trika/crystal.git
cd crystal/project-crystal/crystal-guard

# Install Crystal
pip install crystal-code

# Run on the "before" project
crystal init examples/case-study/before
crystal check examples/case-study/before
crystal gates examples/case-study/before
crystal fix-prompt examples/case-study/before
```

Every number in this case study is from a real Crystal scan on the actual files
in the `before/` directory. No fabrication.

---

*Crystal v0.1.0 — https://crystalcodes.dev*
*pip install crystal-code*
