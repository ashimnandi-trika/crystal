# Component Specifications

## Spec 1: Crystal Core (Validation Engine)

### Overview
The shared validation library used by CLI, MCP server, and CI/CD. This is the brain of Crystal.

### Package Structure
```
crystal_core/
  __init__.py
  config.py           # Load and validate .crystal/ configuration
  detector.py         # Auto-detect project stack
  
  analyzers/
    __init__.py
    base.py            # Base analyzer class
    architecture.py    # File structure validation
    domain.py          # Domain boundary checks
    security.py        # Security pattern scanning
    dependencies.py    # Dependency audit
    placeholders.py    # TODO/FIXME detection
    
  scoring/
    __init__.py
    health.py          # Calculate health score (A-F)
    
  rules/
    __init__.py
    loader.py          # Load rules from YAML
    builtin/
      react_python_mongo.yaml
      react_node_postgres.yaml
      nextjs_prisma.yaml
      python_fastapi_mongo.yaml
      generic.yaml      # Fallback rules
      
  reporters/
    __init__.py
    terminal.py        # Rich terminal output
    json_reporter.py   # JSON for CI/CD
    markdown.py        # Markdown for PR comments
```

### Stack Detection Logic
```
Priority order:
1. Check .crystal/config.yaml (explicit declaration)
2. Detect from files present:
   - package.json + src/App.js → React frontend
   - requirements.txt + server.py → Python backend
   - package.json + next.config.js → Next.js
   - package.json + angular.json → Angular
   - Gemfile → Ruby on Rails
   - go.mod → Go
   - Cargo.toml → Rust
3. Detect database from dependencies:
   - pymongo/mongoose → MongoDB
   - prisma → Prisma (Postgres/MySQL)
   - sqlalchemy → SQL database
4. Fallback to generic rules
```

### Health Scoring Algorithm
```
Score = weighted average of:
  Architecture Compliance:  30% weight
  Domain Purity:           25% weight
  Security:                25% weight
  Code Hygiene:            10% weight (placeholders, dead code)
  Dependency Health:       10% weight

Grades:
  A: 90-100  "Excellent structure. Ship with confidence."
  B: 75-89   "Good structure. Minor issues to address."
  C: 60-74   "Needs attention. Several structural issues."
  D: 40-59   "Significant problems. Fix before deploying."
  F: 0-39    "Critical issues. Do not deploy."

Each issue has severity:
  CRITICAL: -15 points (hardcoded secrets, direct DB in frontend)
  HIGH:     -8 points  (wrong layer, missing separation)
  MEDIUM:   -4 points  (minor domain violation)
  LOW:      -2 points  (placeholder, naming convention)
```

### Analyzer Details

#### Architecture Analyzer
```
Checks:
1. Expected directories exist (based on stack rules)
2. No unexpected files in root (configuration sprawl)
3. File naming conventions followed
4. No deeply nested directories (>5 levels)
5. No circular imports (via AST analysis)
6. Test directory exists
7. Environment files present (.env.example)

Output per issue:
{
  "analyzer": "architecture",
  "severity": "HIGH",
  "file": "src/App.js",
  "line": null,
  "message": "Project missing /tests directory. No test structure detected.",
  "suggestion": "Create a /tests directory and add basic tests for critical functions.",
  "rule": "arch-001"
}
```

#### Domain Purity Analyzer
```
Checks:
1. Frontend files don't contain backend patterns (DB queries, file system access)
2. Backend route files don't contain business logic (should delegate to services)
3. Model files don't contain business logic (should be pure data definitions)
4. No cross-layer imports (frontend importing backend modules)
5. Environment variables used correctly per layer
6. API calls from frontend go through proper fetch/axios patterns

Uses regex pattern matching on file contents, scoped by file location.
```

#### Security Analyzer
```
Checks:
1. Hardcoded API keys/secrets (regex: various API key patterns)
2. Hardcoded passwords
3. SQL injection patterns (string concatenation in queries)
4. Exposed .env files (not in .gitignore)
5. CORS set to wildcard (*) in production config
6. No rate limiting on auth endpoints
7. Plain-text password storage (no bcrypt/argon2)
8. Sensitive data in console.log/print statements
```

#### Dependency Analyzer
```
Checks:
1. Known vulnerabilities (uses safety/pip-audit for Python, npm audit for Node)
2. Outdated major versions
3. Unnecessary dependencies (detected but unused imports)
4. Duplicate functionality (e.g., both axios and fetch, both lodash and underscore)
5. License compatibility
```

