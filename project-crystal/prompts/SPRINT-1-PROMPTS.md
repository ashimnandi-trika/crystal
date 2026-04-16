# Crystal — Build Prompts for Missing Features
## Sprint 1: The 3 Critical Gaps

---

## PROMPT: crystal test — Execute Actual Test Suites

```
Add a `crystal test` command to the Crystal CLI.

Purpose: Actually RUN the project's tests (pytest, npm test, etc.) — not just 
check if test files exist. Report results as part of the quality gates.

Requirements:
1. Auto-detect test runner:
   - If requirements.txt has pytest → run `pytest --tb=short -q`
   - If package.json has "test" script → run `npm test` or `yarn test`
   - If package.json has vitest → run `npx vitest run`
   - If neither → report "No test runner detected"

2. Parse test results:
   - Count: total tests, passed, failed, skipped
   - Capture failing test names and error messages
   - Calculate pass rate (e.g., "12/14 tests passing (85%)")

3. Integrate with health scoring:
   - 100% pass rate → no penalty
   - <100% but >80% → MEDIUM severity issue
   - <80% → HIGH severity issue
   - 0 tests → HIGH (already exists in arch-007)
   - Test runner fails to start → report as issue

4. Output format:
   ```
   Tests: 12/14 passing (85%)
   FAILED:
   - test_payment_flow: AssertionError: expected 200, got 500
   - test_user_auth: ConnectionError: database not available
   ```

5. Integration with crystal check:
   When running `crystal check`, add a "Tests" gate:
   ```
   PASS  Architecture
   PASS  Domain Purity
   PASS  Security
   FAIL  Tests (2 failing)
   PASS  Code Hygiene
   ```

6. The test results should be included in the handoff prompt.

File: crystal_guard/test_runner.py
CLI command: crystal test [path] [--verbose]
```

---

## PROMPT: crystal fix-prompt — Generate Paste-Ready Fix Prompts

```
Add a `crystal fix-prompt` command to the Crystal CLI.

Purpose: When quality gates fail, generate a COMPLETE, PASTE-READY prompt
that the user copies into their AI coding tool. The AI reads it and fixes
the exact issue without breaking anything else.

Requirements:
1. Run all quality gates first (reuse crystal check logic)
2. For EACH issue, generate a structured fix prompt that includes:
   a. WHAT: The specific problem
   b. WHERE: File path and line number
   c. WHY: Plain-English explanation of why this matters (not jargon)
   d. HOW: Step-by-step fix instructions
   e. GUARD RAILS: What NOT to change
   f. VERIFY: How to verify the fix worked

3. Fix prompt format:
   ```
   ## FIX REQUIRED: Hardcoded API Key

   FILE: src/config.js, line 15
   
   PROBLEM: 
   The OpenAI API key "sk-abc123..." is written directly in the code.
   
   WHY THIS IS DANGEROUS:
   Anyone who can see your code gets your API key. They can use your
   OpenAI account, run up your bill, or access your data. This includes
   anyone who can see your GitHub repo.
   
   STEP-BY-STEP FIX:
   1. Open or create a file called .env in your project root
   2. Add this line: REACT_APP_OPENAI_KEY=sk-abc123...
   3. Open src/config.js
   4. Replace line 15 with: const API_KEY = process.env.REACT_APP_OPENAI_KEY
   5. Make sure .env is in your .gitignore file
   
   DO NOT:
   - Change any other lines in src/config.js
   - Rename or move any files
   - Modify any other files except .env and .gitignore
   
   VERIFY:
   Run `crystal check` — the sec-001 issue should disappear.
   ```

4. Support batch mode: `crystal fix-prompt --all` generates one document
   with ALL fixes in priority order (critical first)

5. Support clipboard: `crystal fix-prompt --copy` copies to clipboard

6. Each fix prompt should include the project's architecture rules
   context so the AI doesn't violate them while fixing.

7. WHY explanations must be written for someone who has NEVER coded.
   No jargon. No acronyms. Explain like they're 12.

File: crystal_guard/fix_prompt.py
CLI command: crystal fix-prompt [path] [--all] [--copy] [--output fixes.md]
```

