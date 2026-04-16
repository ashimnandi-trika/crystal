# Session Workflow — How Crystal Fits Into a Vibe Coding Session

## The User Journey (No Code Knowledge Required)

### First Time Setup (Once)
```
Step 1: User installs Crystal
        $ pip install crystal-guard

Step 2: User navigates to their project
        $ cd my-awesome-app

Step 3: User initializes Crystal
        $ crystal init
        
        Output:
        Detected stack: React + Python + MongoDB
        Created .crystal/ configuration
        Loaded 24 rules for your stack
        Run 'crystal check' to analyze your project
```

### Every Coding Session
```
Before coding:
        $ crystal status
        
        Output:
        Project: my-awesome-app
        Health: B (82/100)
        Last check: 2 hours ago
        Open issues: 3 medium, 1 low

During coding (if using MCP-enabled platform):
        Crystal MCP automatically provides context:
        - "Here's what was built last session"
        - "This file should go in /backend/services/"
        - "Warning: this pattern is a security risk"

After coding:
        $ crystal check
        
        Output:
        Running 6 analyzers...
        
        Architecture  [PASS] 
        Domain Purity [PASS] 
        Security      [1 issue found]
        Dependencies  [PASS] 
        Placeholders  [2 issues found]
        
        HEALTH SCORE: B (78/100)
        
        Issues:
        [CRITICAL] sec-003: API key pattern found in src/config.js:15
                   Remove this key and use .env instead
        [LOW]      hyg-001: TODO comment in backend/services/payment.py:42
        [LOW]      hyg-003: console.log in frontend/src/App.js:88
        
        Fix critical issues before deploying.
        Run 'crystal fix --dry-run' for auto-fix suggestions.
```

### On Git Push (if CI/CD configured)
```
Push to GitHub → Crystal GitHub Action runs → PR gets comment:

  Crystal Health Report
  
  Grade: B (78/100)
  
  1 Critical Issue:
  - Hardcoded API key in src/config.js:15
  
  Action Required: Fix critical issues before merging.
```

---

## Session Continuity — The PRD File

### What is .crystal/prd.md?
A living document that Crystal maintains to track project state across sessions.

### Structure:
```markdown
# My Awesome App — Crystal PRD

## Project Overview
E-commerce app with user auth, product catalog, and checkout.

## What's Been Built
- [x] User authentication (login, register, password reset)
- [x] Product listing page
- [x] Product detail page
- [x] Shopping cart
- [ ] Checkout flow
- [ ] Payment integration
- [ ] Order history

## Architecture Decisions
- Using JWT for authentication (decided Session 2)
- MongoDB for all data storage
- Stripe for payments (planned)

## Current Issues
- Cart doesn't persist on page reload (Session 3)
- Product images loading slow (Session 4)

## Session Log
### Session 5 (Jan 15, 2026)
- Added product filtering by category
- Fixed cart persistence issue
- Crystal Health: B (82/100)

### Session 4 (Jan 14, 2026)  
- Added product detail page
- Image upload for products
- Crystal Health: C (68/100) — fixed 2 security issues
```

### How It's Updated:
1. **MCP Server**: AI assistant calls `update_prd()` after completing features
2. **CLI**: `crystal check` updates the health score and session log
3. **Manual**: Users can edit it directly (it's just a markdown file)

### Why This Matters:
- Next session, the AI assistant reads the PRD and knows exactly where things stand
- No more re-explaining what was built
- No more conflicting implementations across sessions
- Clear visibility into project progress

---

## Integration Points — How Crystal Connects

### With Cursor
```json
// .cursor/mcp.json
{
  "mcpServers": {
    "crystal-guard": {
      "command": "crystal",
      "args": ["mcp", "serve"]
    }
  }
}
```
Cursor's AI now has access to Crystal tools. When composing code, it can:
- Check if a file is in the right location
- Read the PRD for context
- Validate architecture before writing

### With Windsurf
```json
// .windsurfrules or MCP config
{
  "mcp": {
    "servers": {
      "crystal-guard": {
        "type": "stdio",
        "command": "crystal",
        "args": ["mcp", "serve"]
      }
    }
  }
}
```

### With Claude Desktop
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "crystal-guard": {
      "command": "crystal",
      "args": ["mcp", "serve"],
      "cwd": "/path/to/project"
    }
  }
}
```

### With GitHub Actions
Copy `.github/workflows/crystal.yml` to your repo. Done.

### With Any Platform (CLI Fallback)
If the platform doesn't support MCP:
```
$ crystal check
```
Just run it manually before deploying.