#### Placeholder Analyzer
```
Checks:
1. TODO/FIXME comments
2. Placeholder values (example.com, test@test.com, lorem ipsum)
3. Console.log/print statements (debug leftovers)
4. Commented-out code blocks (>5 lines)
5. Hardcoded localhost URLs in non-dev files
```

---

## Spec 2: Crystal CLI

### Commands
```
crystal init [--stack react-python-mongo]
  - Detects project stack (or accepts explicit)
  - Creates .crystal/ directory with config
  - Creates .crystal/rules.yaml with stack defaults
  - Creates .crystal/prd.md template
  - Adds .crystal/ to .gitignore (optional)
  
crystal check [--format terminal|json|markdown] [--severity critical|high|medium|all]
  - Runs all analyzers
  - Outputs results in chosen format
  - Returns exit code 0 (pass) or 1 (fail based on severity threshold)

crystal status
  - Shows health score (A-F)
  - Shows issue count by severity
  - Shows last check timestamp
  - Plain-English project health summary

crystal rules [list|add|remove]
  - List active rules
  - Add custom rules
  - Remove/disable rules

crystal fix [--dry-run]
  - Auto-fix simple issues (e.g., add .env to .gitignore)
  - Dry-run shows what would be fixed
  - Only fixes LOW/MEDIUM severity with high confidence

crystal report [--output report.md]
  - Generate detailed markdown report
  - Suitable for sharing with team or attaching to PR
```

### Installation
```bash
pip install crystal-guard

# Or with pipx for isolated install
pipx install crystal-guard
```

### Configuration File (.crystal/config.yaml)
```yaml
project:
  name: "My App"
  stack: "react-python-mongo"  # auto-detected or manual
  
checks:
  architecture: true
  domain_purity: true
  security: true
  dependencies: true
  placeholders: true
  
severity_threshold: "high"  # fail on HIGH and CRITICAL only

custom_rules:
  - name: "no-inline-styles"
    pattern: 'style=\{?\{'
    files: "**/*.jsx"
    message: "Use CSS classes instead of inline styles."
    severity: "low"

ignore:
  files:
    - "node_modules/**"
    - "venv/**"
    - ".git/**"
    - "build/**"
    - "dist/**"
  rules:
    - "sec-003"  # Disable specific rule by ID
```

---

## Spec 3: Crystal MCP Server

### MCP Tools (what AI can call)

```python
@mcp.tool()
def check_architecture(project_path: str) -> str:
    """Check if the project follows proper file structure and organization.
    Returns issues found with suggestions for fixing them."""
    
@mcp.tool()
def check_domain_purity(file_path: str) -> str:
    """Check if a specific file respects domain boundaries.
    Example: frontend files shouldn't contain database queries."""
    
@mcp.tool()
def validate_file_placement(file_path: str, file_purpose: str) -> str:
    """Before creating a new file, validate it's being placed in the correct directory.
    Args: file_path (where AI wants to create it), file_purpose (what the file does)"""

@mcp.tool()
def get_project_context() -> str:
    """Get the current project status: what's been built, what's remaining,
    recent decisions, and the project's architecture rules."""

@mcp.tool()  
def get_health_score() -> str:
    """Get the project's current health score (A-F) with a summary of issues."""

@mcp.tool()
def suggest_fix(issue_id: str) -> str:
    """Get a detailed fix suggestion for a specific issue found during checks."""

@mcp.tool()
def update_prd(section: str, content: str) -> str:
    """Update the project requirements document after completing a feature
    or making an architectural decision."""
```

### MCP Resources (data AI can read)

```python
@mcp.resource("crystal://prd")
def get_prd() -> str:
    """The project requirements document - what's built, what's remaining."""

@mcp.resource("crystal://rules") 
def get_rules() -> str:
    """The architecture rules for this project."""

@mcp.resource("crystal://health")
def get_health() -> str:
    """Latest health check results in JSON."""

@mcp.resource("crystal://session-log")
def get_sessions() -> str:
    """Log of what was done in previous coding sessions."""
```

### MCP Prompts (templates for AI)

