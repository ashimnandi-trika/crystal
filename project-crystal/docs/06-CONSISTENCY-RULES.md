# Consistency & Quality Rules

## These rules apply to ALL components of Crystal

### 1. Naming Conventions
- Python: snake_case for functions/variables, PascalCase for classes
- Files: lowercase with underscores (architecture_analyzer.py)
- CLI commands: lowercase with hyphens (crystal check, not crystal_check)
- YAML keys: lowercase with underscores
- Rule IDs: {category}-{number} (arch-001, sec-003, dom-005)

### 2. Error Messages Must Be
- Written for non-coders (no jargon)
- Actionable (always include "how to fix")
- Specific (mention exact file and line)
- Consistent tone: helpful, not judgmental

### 3. Bad vs Good Error Messages
BAD: "Domain boundary violation in src/App.js:42 — cross-layer import detected"
GOOD: "Your file src/App.js (line 42) contains a database query. Database access should only happen in backend files. Move this code to a backend service file."

BAD: "arch-001: Missing expected directory structure"
GOOD: "Your project is missing a 'tests' folder. Adding tests helps catch bugs before they reach your users. Create a 'tests/' folder in your project root."

### 4. Severity Levels (Consistent Across All Analyzers)
```
CRITICAL — Will cause bugs, security issues, or crashes. Must fix before deploy.
HIGH     — Significant structural problem. Should fix before deploy.
MEDIUM   — Code quality issue. Fix when convenient.
LOW      — Minor style/convention issue. Nice to fix.
```

### 5. Output Formats (All Reporters Must Support)

Terminal:
- Use Rich library
- Colors: Red=critical, Orange=high, Yellow=medium, Blue=low, Green=pass
- Always show summary panel at the end
- Progress bar during analysis

JSON:
```json
{
  "project": "my-app",
  "stack": "react-python-mongo",
  "timestamp": "2026-01-15T10:30:00Z",
  "health": {
    "score": 72,
    "grade": "C"
  },
  "issues": [...],
  "passed": false
}
```

Markdown:
```markdown
# Crystal Health Report
**Project**: my-app | **Stack**: react-python-mongo | **Grade**: C (72/100)

## Critical Issues (2)
- **[sec-001]** Hardcoded API key in `src/config.js:15` ...

## Summary
Fix 2 critical issues before deploying.
```

### 6. Configuration File Consistency
All YAML files use:
- 2-space indentation
- No tabs
- Comments for non-obvious settings
- Sensible defaults (works without customization)

### 7. Testing Standards
- Every analyzer must have tests with:
  - A "clean" project (should pass with 0 issues)
  - A "dirty" project (should catch known issues)
  - Edge cases (empty files, binary files, missing permissions)
- CLI tests: use Typer's testing utilities (CliRunner)
- MCP tests: use FastMCP's testing client

### 8. Documentation Standards
- Every public function has a docstring
- README examples actually work (copy-paste test them)
- Configuration options have defaults documented
- "Why" is explained, not just "what"

### 9. Commit Message Format
```
feat(analyzer): add architecture depth check
fix(security): reduce false positives for string constants  
docs(readme): add Cursor MCP configuration example
test(domain): add edge case for empty frontend files
chore(deps): update FastMCP to 0.2.0
```

### 10. Version Strategy
- Semantic versioning: MAJOR.MINOR.PATCH
- 0.x.x = pre-stable (breaking changes allowed)
- 1.0.0 = first stable release (after community feedback)
- MINOR = new analyzers, new stack support, new features
- PATCH = bug fixes, rule updates, documentation
