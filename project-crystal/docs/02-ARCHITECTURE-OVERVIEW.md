# Architecture Overview — How Crystal Works

## System Diagram (Text)

```
+-----------------------------------------------+
|           USER'S VIBE CODING PLATFORM          |
|  (Cursor, Bolt, Lovable, Replit, Emergent...)  |
+------------------+----------------------------+
                   |
                   | MCP Protocol (stdio/http)
                   v
+------------------+----------------------------+
|          CRYSTAL MCP GUARDIAN SERVER           |
|                                                |
|  Tools:                                        |
|  - check_architecture()                        |
|  - check_domain_purity()                       |
|  - get_project_context()                       |
|  - validate_file_placement()                   |
|  - get_health_score()                          |
|  - suggest_fix()                               |
|                                                |
|  Resources:                                    |
|  - crystal://prd          (project status)     |
|  - crystal://rules        (architecture rules) |
|  - crystal://health       (health dashboard)   |
|                                                |
|  Prompts:                                      |
|  - crystal-review         (review changes)     |
|  - crystal-plan           (plan next feature)  |
+------------------+----------------------------+
                   |
                   | reads/writes
                   v
+------------------+----------------------------+
|            CRYSTAL PROJECT FILES               |
|                                                |
|  .crystal/                                     |
|    config.yaml      (project configuration)    |
|    rules.yaml       (architecture rules)       |
|    prd.md           (project requirements doc) |
|    sessions.log     (session history)           |
|    health.json      (latest health score)      |
+-----------------------------------------------+

+-----------------------------------------------+
|              CRYSTAL CLI                       |
|                                                |
|  crystal init     - Initialize in project      |
|  crystal check    - Run all validations        |
|  crystal status   - Show health dashboard      |
|  crystal rules    - List/edit rules            |
|  crystal fix      - Auto-fix simple issues     |
+------------------+----------------------------+
                   |
                   | triggers
                   v
+------------------+----------------------------+
|           CRYSTAL CI/CD GATES                  |
|          (GitHub Actions Workflow)              |
|                                                |
|  Gate 1: Architecture Check                    |
|  Gate 2: Domain Purity Check                   |
|  Gate 3: Security Scan                         |
|  Gate 4: Dependency Audit                      |
|  Gate 5: Placeholder Detection                 |
|  Gate 6: Health Score Threshold                |
|                                                |
|  Result: PASS/FAIL with report                 |
+-----------------------------------------------+
```

## Component Breakdown

### Component 1: Crystal MCP Guardian Server
**What**: A Python MCP server built with FastMCP that AI assistants connect to
**Why**: Provides real-time guidance DURING coding, not just after
**How it works**:
1. User configures their AI platform to connect to Crystal MCP
2. Crystal reads the project's `.crystal/` config to understand the rules
3. When AI generates or modifies code, Crystal can validate it
4. Crystal provides project context so AI understands what's been built

**Key Technical Decisions**:
- Built with FastMCP (Python SDK) — simplest, most documented approach
- Runs locally via stdio (for IDE-based platforms) or HTTP (for web platforms)
- Stateless per-request — reads `.crystal/` files for every check
- No external dependencies (no database, no cloud service)

### Component 2: Crystal CLI
**What**: A command-line tool for running checks manually
**Why**: Not all platforms support MCP; CLI works everywhere
**How it works**:
1. User installs: `pip install crystal-guard`
2. User initializes: `crystal init` (detects stack, creates `.crystal/`)
3. User checks: `crystal check` (runs all validations)
4. User gets a health report in plain English

**Key Technical Decisions**:
- Built with Python + Typer (modern CLI framework)
- Same validation engine as MCP server (shared core)
- Output is color-coded terminal + optional JSON for CI

### Component 3: Crystal CI/CD Gates
**What**: GitHub Actions workflow file that runs Crystal checks on every push
**Why**: Final safety net before deployment
**How it works**:
1. User copies `.github/workflows/crystal.yml` to their repo
2. On every push to main, Crystal checks run
3. If any check fails, merge/deploy is blocked
4. Clear report explains what's wrong and how to fix it

**Key Technical Decisions**:
- GitHub Actions (most common, free for public repos)
- Uses Crystal CLI internally
- Configurable severity levels (error = block, warning = allow)
- Can be extended with custom checks

### Component 4: Crystal Agent
**What**: A Python agent that uses Crystal MCP servers as tools for deeper analysis
**Why**: Some checks require multi-step reasoning (e.g., "is this feature complete?")
**How it works**:
1. Agent connects to Crystal MCP server
2. Can run comprehensive project audits
3. Generates detailed reports with actionable recommendations
4. Can be triggered manually or via CI/CD

**Key Technical Decisions**:
- Python-based, uses MCP client to connect to Crystal servers
- Optional — advanced feature for users who want deeper analysis
- Can work with any LLM backend (OpenAI, Anthropic, local models)

### Component 5: Landing Page
**What**: A simple informative website showcasing Crystal
**Why**: First impression, explains the project, links to GitHub
**Sections**: Hero, Problem, Solution, How It Works, Use Cases, Quick Start, GitHub CTA

## Shared Core: The Validation Engine

All components share the same validation logic:

```
crystal-core/
  analyzers/
    architecture.py    - File structure and organization checks
    domain.py          - Domain boundary enforcement
    security.py        - Security pattern detection
    dependencies.py    - Dependency audit
    placeholders.py    - TODO/FIXME/placeholder detection
    health.py          - Overall health scoring
  detectors/
    stack_detector.py  - Auto-detect project stack (React, Python, etc.)
    rule_loader.py     - Load rules from .crystal/rules.yaml
  reporters/
    terminal.py        - CLI output formatting
    json.py            - JSON output for CI
    markdown.py        - Markdown report generation
```

## Stack Rules Architecture

Crystal ships with built-in rules for common stacks:

```yaml
# Example: React + Python + MongoDB
stacks:
  react-python-mongo:
    frontend:
      allowed_dirs: [src/components, src/pages, src/hooks, src/utils, src/styles]
      forbidden_patterns:
        - pattern: "mongoose|mongodb|MongoClient"
          message: "Database access detected in frontend. Use API calls instead."
        - pattern: "process.env.(?!REACT_APP)"
          message: "Only REACT_APP_ environment variables are accessible in frontend."
    backend:
      allowed_dirs: [routes, services, models, utils, middleware]
      forbidden_patterns:
        - pattern: "useState|useEffect|React"
          message: "React code detected in backend."
      required_separation:
        routes: "Request handling only. Delegate to services."
        services: "Business logic. No direct route handling."
        models: "Data definitions. No business logic."
    security:
      forbidden_patterns:
        - pattern: 'api_key\s*=\s*["\'][a-zA-Z0-9]'
          message: "Hardcoded API key detected. Use environment variables."
        - pattern: 'password\s*=\s*["\']'
          message: "Hardcoded password detected."
```

Users can override/extend these rules in their `.crystal/rules.yaml`.