```python
@mcp.prompt("crystal-review")
def review_prompt() -> str:
    """Review recent changes against project architecture rules."""
    return """Review the recent changes in this project against Crystal's architecture rules.
    Check: {check_results}
    Rules: {rules}
    Provide specific, actionable feedback."""

@mcp.prompt("crystal-plan")
def plan_prompt() -> str:
    """Plan the next feature with architecture awareness."""
    return """Based on the project's current state and architecture:
    PRD: {prd}
    Health: {health}
    Rules: {rules}
    Plan the implementation of the next feature while maintaining architectural integrity."""
```

### Client Configuration Examples

#### Cursor (.cursor/mcp.json)
```json
{
  "mcpServers": {
    "crystal": {
      "command": "crystal",
      "args": ["mcp", "serve"],
      "env": {
        "CRYSTAL_PROJECT_PATH": "."
      }
    }
  }
}
```

#### Claude Desktop (claude_desktop_config.json)
```json
{
  "mcpServers": {
    "crystal": {
      "command": "crystal",
      "args": ["mcp", "serve"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

#### VS Code / Windsurf
```json
{
  "mcp": {
    "servers": {
      "crystal": {
        "type": "stdio",
        "command": "crystal",
        "args": ["mcp", "serve"]
      }
    }
  }
}
```

---

## Spec 4: Crystal CI/CD Gates

### GitHub Actions Workflow (.github/workflows/crystal.yml)
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
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install Crystal
        run: pip install crystal-guard
        
      - name: Initialize Crystal (if needed)
        run: crystal init --ci
        
      - name: Run Crystal Checks
        run: crystal check --format json --output crystal-report.json
        
      - name: Generate Report
        if: always()
        run: crystal report --input crystal-report.json --output crystal-report.md
        
      - name: Comment on PR
        if: github.event_name == 'pull_request'
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
            echo "Crystal checks failed. See report for details."
            exit 1
          fi
```

### What Each Gate Checks
```
Gate 1 - Architecture:    File structure matches expected patterns
Gate 2 - Domain Purity:   No cross-layer violations
Gate 3 - Security:        No hardcoded secrets or vulnerable patterns
Gate 4 - Dependencies:    No known vulnerabilities or unnecessary packages
Gate 5 - Code Hygiene:    No TODO/FIXME/placeholder in production code
Gate 6 - Health Score:    Overall score meets minimum threshold (configurable)
```

---

## Spec 5: Crystal Agent

### Overview
An AI agent that uses Crystal MCP tools for deeper, multi-step analysis.

### Capabilities
1. **Full Project Audit**: Runs all checks, correlates issues, produces comprehensive report
2. **Feature Completeness Check**: Compares PRD with actual implementation
3. **Refactoring Suggestions**: Identifies consolidation opportunities
4. **Migration Guide**: When architecture needs restructuring, generates step-by-step plan

### Implementation
```python
# Uses any LLM (OpenAI, Anthropic, local) + Crystal MCP as tools
# The agent is a thin orchestration layer — Crystal MCP does the real work

class CrystalAgent:
    def __init__(self, llm_provider, crystal_mcp_client):
        self.llm = llm_provider
        self.crystal = crystal_mcp_client
    
    async def audit(self, project_path: str) -> AuditReport:
        """Run comprehensive project audit"""
        context = await self.crystal.get_project_context()
        health = await self.crystal.get_health_score()
        architecture = await self.crystal.check_architecture(project_path)
        
        # Use LLM to synthesize findings into actionable report
        report = await self.llm.analyze(context, health, architecture)
        return report
```

---

## Spec 6: Landing Page

### Sections (in order)
1. **Hero**: Project Crystal logo/name + tagline + GitHub star button + "Get Started" CTA
2. **Problem**: "The vibe coding quality crisis" — 3-4 stats with visual treatment
3. **Solution**: "Crystal is your building inspector" — 3 pillars (MCP, CLI, CI/CD)
4. **How It Works**: 3-step flow diagram (Install -> Init -> Check)
5. **Quick Start**: Terminal-style code block showing installation and first check
6. **Use Cases**: 3 cards (Solo Vibe Coder, Team Projects, CI/CD Pipeline)
7. **Commands Reference**: Table of CLI commands
8. **Open Source**: GitHub CTA + contribution invitation
9. **Footer**: License, links, credits

### Design Direction
- Dark terminal-inspired background
- Monospace accents for code/commands
- Minimal color palette: dark bg, green accents (like terminal output), white text
- No fancy animations — clean, informative, developer-trusted aesthetic
- Mobile responsive but desktop-first (developers browse on desktop)
