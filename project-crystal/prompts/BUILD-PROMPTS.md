# Build Prompts — Copy-Paste Prompts for Each Component

These are ready-to-use prompts you can paste into any AI coding platform to build each component of Crystal. Each prompt is self-contained with all the context needed.

---

## PROMPT 1: Crystal Core — Stack Detector

```
Build a Python module called `detector.py` for the crystal-guard project.

Purpose: Auto-detect what tech stack a project uses by examining its files.

Requirements:
1. Function `detect_stack(project_path: str) -> dict` that returns:
   {
     "frontend": "react" | "nextjs" | "vue" | "angular" | "svelte" | null,
     "backend": "python-fastapi" | "python-flask" | "python-django" | "node-express" | "node-nest" | null,
     "database": "mongodb" | "postgresql" | "mysql" | "sqlite" | null,
     "stack_id": "react-python-mongo" | "nextjs-prisma" | etc,
     "confidence": "high" | "medium" | "low",
     "detected_from": ["package.json", "requirements.txt", ...]
   }

2. Detection logic (priority order):
   a. Check for .crystal/config.yaml first (explicit user config)
   b. Frontend: Check package.json for react/next/vue/angular/svelte
   c. Backend: Check for requirements.txt (Python), package.json scripts (Node)
   d. Database: Check dependencies for pymongo/mongoose/prisma/sqlalchemy
   e. Fallback to "generic" stack

3. Use only standard library + pathlib. No external dependencies.
4. Include type hints. Include docstrings.
5. Handle missing files gracefully (return null for undetected parts).

Example usage:
  result = detect_stack("/path/to/my/project")
  print(result["stack_id"])  # "react-python-mongo"
```

---

## PROMPT 2: Crystal Core — Architecture Analyzer

```
Build a Python module called `architecture.py` for the crystal-guard project.

Purpose: Validate that a project's file structure follows expected patterns for its detected stack.

Requirements:
1. Class `ArchitectureAnalyzer` with method `analyze(project_path: str, rules: dict) -> list[Issue]`

2. Issue dataclass:
   @dataclass
   class Issue:
       analyzer: str        # "architecture"
       severity: str        # "critical" | "high" | "medium" | "low"
       file: str           # file path relative to project root
       line: int | None    # line number if applicable
       rule_id: str        # e.g., "arch-001"
       message: str        # human-readable description
       suggestion: str     # how to fix it

3. Checks to implement:
   - Expected directories exist (e.g., React project should have src/components)
   - No unexpected files in project root (more than 10 config files = warning)
   - No deeply nested directories (>5 levels deep)
   - Test directory exists
   - .env.example exists if .env exists
   - .gitignore exists and includes node_modules/venv/.env
   - No duplicate functionality files (e.g., utils.js AND helpers.js AND common.js)

4. Rules come from YAML config (passed in as dict). Example rules structure:
   {
     "expected_dirs": ["src/components", "src/pages", "tests"],
     "max_root_files": 10,
     "max_depth": 5,
     "required_files": [".gitignore"],
     "recommended_files": [".env.example", "README.md"]
   }

5. Use pathlib for file operations. No external dependencies except PyYAML.
6. Return list of Issue objects sorted by severity (critical first).
```

---

## PROMPT 3: Crystal Core — Domain Purity Analyzer

```
Build a Python module called `domain.py` for the crystal-guard project.

Purpose: Check that files respect domain boundaries — frontend code shouldn't contain database queries, backend routes shouldn't contain business logic, etc.

Requirements:
1. Class `DomainAnalyzer` with method `analyze(project_path: str, rules: dict) -> list[Issue]`

2. Uses same Issue dataclass as architecture analyzer.

3. Checks to implement:
   For frontend files (src/**/*.js, src/**/*.jsx, src/**/*.tsx):
   - No database patterns: mongoose, MongoClient, pymongo, prisma.client, SQL queries
   - No filesystem access: fs.readFile, os.path, pathlib
   - No server-only patterns: express, fastapi, flask
   - Environment vars must use REACT_APP_ prefix (or NEXT_PUBLIC_ for Next.js)

   For backend route files (routes/**/*.py, routes/**/*.js):
   - Should delegate to service functions, not contain business logic
   - No direct database queries (should go through models/services)
   - Flag functions longer than 50 lines (likely contains business logic)

   For model files (models/**/*.py, models/**/*.js):
   - Should only contain data definitions
   - No HTTP request handling
   - No business logic (complex conditional chains)

4. Pattern matching: Use regex on file contents. Patterns come from rules YAML:
   {
     "frontend": {
       "forbidden_patterns": [
         {"pattern": "MongoClient|mongoose\\.connect", "message": "Database access in frontend", "severity": "critical"},
         {"pattern": "fs\\.readFile|fs\\.writeFile", "message": "Filesystem access in frontend", "severity": "high"}
       ]
     },
     "backend_routes": {
       "forbidden_patterns": [...],
       "max_function_lines": 50
     }
   }

5. Be smart about false positives:
   - Ignore patterns in comments
   - Ignore patterns in string literals that are clearly documentation
   - Ignore test files
```

