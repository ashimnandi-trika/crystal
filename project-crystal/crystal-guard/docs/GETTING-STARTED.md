# Getting Started with Crystal

This guide walks you through setting up Crystal from scratch.

## Step 1: Install

```bash
pip install crystal-code
```

That's it. Crystal is now available as the `crystal` command.

## Step 2: Go to your project

```bash
cd /path/to/your/project
```

## Step 3: Initialize

```bash
crystal init
```

Crystal looks at your project files and figures out what stack you're using (React, Python, Node, etc.). It creates a `.crystal/` folder with your configuration.

## Step 4: Check your project

```bash
crystal check
```

You'll see a health score from A to F and a list of any issues found.

## Step 5: Fix issues

If Crystal found issues, run:

```bash
crystal fix-prompt
```

This generates paste-ready prompts you can copy into your AI coding tool. Each prompt explains what's wrong, why it matters, and exactly how to fix it.

## Step 6: Set up session handoff

At the end of every coding session, run:

```bash
crystal handoff --output handoff.md
```

Next time you open your AI tool, paste the contents of `handoff.md`. The AI will know exactly where you left off.

## Step 7 (optional): Connect to your AI tool

If your AI tool supports MCP (Cursor, Claude Desktop, VS Code), Crystal can provide real-time guidance while you code.

Create `.cursor/mcp.json` in your project:

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

Restart your AI tool. Crystal tools are now available.

## Step 8 (optional): Add CI/CD

Copy the workflow file to your repo:

```bash
mkdir -p .github/workflows
```

Create `.github/workflows/crystal.yml` with the content from our [CI/CD setup guide](CI-CD-SETUP.md).

Every push will now be checked automatically.

## What to do every session

1. **Start**: Paste your last `handoff.md` into the AI
2. **Build**: Code normally. Crystal MCP guides in real-time (if configured).
3. **Check**: Run `crystal check` before pushing
4. **Fix**: Run `crystal fix-prompt` if issues found
5. **End**: Run `crystal handoff --output handoff.md`

That's the full workflow. Five steps. Repeat every session.
