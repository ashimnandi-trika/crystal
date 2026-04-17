"""Crystal Agent — AI-powered deep analysis (Phase 4).

Works without LLM by default (rule-based analysis).
With an OpenAI/Anthropic key, uses LLM for deeper natural language analysis.
Set EMERGENT_LLM_KEY to use the Emergent Universal key (requires emergentintegrations).
"""

from __future__ import annotations

import os
import asyncio
from pathlib import Path
from crystal_guard.config import load_config, get_crystal_dir, walk_project_files, CODE_EXTENSIONS, is_test_file
from crystal_guard.detector import detect_stack
from crystal_guard.analyzers import architecture, domain, security, placeholders, dependencies
from crystal_guard.scoring import calculate_health
from crystal_guard.rules.loader import load_rules
from crystal_guard.debt import get_debt_summary
from crystal_guard.handoff import get_project_metrics
import re


class CrystalAgent:
    def __init__(self, project_path: str, llm_key: str = None, llm_provider: str = None, use_llm: bool = True):
        self.project_path = str(Path(project_path).resolve())
        self.config = load_config(self.project_path)
        self.rules = load_rules(self.project_path, self.config.stack)
        if not use_llm:
            self.llm_key = None
            self.llm_provider = None
            return
        # Priority: explicit arg > user env > Emergent key
        self.llm_key = (
            llm_key
            or os.environ.get("ANTHROPIC_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("EMERGENT_LLM_KEY")
        )
        self.llm_provider = llm_provider or self._detect_provider()

    def _detect_provider(self) -> str | None:
        if os.environ.get("ANTHROPIC_API_KEY"):
            return "anthropic"
        if os.environ.get("OPENAI_API_KEY"):
            return "openai"
        if os.environ.get("EMERGENT_LLM_KEY"):
            return "emergent"
        return None

    def _llm_insight(self, system: str, prompt: str) -> str | None:
        """Return LLM-generated text, or None if no LLM available/configured."""
        if not self.llm_key or not self.llm_provider:
            return None
        try:
            if self.llm_provider == "emergent":
                from emergentintegrations.llm.chat import LlmChat, UserMessage
                chat = LlmChat(
                    api_key=self.llm_key,
                    session_id="crystal-agent",
                    system_message=system,
                ).with_model("anthropic", "claude-sonnet-4-5-20250929")
                return asyncio.run(chat.send_message(UserMessage(text=prompt)))
            if self.llm_provider == "anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=self.llm_key)
                resp = client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=1024,
                    system=system,
                    messages=[{"role": "user", "content": prompt}],
                )
                return resp.content[0].text
            if self.llm_provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=self.llm_key)
                resp = client.chat.completions.create(
                    model="gpt-5.1",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                )
                return resp.choices[0].message.content
        except Exception:
            return None
        return None

    def audit(self) -> str:
        """Run comprehensive project audit — correlate issues across analyzers."""
        issues = []
        issues.extend(architecture.analyze(self.project_path, self.rules))
        issues.extend(domain.analyze(self.project_path, self.rules))
        issues.extend(security.analyze(self.project_path, self.rules))
        issues.extend(placeholders.analyze(self.project_path, self.rules))
        issues.extend(dependencies.analyze(self.project_path, self.rules))

        health = calculate_health(issues)
        metrics = get_project_metrics(self.project_path)
        debt = get_debt_summary(self.project_path)
        detected = detect_stack(self.project_path)

        lines = []
        lines.append("# Crystal Audit Report")
        lines.append(f"\n## Project: {self.config.project_name or Path(self.project_path).name}")
        lines.append(f"Stack: {detected['stack_id']}")
        lines.append(f"Files: {metrics['file_count']} | Tests: {metrics['test_file_count']} | Endpoints: {metrics['endpoint_count']}")
        lines.append(f"\n## Health: {health.grade} ({health.score}/100)")
        lines.append(health.summary)

        # Correlate issues
        files_with_issues = {}
        for issue in issues:
            files_with_issues.setdefault(issue.file, []).append(issue)

        hotspots = sorted(files_with_issues.items(), key=lambda x: len(x[1]), reverse=True)

        if hotspots:
            lines.append("\n## Problem Hotspots")
            lines.append("Files with the most issues (fix these first):")
            for filepath, file_issues in hotspots[:5]:
                crits = sum(1 for i in file_issues if i.severity == "critical")
                lines.append(f"\n### {filepath} ({len(file_issues)} issues, {crits} critical)")
                for issue in sorted(file_issues, key=lambda i: {"critical":0,"high":1,"medium":2,"low":3}[i.severity]):
                    lines.append(f"- [{issue.severity.upper()}] {issue.rule_id}: {issue.message}")

        # Cross-analyzer patterns
        lines.append("\n## Analysis")
        sec_count = sum(1 for i in issues if i.analyzer == "security")
        dom_count = sum(1 for i in issues if i.analyzer == "domain")
        arch_count = sum(1 for i in issues if i.analyzer == "architecture")

        if sec_count > 3:
            lines.append(f"- Security is the primary concern ({sec_count} issues). Fix all secret exposure before anything else.")
        if dom_count > 0:
            lines.append(f"- Domain boundaries are violated ({dom_count} issues). Code is in the wrong layer, increasing risk and complexity.")
        if arch_count > 2:
            lines.append(f"- Architecture needs restructuring ({arch_count} issues). Project organization will degrade further without intervention.")

        if debt.get("trend") == "degrading":
            lines.append("- Technical debt is GROWING. The project is getting worse with each session.")
        elif debt.get("trend") == "improving":
            lines.append("- Technical debt is shrinking. Good trajectory.")

        lines.append("\n## Recommendation")
        if health.score >= 90:
            lines.append("Project is in excellent shape. Maintain current practices.")
        elif health.score >= 60:
            lines.append("Project needs targeted fixes. Focus on critical and high severity issues first.")
        else:
            lines.append("Project needs significant work. Do not deploy until critical issues are resolved.")

        # Optional LLM-powered insight
        if self.llm_key:
            rule_report = "\n".join(lines)
            insight = self._llm_insight(
                system=(
                    "You are Crystal, a senior staff engineer reviewing a codebase. "
                    "Given a rule-based audit, add 3-5 concise insights a reviewer "
                    "would raise. Focus on architectural patterns and risk, not lint."
                ),
                prompt=f"Audit report:\n{rule_report}\n\nAdd your insights as markdown bullets under '## AI Insight'.",
            )
            if insight:
                lines.append("")
                lines.append(insight.strip())

        return "\n".join(lines)

    def completeness(self) -> str:
        """Compare PRD with actual implementation."""
        prd_path = get_crystal_dir(self.project_path) / "prd.md"
        if not prd_path.exists():
            return "No PRD found. Run `crystal init` first to create one."

        prd = prd_path.read_text()
        metrics = get_project_metrics(self.project_path)

        # Extract checklist items from PRD
        total_items = 0
        done_items = 0
        items = []
        for line in prd.split("\n"):
            if re.match(r'\s*-\s*\[[ x]\]', line):
                total_items += 1
                done = "[x]" in line.lower()
                if done:
                    done_items += 1
                text = re.sub(r'\s*-\s*\[[ xX]\]\s*', '', line).strip()
                items.append({"text": text, "done": done})

        lines = []
        lines.append("# Feature Completeness Report")
        if total_items > 0:
            pct = round((done_items / total_items) * 100)
            lines.append(f"\n## PRD Progress: {done_items}/{total_items} ({pct}%)")
            lines.append("\n### Done:")
            for item in items:
                if item["done"]:
                    lines.append(f"- {item['text']}")
            lines.append("\n### Remaining:")
            for item in items:
                if not item["done"]:
                    lines.append(f"- {item['text']}")
        else:
            lines.append("\nNo checklist items found in PRD. Add items like `- [ ] Feature name`.")

        lines.append("\n## Project Metrics")
        lines.append(f"- Files: {metrics['file_count']}")
        lines.append(f"- Tests: {metrics['test_file_count']}")
        lines.append(f"- Endpoints: {metrics['endpoint_count']}")

        return "\n".join(lines)

    def refactor(self) -> str:
        """Identify consolidation opportunities."""
        root = Path(self.project_path).resolve()
        lines = []
        lines.append("# Refactoring Opportunities")

        # Find duplicate-ish filenames
        file_names = {}
        for f in walk_project_files(self.project_path, CODE_EXTENSIONS):
            name = f.stem.lower()
            file_names.setdefault(name, []).append(str(f.relative_to(root)))

        dupes = {k: v for k, v in file_names.items() if len(v) > 1}
        if dupes:
            lines.append("\n## Files with similar names (potential duplicates)")
            for name, paths in dupes.items():
                lines.append(f"\n### '{name}' appears {len(paths)} times:")
                for p in paths:
                    lines.append(f"  - {p}")

        # Find large files
        large_files = []
        for f in walk_project_files(self.project_path, CODE_EXTENSIONS):
            if is_test_file(f, root):
                continue
            try:
                line_count = len(f.read_text(errors="ignore").split("\n"))
                if line_count > 200:
                    large_files.append((str(f.relative_to(root)), line_count))
            except OSError:
                pass

        if large_files:
            lines.append("\n## Large files (consider splitting)")
            for path, count in sorted(large_files, key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"- {path}: {count} lines")

        if not dupes and not large_files:
            lines.append("\nNo obvious refactoring opportunities found.")

        return "\n".join(lines)
