# GitHub Repository Structure

## Repository Name
`crystal-guard` (or `project-crystal`)

## Why `crystal-guard`?
- Clear what it does (guards your project)
- Available as pip package name
- Short, memorable
- "Crystal" conveys transparency/clarity

## Repository Structure

```
crystal-guard/
│
├── README.md                          # Main README with overview, install, quick start
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # How to contribute
├── CODE_OF_CONDUCT.md                # Community guidelines
├── CHANGELOG.md                      # Version history
├── pyproject.toml                    # Python package configuration
├── setup.cfg                         # Package metadata
├── Makefile                          # Common development commands
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Run tests on PR
│   │   ├── release.yml               # Publish to PyPI on tag
│   │   └── crystal.yml               # Crystal checks itself (dogfooding)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── new_stack_rules.md        # Request rules for a new stack
│   └── PULL_REQUEST_TEMPLATE.md
│
├── src/
│   └── crystal_guard/
│       ├── __init__.py               # Version, public API
│       ├── cli.py                    # CLI entry point (Typer)
│       ├── config.py                 # Configuration management
│       ├── detector.py               # Stack auto-detection
│       │
│       ├── analyzers/
│       │   ├── __init__.py
│       │   ├── base.py               # Base analyzer class
│       │   ├── architecture.py       # File structure checks
│       │   ├── domain.py             # Domain boundary checks
│       │   ├── security.py           # Security scanning
│       │   ├── dependencies.py       # Dependency audit
│       │   └── placeholders.py       # Placeholder detection
│       │
│       ├── scoring/
│       │   ├── __init__.py
│       │   └── health.py             # Health score calculator
│       │
│       ├── rules/
│       │   ├── __init__.py
│       │   ├── loader.py             # YAML rule loader
│       │   └── builtin/
│       │       ├── react_python_mongo.yaml
│       │       ├── react_node_postgres.yaml
│       │       ├── nextjs_prisma.yaml
│       │       ├── python_fastapi.yaml
│       │       └── generic.yaml
│       │
│       ├── reporters/
│       │   ├── __init__.py
│       │   ├── terminal.py           # Rich terminal output
│       │   ├── json_reporter.py      # JSON output
│       │   └── markdown.py           # Markdown output
│       │
│       ├── mcp/
│       │   ├── __init__.py
│       │   └── server.py             # MCP server (FastMCP)
│       │
│       └── agent/
│           ├── __init__.py
│           └── agent.py              # Crystal Agent
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Shared fixtures
│   ├── test_detector.py
│   ├── test_architecture.py
│   ├── test_domain.py
│   ├── test_security.py
│   ├── test_dependencies.py
│   ├── test_placeholders.py
│   ├── test_health.py
│   ├── test_cli.py
│   ├── test_mcp_server.py
│   └── fixtures/
│       ├── good_project/             # A well-structured project
│       ├── bad_project/              # A poorly-structured project
│       └── mixed_project/            # Some good, some bad
│
├── examples/
│   ├── react-python-mongo/           # Example project with Crystal
│   ├── nextjs-prisma/                # Example project with Crystal
│   └── crystal-ci-cd/               # Example GitHub Actions setup
│
├── docs/
│   ├── getting-started.md
│   ├── configuration.md
│   ├── rules-reference.md
│   ├── mcp-setup.md
│   ├── ci-cd-setup.md
│   ├── custom-rules.md
│   ├── contributing-rules.md
│   └── faq.md
│
└── landing-page/
    ├── index.html                    # Single-page landing site
    ├── styles.css
    └── assets/
```

## pyproject.toml
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "crystal-guard"
version = "0.1.0"
description = "Architecture guardian for vibe-coded projects"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
keywords = ["mcp", "architecture", "code-quality", "vibe-coding", "ai-coding"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Quality Assurance",
]
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
    "fastmcp>=0.1.0",
]

[project.optional-dependencies]
agent = ["openai>=1.0.0", "anthropic>=0.20.0"]
dev = ["pytest>=7.0", "ruff>=0.1.0", "mypy>=1.0"]

[project.scripts]
crystal = "crystal_guard.cli:app"

[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/crystal-guard"
Documentation = "https://crystal-guard.dev"
Repository = "https://github.com/YOUR_USERNAME/crystal-guard"
```

## Key Design Decisions

### 1. Monorepo
Everything in one repo — CLI, MCP server, agent, rules, docs, landing page. Simpler for contributors and users.

### 2. src/ layout
Using `src/crystal_guard/` (not flat `crystal_guard/`) to prevent import confusion during development.

### 3. Built-in Rules as YAML
Rules are YAML files, not Python code. This means:
- Non-coders can read and understand rules
- Easy to contribute new rules without Python knowledge
- Rules can be shared, copied, modified independently

### 4. Test Fixtures
Real project structures (good, bad, mixed) as test fixtures. This makes testing intuitive and comprehensive.

### 5. Examples Directory
Complete example projects showing Crystal in action. Users can clone and try immediately.
