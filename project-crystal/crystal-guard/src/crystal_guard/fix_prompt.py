"""Fix Prompt Generator — Generates paste-ready AI prompts for every issue.

When quality gates fail, vibe coders can't fix things themselves.
This generates the EXACT prompt they paste into their AI coding tool.
The AI reads it and fixes the issue without breaking anything else.
"""

from crystal_guard.analyzers import Issue

# WHY explanations for each rule — written for someone who has never coded
WHY_EXPLANATIONS = {
    "arch-001": "Your project needs organized folders so your AI tool knows where to put things. Without them, files end up in random places and your project becomes a mess that nobody can navigate.",
    "arch-002": "Without a .gitignore file, your passwords, API keys, and private data get uploaded to GitHub where anyone can see them. This is one of the most common security mistakes.",
    "arch-004": "Too many files dumped in the root folder is like having everything on your desktop. It gets harder to find things, and your AI tool will struggle to understand your project structure.",
    "arch-005": "Folders nested too deep means your project's organization is getting tangled. It makes everything harder to find and maintain.",
    "arch-006": "Your .gitignore file doesn't include .env, which means your secret keys and passwords will be uploaded to GitHub. Anyone who finds your repo gets all your secrets.",
    "arch-007": "Your project has zero tests. That means there's no way to know if new changes break old features. This is why things keep breaking every time you add something.",
    "dom-001": "Your website runs in people's browsers. If database code is in the frontend, anyone can open browser developer tools and see exactly how to access your database. They could read, change, or delete all your data.",
    "dom-002": "Your website runs in a browser. Browsers cannot read files from your server. This code will crash the moment a real user visits your site.",
    "dom-003": "Only environment variables starting with REACT_APP_ (or NEXT_PUBLIC_ for Next.js) are available in the browser. The variable you're using won't load, and your feature will silently break.",
    "dom-004": "Password hashing and authentication must happen on the server, not in the browser. If it's in the frontend, attackers can see your security logic and bypass it.",
    "sec-001": "Your API key is like a credit card number for a service you use. Right now it's written directly in your code. If anyone sees your code (GitHub, a teammate, a hacker), they get your key and can use your account. You'll get the bill.",
    "sec-002": "A password is sitting directly in your code. Anyone who can see the code gets the password. This includes anyone with access to your GitHub repo.",
    "sec-003": "Crystal recognized this as a real API key (Stripe, OpenAI, GitHub, or AWS format). This is an active security risk right now. If this code is on GitHub, your key may already be compromised.",
    "sec-004": "Your .env file contains all your secrets (API keys, passwords, database URLs). Right now, .env is not in .gitignore, which means every time you push code, all your secrets go to GitHub too.",
    "sec-005": "CORS wildcard (*) means ANY website on the internet can make requests to your API. An attacker could create a fake site that talks to your backend and steals user data.",
    "sec-006": "Building SQL queries by pasting user input directly into the query string lets attackers inject their own SQL commands. They could read your entire database, delete data, or gain admin access.",
    "hyg-001": "TODO means 'I need to finish this later.' In production, 'later' usually means 'never.' This is something your app needs but doesn't have yet. If users hit this path, something will break or be missing.",
    "hyg-002": "Values like example.com or test@test.com mean something wasn't configured with real data. Real users will see broken links or fake information.",
    "hyg-003": "console.log sends messages to the browser console. In production, it slows your app down and can accidentally leak sensitive information to anyone who opens developer tools.",
    "hyg-004": "localhost only works on your computer. When your app is deployed to a real server, every link pointing to localhost will break.",
}


def generate_fix_prompt(issue: Issue, project_context: str = "") -> str:
    """Generate a paste-ready fix prompt for a single issue."""
    why = WHY_EXPLANATIONS.get(issue.rule_id, issue.why or "This issue can cause problems in production.")

    loc = issue.file
    if issue.line:
        loc += f", line {issue.line}"

    lines = []
    lines.append(f"## FIX: {issue.message}")
    lines.append("")
    lines.append(f"**File**: {loc}")
    lines.append(f"**Severity**: {issue.severity.upper()}")
    lines.append("")
    lines.append("**What's wrong**:")
    lines.append(issue.message)
    lines.append("")
    lines.append("**Why this is dangerous**:")
    lines.append(why)
    lines.append("")
    lines.append("**How to fix it**:")
    lines.append(issue.suggestion)
    lines.append("")
    lines.append("**Rules**:")
    lines.append(f"- Only change {issue.file}. Do not modify other files unless the fix requires it.")
    lines.append("- Do not rename or move the file.")
    lines.append("- Do not rewrite code that is already working.")
    lines.append("- After fixing, run `crystal check` to verify the issue is resolved.")

    return "\n".join(lines)


def generate_all_fix_prompts(issues: list[Issue], project_context: str = "") -> str:
    """Generate one document with fix prompts for ALL issues, in priority order."""
    if not issues:
        return "No issues found. All quality gates passed."

    sorted_issues = sorted(issues, key=lambda i: (
        {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(i.severity, 4)
    ))

    lines = []
    lines.append("# CRYSTAL FIX PROMPTS")
    lines.append("")
    lines.append(f"Found {len(issues)} issues. Fix them in this order (most critical first).")
    lines.append("Paste each section into your AI coding tool one at a time.")
    lines.append("")

    if project_context:
        lines.append("## PROJECT CONTEXT")
        lines.append(project_context[:1000])
        lines.append("")

    for i, issue in enumerate(sorted_issues, 1):
        lines.append("---")
        lines.append(f"### Issue {i} of {len(sorted_issues)} ({issue.severity.upper()})")
        lines.append("")
        lines.append(generate_fix_prompt(issue))
        lines.append("")

    lines.append("---")
    lines.append("After fixing all issues, run `crystal check` to verify everything passes.")

    return "\n".join(lines)
