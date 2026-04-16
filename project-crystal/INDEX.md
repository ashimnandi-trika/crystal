# Project Crystal — Master Document Index

## What Is This?
This is the complete strategic foundation for Project Crystal — an open-source architecture guardian for vibe-coded projects. Every document here was researched, organized, and written to ensure systematic, consistent building.

## Document Map

### Strategic Documents (Read First)
| # | Document | Purpose |
|---|----------|---------|
| 00 | [Executive Summary](docs/00-EXECUTIVE-SUMMARY.md) | 5-minute overview of what Crystal is and why it matters |
| 01 | [Problem Deep Dive](docs/01-PROBLEM-DEEP-DIVE.md) | The 7 problems Crystal solves, with data |
| 07 | [Recommendations](docs/07-RECOMMENDATIONS.md) | Strategic analysis, risks, launch plan |

### Architecture Documents (Reference During Build)
| # | Document | Purpose |
|---|----------|---------|
| 02 | [Architecture Overview](docs/02-ARCHITECTURE-OVERVIEW.md) | System diagram, component breakdown, shared core |
| 04 | [Component Specs](docs/04-COMPONENT-SPECS.md) | Detailed specs for each component (CLI, MCP, CI/CD, Agent) |
| 05 | [GitHub Repo Structure](docs/05-GITHUB-REPO-STRUCTURE.md) | File-by-file repo layout with pyproject.toml |

### Build Documents (Use During Implementation)
| # | Document | Purpose |
|---|----------|---------|
| 03 | [Phased Delivery Plan](docs/03-PHASED-DELIVERY-PLAN.md) | What to build and in what order |
| 06 | [Consistency Rules](docs/06-CONSISTENCY-RULES.md) | Naming, formatting, testing standards |
| 08 | [Session Workflow](docs/08-SESSION-WORKFLOW.md) | How Crystal fits into a user's workflow |

### Specifications
| Document | Purpose |
|----------|---------|
| [Rules Specification](specs/RULES-SPECIFICATION.md) | Complete YAML rule definitions for all stacks |

### Build Prompts
| Document | Purpose |
|----------|---------|
| [Build Prompts](prompts/BUILD-PROMPTS.md) | 10 copy-paste prompts to build each component |

## Build Order
```
Phase 0: [CURRENT] Strategic foundation + Landing page
Phase 1: Crystal Core + CLI (stack detection, analyzers, health scoring)
Phase 2: Crystal MCP Server (FastMCP, tools, resources)
Phase 3: Crystal CI/CD Gates (GitHub Actions workflow)
Phase 4: Crystal Agent (AI-powered deep analysis)
Phase 5: Polish & Launch (PyPI, README, marketing)
```

## Key Decisions Made
1. Python for everything (FastMCP, Typer CLI, pytest)
2. YAML for rules (accessible to non-coders, easy to contribute)
3. GitHub Actions for CI/CD (free, widely used)
4. MCP via FastMCP (simplest Python implementation)
5. No external dependencies for core (no database, no cloud)
6. MIT license (maximum adoption)
7. Monorepo (everything in one GitHub repo)

## How To Use This
1. Read Executive Summary first
2. Read Recommendations for strategic context
3. Follow Phased Delivery Plan for build order
4. Use Build Prompts when building each component
5. Reference Component Specs for implementation details
6. Follow Consistency Rules for code quality
7. Check Rules Specification for YAML formats