---

## PROMPT 4: Crystal Core — Security Analyzer

```
Build a Python module called `security.py` for the crystal-guard project.

Purpose: Detect common security issues in AI-generated code — hardcoded secrets, vulnerable patterns, exposed sensitive data.

Requirements:
1. Class `SecurityAnalyzer` with method `analyze(project_path: str, rules: dict) -> list[Issue]`

2. Checks to implement:
   a. Hardcoded API Keys (severity: CRITICAL)
      Patterns: api_key = "...", apiKey: "...", API_KEY = "..."
      Also check for known formats: sk-..., pk_..., ghp_..., AKIA...
   
   b. Hardcoded Passwords (severity: CRITICAL)
      Patterns: password = "...", passwd = "...", secret = "..."
   
   c. Exposed .env (severity: CRITICAL)
      Check: .env is not in .gitignore
   
   d. CORS Wildcard (severity: HIGH)
      Pattern: cors(origin: "*") or allow_origins=["*"]
      Note: Only flag in production configs, not dev
   
   e. SQL Injection Vectors (severity: HIGH)
      Pattern: f"SELECT...{variable}" or "SELECT..." + variable
   
   f. No Password Hashing (severity: HIGH)
      If auth code exists, check for bcrypt/argon2/pbkdf2
   
   g. Sensitive Data in Logs (severity: MEDIUM)
      Pattern: console.log(password) or print(api_key)
   
   h. HTTP instead of HTTPS (severity: MEDIUM)
      Pattern: http:// in production URLs (not localhost)

3. Scan ALL files except: node_modules, venv, .git, build, dist, __pycache__
4. Report exact file and line number for each finding.
5. Reduce false positives: skip comments, skip .env.example files, skip test fixtures.
```

---

## PROMPT 5: Crystal Core — Health Scorer

```
Build a Python module called `health.py` for the crystal-guard project.

Purpose: Calculate an overall health score (A-F) from analyzer results and generate a plain-English summary.

Requirements:
1. Function `calculate_health(issues: list[Issue]) -> HealthReport`

2. HealthReport dataclass:
   @dataclass
   class HealthReport:
       score: int           # 0-100
       grade: str           # A, B, C, D, F
       summary: str         # Plain English summary
       breakdown: dict      # Score per category
       critical_count: int
       high_count: int
       medium_count: int
       low_count: int
       top_issues: list     # Top 5 most important issues to fix

3. Scoring algorithm:
   Start at 100. Subtract per issue:
   - CRITICAL: -15 points
   - HIGH: -8 points
   - MEDIUM: -4 points
   - LOW: -2 points
   Minimum: 0

4. Grade thresholds:
   A: 90-100, B: 75-89, C: 60-74, D: 40-59, F: 0-39

5. Summary generation (plain English, for non-coders):
   Grade A: "Your project has excellent structure. Ship with confidence."
   Grade B: "Your project is well-structured with minor issues. Quick fixes recommended."
   Grade C: "Your project needs attention. {critical_count} critical issues found."
   Grade D: "Significant structural problems detected. Fix before deploying."
   Grade F: "Critical issues found. Do not deploy until resolved."
   
   Then add top issue descriptions.

6. Breakdown shows score per analyzer:
   {"architecture": 28/30, "domain": 22/25, "security": 20/25, ...}
```

---

## PROMPT 6: Crystal CLI

```
Build the CLI for crystal-guard using Python + Typer + Rich.

Requirements:
1. Entry point: crystal_guard/cli.py
2. Commands:
   
   crystal init
   - Auto-detect stack using detector.py
   - Create .crystal/ directory with config.yaml and rules.yaml
   - Print: "Crystal initialized for [stack]. Run 'crystal check' to analyze."
   
   crystal check [--format terminal|json|markdown] [--severity critical|high|medium|all]
   - Load config from .crystal/
   - Run all analyzers
   - Calculate health score
   - Output in chosen format (default: terminal)
   - Terminal output: use Rich for colors and formatting
   - Return exit code 1 if issues above severity threshold
   
   crystal status
   - Quick health dashboard (Rich panel)
   - Score, grade, issue counts, last check time
   
   crystal report --output report.md
   - Generate detailed markdown report
   
3. Terminal output style:
   Use Rich library for:
   - Green check marks for passes
   - Red X for failures
   - Yellow warnings
   - Progress bar during analysis
   - Panel with health score
   - Table for issues
   
4. Dependencies: typer, rich, pyyaml
5. The CLI should work even if .crystal/ doesn't exist (crystal check without init should auto-detect and run with defaults, printing a suggestion to run init for customization)
```

---

## PROMPT 7: Crystal MCP Server

