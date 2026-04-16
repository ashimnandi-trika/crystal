# Crystal — Growth Strategy: Finding First 100 Users

## Who We're Looking For

**Primary**: Non-technical people building apps with AI tools (Cursor, Bolt, Lovable, Replit, Emergent)
**Secondary**: Technical developers using AI who want automated guardrails
**Where they are**: Reddit, Twitter/X, Discord communities, YouTube, Hacker News

---

## Phase 1: Seed Users (Week 1-2) — Get 10 users

### Action 1: Reddit Posts (Day 1)
Post in these subreddits with genuine, helpful content (not spammy):

**r/vibecoding** (most relevant)
> Title: "I built a CLI that checks your vibe-coded project for issues before you ship"
> Content: Share the case study. Show before/after. Link to GitHub.

**r/cursor** (Cursor users)
> Title: "Made a tool that gives your Cursor AI context about what you built last session"
> Content: Focus on the handoff feature. Show how it solves the "start from zero" problem.

**r/webdev** (broader audience)
> Title: "Open source tool that catches hardcoded API keys, wrong file placement, and missing tests in AI-generated code"
> Content: Focus on the 15 gates. Show real output.

**r/SideProject** (builders)
> Title: "My AI kept breaking old features every session, so I built this"
> Content: Personal story + the tool.

### Action 2: Twitter/X Thread (Day 2)
Write a thread:
```
I build apps with AI. Here's the problem nobody talks about:

Every new session, the AI starts from zero.
It rewrites files that work. It puts database code in the frontend.
It hardcodes API keys. It breaks old features.

So I built Crystal. [thread 🧵]
```
Tag: @cursor_ai @lovaborhq @replitapp @emergaborhq
Hashtags: #vibecoding #buildinpublic #opensource

### Action 3: Hacker News — Show HN (Day 3)
> Title: "Show HN: Crystal – CLI that checks AI-generated code for architectural issues"
> Link: GitHub repo
> Comment: Explain the problem, show the case study, mention it's open source MIT

### Action 4: Discord Communities (Day 4-5)
Join and contribute (don't just spam):
- **Cursor Discord** — Share in their tools/plugins channel
- **Claude Discord** — Share as an MCP tool
- **Bolt.new Discord** — Share as a quality tool
- **Lovable Discord** — Same
- **Indie Hackers Discord** — Share as a side project

---

## Phase 2: Content (Week 2-4) — Get 50 users

### Action 5: YouTube Demo Video (3 minutes)
Record a terminal screencast:
1. Show a messy project (the case study "before")
2. Run `crystal init && crystal check` — show the F score
3. Run `crystal fix-prompt` — show the paste-ready prompts
4. Fix one issue live
5. Re-check — score improves
6. End with `crystal handoff`

Title: "This CLI saved my vibe-coded project from disaster"
Post to: YouTube, Twitter, Reddit

### Action 6: Blog Post
Write on dev.to or Medium:
> "I analyzed 50 vibe-coded projects. Here's what breaks most often."
> - Use Crystal to scan real (anonymized) projects
> - Show the most common issues
> - Pitch Crystal as the solution

### Action 7: MCP Directory Listing
Submit Crystal to:
- **mcpservers.com** (MCP directory)
- **glama.ai/mcp** (MCP marketplace)
- **pulsemcp.com** (MCP catalog)
- **awesome-mcp-servers** GitHub list

---

## Phase 3: Community (Month 2) — Get 100+ users

### Action 8: "Good First Issue" Labels
Create 10+ "good first issue" labels on GitHub:
- "Add rules for [Ruby on Rails / Go / Rust / Angular / Svelte]" — just YAML
- "Improve WHY explanation for [gate X]" — just strings
- "Add test fixture for [scenario]" — just files

This attracts contributors who become advocates.

### Action 9: Product Hunt Launch
- Prep: Get 5 people to commit to upvoting on launch day
- Hunter: Ask someone with followers to hunt it
- Assets: GIF demo, clear tagline, case study link
- Tagline: "Crystal — Clean code that ships. Architecture guardian for AI-coded projects."

### Action 10: Partnership Outreach
Email/DM the founders of:
- Cursor, Bolt, Lovable, Replit, Emergent
- Pitch: "Crystal makes projects built on your platform more maintainable. Happy to integrate deeper."
- Offer: Free case study showing Crystal + their platform

---

## Messaging by Channel

| Channel | Message Angle |
|---------|--------------|
| Reddit r/vibecoding | "Your AI keeps breaking old features? Here's why and how to stop it." |
| Reddit r/cursor | "Get context from your last session into Cursor automatically" |
| Twitter/X | Build in public story: "Built an app with AI. It broke. Here's what I did." |
| Hacker News | Technical: "15 static analysis checks specifically for AI-generated code" |
| Discord | Helpful: "If anyone's having issues with AI rewriting their files, I made this tool" |
| YouTube | Demo: "Watch Crystal catch 18 issues in 30 seconds" |
| Product Hunt | Polish: "Architecture guardian for the vibe coding era" |

---

## Metrics to Track

| Week | Target | How to measure |
|------|--------|---------------|
| Week 1 | 10 GitHub stars, 5 pip installs | GitHub insights, PyPI stats |
| Week 2 | 30 stars, 20 installs | Same |
| Week 4 | 100 stars, 50 installs | Same |
| Month 2 | 250 stars, 3 contributors | GitHub insights |
| Month 3 | 500 stars, 10 contributors, 1 platform partnership | GitHub + outreach |

---

## Templates

### Reddit Post Template
```
Title: [Problem statement that resonates]

Body:
I've been building [app type] with [AI tool]. It worked great until [specific problem].

After session 3, my AI rewrote the auth system I built in session 1. 
API keys were hardcoded in the frontend. No tests. No .gitignore.

I built Crystal to fix this. It's a CLI that:
- Runs 15 checks on your project (architecture, security, domain purity)
- Generates paste-ready fix prompts when things are wrong
- Creates a session handoff so your next AI chat has full context

Open source, MIT license, pip install crystal-code.

GitHub: https://github.com/ashimnandi-trika/crystal
Website: https://crystalcodes.dev

Happy to answer questions.
```

### Twitter Thread Template
```
Tweet 1: Problem hook (the pain)
Tweet 2: What goes wrong (specifics with numbers)
Tweet 3: "So I built [Crystal]"
Tweet 4: Demo GIF or screenshot
Tweet 5: Key features (3 bullet points)
Tweet 6: Case study result (F → A)
Tweet 7: CTA (GitHub link, pip install)
```

---

## What NOT to Do

1. **Don't spam** — Contribute to communities before promoting
2. **Don't oversell** — Be honest about what Crystal does and doesn't do
3. **Don't chase vanity metrics** — 10 real users > 1000 stars from bots
4. **Don't build more features yet** — Get feedback on what exists first
5. **Don't pay for ads** — Organic first. Ads after product-market fit.
