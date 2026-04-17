# MCP Server Setup Guide

Crystal's MCP server lets your AI coding assistant access quality tools **while it codes**.
The AI can check architecture, validate file placement, and read project context in real-time.

## Quick Setup

### Cursor

Create `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "crystal": {
      "command": "crystal",
      "args": ["mcp", "serve"]
    }
  }
}
```

Restart Cursor. Crystal tools are now available to the AI.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or
`%APPDATA%/Claude/claude_desktop_config.json` (Windows):

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

Restart Claude Desktop.

### VS Code / Windsurf

Add to your settings or MCP config:

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

### HTTP Transport (for web-based tools)

```bash
crystal mcp serve --transport http --port 8080
```

Then connect your tool to `http://localhost:8080`.

## Available Tools

Once connected, your AI assistant can call these tools:

| Tool | What it does |
|------|-------------|
| `check_architecture` | Validates file structure and organization |
| `check_domain_purity` | Checks if files respect domain boundaries |
| `check_security` | Scans for hardcoded secrets and vulnerabilities |
| `run_all_checks` | Runs all 20 quality gates at once |
| `validate_file_placement` | Checks if a new file is going in the right place |
| `get_project_context` | Gets project state, PRD, git info for context |
| `get_health_score` | Quick health score (A-F) |
| `update_prd` | Updates the project requirements document |

## Available Resources

| Resource | Content |
|----------|---------|
| `crystal://health` | Latest health check results |
| `crystal://rules` | Architecture rules (architecture.md) |
| `crystal://prd` | Project requirements document |

## How the AI Uses It

When Crystal MCP is connected, your AI assistant can:

1. **Before writing code**: Call `get_project_context` to understand what's been built
2. **Before creating a file**: Call `validate_file_placement` to check it's in the right directory
3. **After making changes**: Call `run_all_checks` to verify nothing broke
4. **At session end**: Call `update_prd` to record what was built

The AI does this automatically — you don't need to ask it.