```
Build an MCP server for crystal-guard using FastMCP (Python).

Requirements:
1. File: crystal_guard/mcp/server.py
2. Uses FastMCP to expose Crystal's analysis as MCP tools

3. Tools to expose:
   @mcp.tool() check_architecture(project_path: str) -> str
   @mcp.tool() check_domain_purity(file_path: str) -> str
   @mcp.tool() validate_file_placement(file_path: str, purpose: str) -> str
   @mcp.tool() get_project_context() -> str
   @mcp.tool() get_health_score() -> str
   @mcp.tool() update_prd(section: str, content: str) -> str

4. Resources to expose:
   @mcp.resource("crystal://prd") -> project requirements doc
   @mcp.resource("crystal://rules") -> architecture rules
   @mcp.resource("crystal://health") -> latest health data

5. The MCP server uses the same crystal_guard core modules internally.
6. Project path comes from:
   a. Environment variable CRYSTAL_PROJECT_PATH
   b. Current working directory (fallback)
   
7. Entry point for running:
   crystal mcp serve  (CLI subcommand)
   Or: python -m crystal_guard.mcp.server

8. Transport: stdio (default) or http (--transport http --port 8080)
```

---

## PROMPT 8: GitHub Actions Workflow

```
Create a GitHub Actions workflow file for Crystal CI/CD gates.

File: .github/workflows/crystal.yml

Requirements:
1. Triggers on: push to main, pull requests to main
2. Steps:
   a. Checkout code
   b. Set up Python 3.11
   c. Install crystal-guard (pip install crystal-guard)
   d. Run crystal init --ci (auto-detect, no interactive prompts)
   e. Run crystal check --format json --output crystal-report.json
   f. Generate markdown report: crystal report --input crystal-report.json --output crystal-report.md
   g. If PR: Comment the report on the PR using github-script
   h. If health score below threshold: exit 1 (fail the check)
   
3. Make it a reusable action that users can copy to their repos
4. Include comments explaining each step
5. Keep it simple — one job, sequential steps
```

---

## PROMPT 9: Landing Page

```
Build a single-page landing site for Project Crystal.

Requirements:
- Static HTML + CSS + minimal JS
- Dark, terminal-inspired theme
- Monospace font for code sections
- Green accent color (#00ff41 terminal green)
- Mobile responsive but desktop-first

Sections (in order):
1. HERO:
   - "Project Crystal" (large)
   - Tagline: "The building inspector for vibe-coded projects"
   - Subtitle: "Open-source MCP servers + CI/CD gates that keep AI-generated code structurally sound"
   - Two buttons: "Get Started" (links to GitHub) + "View on GitHub" (star count)

2. PROBLEM (stats strip):
   - "36% of vibe coders skip QA"
   - "1.7x more logic errors in AI code"
   - "45% contain security vulnerabilities"
   - "63% spend more time debugging than writing"

3. HOW IT WORKS:
   Three columns:
   a. "During Coding" - MCP Guardian watches your AI assistant
   b. "Before Deploy" - CLI runs local checks
   c. "On Every Push" - CI/CD gates block bad code

4. QUICK START:
   Terminal-style block:
   ```
   $ pip install crystal-guard
   $ crystal init
   $ crystal check
   ```
   Show example output with colored health score

5. FEATURES:
   Grid of 6 cards:
   - Architecture Validation
   - Domain Purity
   - Security Scanning
   - Dependency Audit
   - Session Memory
   - CI/CD Gates

6. USE CASES:
   Three scenarios:
   - "Solo Vibe Coder" — protect your passion project
   - "Team Projects" — consistent architecture across sessions
   - "Open Source" — quality gates for community contributions

7. COMMANDS:
   Table of CLI commands with descriptions

8. FOOTER:
   - Open source MIT license
   - GitHub link
   - "Built for the vibe coding community"

No JavaScript frameworks. Pure HTML/CSS. Use CSS Grid/Flexbox.
Fonts: JetBrains Mono for code, system sans-serif for body.
```

---

## PROMPT 10: README.md for GitHub

```
Write the README.md for the crystal-guard GitHub repository.

Structure:
1. Logo/banner (use ASCII art or simple text)
2. One-line description + badges (PyPI version, license, GitHub stars)
3. "What is Crystal?" — 3-sentence explanation
4. "The Problem" — brief stats
5. "Quick Start" — 4-line install + init + check
6. "What Crystal Checks" — table of all check categories
7. "MCP Server Setup" — config for Cursor, Claude Desktop, VS Code
8. "CI/CD Setup" — copy the workflow file
9. "Configuration" — .crystal/config.yaml reference
10. "Custom Rules" — how to add your own rules
11. "Supported Stacks" — table of auto-detected stacks
12. "Contributing" — link to CONTRIBUTING.md
13. "License" — MIT
14. "Star History" — placeholder

Keep it scannable. Use code blocks. Use tables. Link to docs/ for details.
Maximum 300 lines. Non-coders should understand it.
```

---

## Usage Notes

Each prompt above is designed to be:
1. **Self-contained** — Paste into any AI coding platform and get a working result
2. **Sequenced** — Build in order (1-10) as each builds on the previous
3. **Testable** — Each component can be tested independently
4. **Simple** — Uses minimal dependencies, avoids over-engineering

When building, create test fixtures first (good_project, bad_project) so you can verify each analyzer works correctly.
