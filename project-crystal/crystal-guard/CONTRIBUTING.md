# Contributing to Crystal

Thank you for your interest in contributing to Crystal. This guide will help you get started.

## Ways to Contribute

### No Python knowledge needed

- **Add rules for a new stack**: Rules are YAML files in `src/crystal_guard/rules/builtin/`. Copy an existing one and modify it for your stack. [See rules format](#adding-stack-rules)
- **Improve error messages**: The WHY explanations in `src/crystal_guard/fix_prompt.py` are plain English strings. If you can explain a concept more clearly, submit a PR.
- **Add test fixtures**: Create sample projects in `tests/fixtures/` that test specific scenarios.
- **Improve docs**: Fix typos, add examples, clarify confusing sections.

### Python knowledge helpful

- **Add new analyzers**: Create a new file in `src/crystal_guard/analyzers/`.
- **Improve detection**: Better stack detection logic in `src/crystal_guard/detector.py`.
- **Add CLI commands**: New commands in `src/crystal_guard/cli.py`.
- **Fix bugs**: Check [open issues](https://github.com/ashimnandi-trika/crystal/issues).

## Getting Started

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/crystal.git
cd crystal
```

### 2. Install in development mode

```bash
pip install -e ".[dev,mcp]"
```

### 3. Run tests

```bash
pytest
```

### 4. Run Crystal on itself

```bash
crystal check .
```

### 5. Make your changes

### 6. Submit a pull request

## Adding Stack Rules

Rules live in `src/crystal_guard/rules/builtin/` as YAML files. Here's the format:

```yaml
meta:
  name: "Your Stack Name"
  stack_id: "your-stack-id"
  description: "What this stack is"
  version: "1.0.0"

architecture:
  frontend:
    root: "src"
    expected_dirs:
      - path: "components"
        description: "UI components"
        optional: true
  shared:
    required_files:
      - ".gitignore"
    recommended_files:
      - "README.md"

domain_purity:
  frontend:
    file_patterns:
      - "src/**/*.js"
    forbidden:
      - id: "dom-001"
        pattern: "your-regex-pattern"
        message: "What's wrong (plain English)"
        suggestion: "How to fix it"
        severity: "critical"

security:
  global:
    checks:
      - id: "sec-001"
        pattern: "pattern-to-match"
        message: "What's wrong"
        severity: "critical"

placeholders:
  global:
    checks:
      - id: "hyg-001"
        pattern: "\\bTODO\\b"
        message: "Unresolved TODO."
        severity: "low"
```

Save it as `src/crystal_guard/rules/builtin/your_stack_name.yaml`.

## Code Style

- Python: Follow existing patterns. We use type hints.
- Error messages: Write for someone who has never coded. No jargon.
- Commits: `feat(analyzer): add X`, `fix(security): resolve Y`, `docs(readme): update Z`

## Questions?

Open an issue or start a discussion on GitHub.