---

## PROMPT: Stage-Aware Pipeline — local/staging/production

```
Add stage support to `crystal check`: `crystal check --stage local|staging|production`

Purpose: Different strictness levels for different deployment stages.
Local is lenient (you're still building). Staging is strict (testing before 
real users see it). Production is zero-tolerance.

Requirements:

1. Three stages with escalating strictness:

LOCAL (default — what crystal check does now):
- Run all 15 quality gates
- Severity threshold: fail on CRITICAL only
- TODOs allowed (you're still building)
- console.log allowed (you're debugging)
- localhost URLs allowed (you're running locally)
- Tests: warn if missing, don't fail

STAGING (stricter):
- Everything from LOCAL, plus:
- Severity threshold: fail on CRITICAL and HIGH
- No localhost URLs (staging has real URLs)
- All referenced env vars must exist
- CORS must not be wildcard (*)
- No placeholder values (example.com, test@test.com)
- Tests: must exist AND pass
- Additional staging checks:
  - stg-001: No localhost URLs in non-dev files
  - stg-002: All env vars referenced in code exist in environment
  - stg-003: CORS configured with specific origins
  - stg-004: No DEBUG=True in production configs

PRODUCTION (zero tolerance):
- Everything from STAGING, plus:
- Severity threshold: fail on CRITICAL, HIGH, and MEDIUM
- Zero TODOs/FIXMEs anywhere
- Zero console.log/print statements
- Zero placeholder values
- All tests must pass (100%)
- Health score must be A (90+)
- Additional production checks:
  - prod-001: Error monitoring configured (Sentry/similar)
  - prod-002: No development dependencies in production build
  - prod-003: All API endpoints have error handling

2. Stage state tracking:
   Crystal tracks which stage each check was run at:
   ```
   .crystal/pipeline.json:
   {
     "local": {"passed": true, "timestamp": "...", "score": 85},
     "staging": {"passed": false, "timestamp": "...", "issues": [...]},
     "production": null
   }
   ```

3. Stage progression enforcement:
   - Can't run staging check until local passes
   - Can't run production check until staging passes
   - If local fails after staging passed, staging is invalidated

4. Stage info in handoff:
   "Pipeline: local PASSED, staging FAILED (2 issues), production NOT RUN"

File: crystal_guard/pipeline.py
Modify: crystal_guard/cli.py (add --stage flag to check command)
```

---

## PROMPT: WHY Explanations for Every Gate

```
Update all 15 quality gates to include a `why` field in every Issue.

The `why` field explains to a NON-CODER why this issue matters.
Written in plain English. No jargon. No acronyms.

Examples:

Gate 5 (dom-001 — Database in frontend):
  message: "Database access detected in frontend code."
  why: "Your website runs in people's browsers. If database code is in the 
        frontend, anyone can see how to access your database just by opening 
        browser developer tools. This means anyone can read, change, or 
        delete all your data."

Gate 8 (sec-001 — Hardcoded API key):
  message: "Hardcoded API key detected."
  why: "Your API key is like a credit card number for a service you're using.
        Right now it's written directly in your code. If your code is on 
        GitHub (even a private repo that gets shared), anyone who sees it 
        gets your key. They can use your account and you'll get the bill."

Gate 12 (hyg-001 — TODO/FIXME):
  message: "Unresolved TODO comment."
  why: "TODO means 'I need to finish this later.' In production, 'later' 
        usually means 'never.' This is something your app needs but doesn't 
        have yet. If users hit this path, something will break or be missing."

Add the `why` field to the Issue dataclass.
Display it in terminal output when showing issues.
Include it in fix-prompt generation.
```
