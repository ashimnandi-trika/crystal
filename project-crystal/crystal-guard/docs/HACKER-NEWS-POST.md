# HACKER NEWS ANNOUNCEMENT — Copy-paste ready

## Submit at: https://news.ycombinator.com/submit

### Title:
Show HN: We scanned a vibe-coded todo app. It had 29 problems nobody knew about.

### URL:
https://github.com/ashimnandi-trika/crystal

### First comment (post immediately after submitting):

---

We took a simple todo app built across 4 AI coding sessions in Cursor and scanned it with Crystal, an open-source CLI we built.

The app worked perfectly on localhost. The developer was about to push it to GitHub and deploy.

Crystal found 29 issues. 5 were critical:

1. An OpenAI API key was hardcoded in two files — the frontend React component and the backend server. Anyone who sees the code gets the key.

2. A MongoDB import was sitting in a React component. That means database access logic is visible to anyone who opens browser dev tools.

3. The database password was written directly in server.py: `password = "..."`. Not in an environment variable. In the code.

4. There was no .gitignore. The .env file containing the Stripe secret key, OpenAI key, and database password would have been committed to GitHub on the next push.

5. CORS was set to wildcard (*), meaning any website on the internet could make requests to the API.

Beyond the critical issues, there were 7 unfinished TODO comments, 4 console.log debug statements, 5 hardcoded localhost URLs that would break on deploy, and placeholder text like "test@test.com" and "example.com" in the UI.

The developer had no idea about any of this. The app worked. That was enough. Until it wasn't.

We built Crystal to catch exactly this. It runs 15 checks across architecture, security, domain purity, and code hygiene. When something fails, it generates a paste-ready prompt — you copy it into your AI tool, the AI fixes the exact issue.

The real project files are in the repo. You can clone it and run the scan yourself:

```
pip install crystal-code
cd examples/case-study/before
crystal init && crystal check
```

You'll see the same 29 issues, the same F score.

Case study with full terminal output: https://github.com/ashimnandi-trika/crystal/blob/main/project-crystal/crystal-guard/examples/case-study/CASE-STUDY.md

Live site: https://build-integrity.emergent.host

Would love feedback on what checks matter most to your workflow.
