# CI/CD Setup Guide

Crystal runs on every push to GitHub and blocks bad code from merging.

## Quick Setup (2 minutes)

### 1. Copy the workflow file

Create `.github/workflows/crystal.yml` in your repo:

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

      - name: Install Crystal
        run: pip install crystal-guard

      - name: Initialize Crystal
        run: crystal init --ci .

      - name: Run Quality Gates
        run: crystal check --format json --output crystal-report.json .

      - name: Generate Report
        if: always()
        run: crystal report --output crystal-report.md .

      - name: Comment on PR
        if: github.event_name == 'pull_request' && always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('crystal-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });

      - name: Check Pass/Fail
        run: |
          RESULT=$(python -c "import json; r=json.load(open('crystal-report.json')); print('PASS' if r['passed'] else 'FAIL')")
          if [ "$RESULT" = "FAIL" ]; then
            echo "::error::Crystal quality gates failed."
            exit 1
          fi
```

### 2. Push to GitHub

```bash
git add .github/workflows/crystal.yml
git commit -m "Add Crystal quality gates"
git push
```

### 3. That's it

Every push and PR now gets checked automatically. If checks fail, the PR is blocked.

## What Gets Checked

Crystal runs 15 quality gates on every push:

| Gate | What it checks |
|------|---------------|
| 1-4 | Architecture (directories, files, nesting) |
| 5-7 | Domain purity (no DB in frontend, correct env vars) |
| 8-11 | Security (no hardcoded secrets, .env protected) |
| 12-15 | Code hygiene (no TODOs, no debug logs, no placeholders) |

## Customizing

Add a `.crystal/config.yaml` to your repo to customize:

```yaml
severity_threshold: high  # Only fail on HIGH and CRITICAL

ignore:
  rules:
    - hyg-003  # Allow console.log
```

## PR Comment Example

When Crystal runs on a PR, it posts a comment like:

> **Crystal Health Report**
>
> **Grade: B (82/100)**
>
> ## CRITICAL Issues (1)
> - **[sec-001]** Hardcoded API key in `src/config.js:15`
>   - Fix: Move this key to your .env file
>
> ## LOW Issues (2)
> - **[hyg-001]** TODO in `backend/services/auth.py:42`
> - **[hyg-003]** console.log in `frontend/src/App.js:88`
