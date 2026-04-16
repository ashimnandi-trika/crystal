import { useState, useEffect, useRef } from "react";
import "./App.css";
import {
  Server, Terminal, ShieldCheck, FolderTree, Layers, GitBranch,
  ArrowRight, Check, Copy, ExternalLink, ChevronDown,
  BarChart3, FileText, RefreshCw, Zap,
} from "lucide-react";

const HERO_BG = "https://static.prod-images.emergentagent.com/jobs/3778f3fa-dbe3-475d-870a-0b138480ff3d/images/5562c81e28f7695995a13ea769adea0593fe6447e0c319030cb8381c3bf4fc80.png";

/* ═══════════════════════════════════════════════════
   ANIMATED SECTION — reveals on scroll
   ═══════════════════════════════════════════════════ */
const Reveal = ({ children, className = "", delay = 0 }) => {
  const ref = useRef(null);
  const [vis, setVis] = useState(false);
  useEffect(() => {
    const obs = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) setVis(true); },
      { threshold: 0.08 }
    );
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);
  return (
    <div
      ref={ref}
      className={`${className} transition-all duration-700 ease-out ${vis ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
};

/* ═══════════════════════════════════════════════════
   NAVIGATION
   ═══════════════════════════════════════════════════ */
const Nav = () => {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", h);
    return () => window.removeEventListener("scroll", h);
  }, []);
  return (
    <nav
      data-testid="main-navigation"
      className={`fixed top-0 left-0 right-0 z-50 glass-nav border-b transition-all duration-500 ${scrolled ? "border-white/[0.08] py-3" : "border-transparent py-5"}`}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-12 flex items-center justify-between">
        <a href="#hero" data-testid="nav-logo" className="flex items-center gap-3 group">
          <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/25 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
            <ShieldCheck size={16} className="text-blue-400" />
          </div>
          <span className="font-mono text-[15px] font-semibold tracking-tight text-white">Crystal</span>
        </a>
        <div className="flex items-center gap-8">
          <a href="#features" data-testid="nav-features-link" className="hidden md:inline text-[14px] text-neutral-400 hover:text-white transition-colors duration-200">Features</a>
          <a href="#quick-start" data-testid="nav-docs-link" className="hidden md:inline text-[14px] text-neutral-400 hover:text-white transition-colors duration-200">Get Started</a>
          <a href="#commands" data-testid="nav-commands-link" className="hidden md:inline text-[14px] text-neutral-400 hover:text-white transition-colors duration-200">Commands</a>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            data-testid="nav-github-btn"
            className="inline-flex items-center gap-2 rounded-lg bg-white px-5 py-2.5 text-[13px] font-semibold text-black hover:bg-neutral-100 transition-colors"
          >
            <GitBranch size={14} />
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
};

/* ═══════════════════════════════════════════════════
   HERO — The first impression. Must hit HARD.
   ═══════════════════════════════════════════════════ */
const Hero = () => (
  <section id="hero" data-testid="hero-section" className="relative min-h-screen flex items-center justify-center hero-glow overflow-hidden">
    {/* Background crystal image */}
    <div
      className="absolute inset-0 opacity-[0.06] pointer-events-none"
      style={{
        backgroundImage: `url(${HERO_BG})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        maskImage: "radial-gradient(ellipse 70% 60% at 50% 40%, black, transparent)",
        WebkitMaskImage: "radial-gradient(ellipse 70% 60% at 50% 40%, black, transparent)",
      }}
    />

    <div className="relative z-10 max-w-5xl mx-auto px-6 lg:px-12 text-center pt-32 pb-20">
      {/* Badge */}
      <div className="animate-fade-up">
        <div className="inline-flex items-center gap-2.5 rounded-full border border-white/[0.08] bg-white/[0.03] px-5 py-2 mb-12">
          <span className="w-2 h-2 rounded-full bg-blue-400" style={{ animation: "pulse-dot 2s ease-in-out infinite" }} />
          <span className="text-[13px] font-mono text-neutral-400 tracking-wide">Open Source &middot; Works with any AI coding tool</span>
        </div>
      </div>

      {/* Line 1: CRYSTAL — massive, commanding */}
      <h1
        data-testid="hero-title"
        className="animate-fade-up delay-100 text-[clamp(4rem,12vw,10rem)] font-black text-white leading-[0.9] tracking-[-0.05em]"
      >
        Crystal
      </h1>

      {/* Line 2: The punch line — large, bold, clear */}
      <p
        data-testid="hero-punchline"
        className="animate-fade-up delay-200 mt-6 text-[clamp(1.5rem,4vw,2.75rem)] font-semibold text-white leading-tight tracking-tight"
      >
        Clean code that ships.
      </p>

      {/* Line 3: One clean line — grey with blue accents on key words */}
      <p
        data-testid="hero-subtitle"
        className="animate-fade-up delay-300 mt-7 text-[clamp(1.1rem,2.2vw,1.5rem)] text-neutral-500 font-normal tracking-tight leading-snug"
      >
        Protects <span className="text-blue-400">architecture integrity</span> and <span className="text-blue-400">domain purity</span> so your code <span className="text-blue-400">ships</span> clean.
      </p>

      {/* CTAs */}
      <div className="animate-fade-up delay-400 mt-12 flex flex-col sm:flex-row items-center justify-center gap-4">
        <a
          href="#quick-start"
          data-testid="hero-get-started-btn"
          className="inline-flex items-center gap-2.5 rounded-lg bg-white px-8 py-4 text-[15px] font-semibold text-black hover:bg-neutral-100 transition-all duration-200 hover:shadow-[0_0_30px_rgba(255,255,255,0.1)]"
        >
          Get Started
          <ArrowRight size={18} />
        </a>
        <a
          href="https://github.com"
          target="_blank"
          rel="noopener noreferrer"
          data-testid="hero-github-btn"
          className="inline-flex items-center gap-2.5 rounded-lg border border-white/15 bg-white/[0.03] px-8 py-4 text-[15px] font-medium text-white hover:bg-white/[0.08] transition-all duration-200"
        >
          <GitBranch size={17} />
          View on GitHub
        </a>
      </div>

      {/* Terminal preview */}
      <div className="animate-fade-up delay-600 mt-20">
        <TerminalWindow
          lines={[
            { t: "cmd", v: "pip install crystal-guard" },
            { t: "out", v: "Installed crystal-guard-0.1.0" },
            { t: "cmd", v: "crystal init" },
            { t: "ok",  v: "Found: React + Python + MongoDB" },
            { t: "ok",  v: "15 quality checks loaded" },
            { t: "cmd", v: "crystal check" },
            { t: "ok",  v: "15/15 checks passed  |  Health: A (100/100)" },
            { t: "cmd", v: "crystal handoff" },
            { t: "ok",  v: "Handoff ready. Paste into your next AI session." },
          ]}
        />
      </div>

      <div className="animate-fade-up delay-800 mt-16">
        <ChevronDown size={22} className="mx-auto text-neutral-700 animate-bounce" />
      </div>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   TERMINAL WINDOW — authentic macOS look
   ═══════════════════════════════════════════════════ */
const TerminalWindow = ({ lines, showCopy = false, copyText = "" }) => {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(copyText || lines.filter(l => l.t === "cmd").map(l => l.v).join("\n"));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <div data-testid="terminal-block" className="terminal-glow rounded-2xl overflow-hidden border border-white/[0.08] bg-[#0A0A0A] w-full max-w-3xl mx-auto text-left shadow-2xl">
      <div className="flex items-center justify-between px-5 py-3.5 bg-[#141414] border-b border-white/[0.06]">
        <div className="flex items-center gap-2.5">
          <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
          <div className="w-3 h-3 rounded-full bg-[#FEBC2E]" />
          <div className="w-3 h-3 rounded-full bg-[#28C840]" />
        </div>
        <span className="text-[11px] font-mono text-neutral-600 tracking-wider">terminal</span>
        {showCopy ? (
          <button data-testid="copy-command-btn" onClick={handleCopy} className="flex items-center gap-1.5 text-[12px] text-neutral-500 hover:text-white transition-colors">
            {copied ? <Check size={12} className="text-green-400" /> : <Copy size={12} />}
            {copied ? "Copied" : "Copy"}
          </button>
        ) : <div />}
      </div>
      <div className="px-6 py-5 space-y-2 font-mono text-[14px] leading-relaxed overflow-x-auto">
        {lines.map((line, i) => (
          <div key={i} className="flex items-start gap-3">
            {line.t === "cmd" && (
              <>
                <span className="text-blue-400 select-none shrink-0 font-semibold">$</span>
                <span className="text-neutral-100">{line.v}</span>
              </>
            )}
            {line.t === "out" && <span className="text-neutral-500 pl-6">{line.v}</span>}
            {line.t === "ok" && (
              <>
                <Check size={15} className="text-emerald-400 mt-0.5 shrink-0" />
                <span className="text-emerald-400">{line.v}</span>
              </>
            )}
            {line.t === "err" && <span className="text-red-400 pl-6">{line.v}</span>}
            {line.t === "warn" && <span className="text-amber-400 pl-6">{line.v}</span>}
          </div>
        ))}
      </div>
    </div>
  );
};

/* ═══════════════════════════════════════════════════
   PROBLEM — Stats that make people stop scrolling
   ═══════════════════════════════════════════════════ */
const stats = [
  { value: "36%", label: "of people using AI to code never test it" },
  { value: "1.7x", label: "more bugs in AI-written code vs human code" },
  { value: "45%", label: "of AI-generated code has security holes" },
  { value: "63%", label: "spend more time fixing AI code than writing it" },
];

const ProblemSection = () => (
  <section id="problem" data-testid="problem-section" className="py-28 md:py-40">
    <div className="max-w-7xl mx-auto px-6 lg:px-12">
      <Reveal>
        <p className="text-[13px] font-mono text-blue-400 tracking-[0.2em] uppercase mb-5">The Problem</p>
        <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white leading-[1.1] max-w-3xl">
          AI builds fast.<br />
          <span className="text-neutral-500">Then things break.</span>
        </h2>
        <p className="mt-7 text-neutral-400 text-[18px] max-w-2xl leading-relaxed">
          You ask AI to build something. It works. Next session, you add a feature. Old stuff breaks. Nobody knows why.
        </p>
      </Reveal>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-20">
        {stats.map((stat, i) => (
          <Reveal key={i} delay={i * 80}>
            <div
              data-testid={`stat-card-${i}`}
              className="relative stat-line rounded-2xl border border-white/[0.07] bg-white/[0.02] p-8 card-lift"
            >
              <span className="block text-[clamp(2.5rem,6vw,3.5rem)] font-extrabold tracking-tighter text-white leading-none">{stat.value}</span>
              <p className="mt-4 text-neutral-400 text-[15px] leading-relaxed">{stat.label}</p>
            </div>
          </Reveal>
        ))}
      </div>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   HOW IT WORKS — 3 pillars
   ═══════════════════════════════════════════════════ */
const pillars = [
  {
    icon: Server,
    title: "While You Code",
    label: "MCP Connection",
    body: "Crystal plugs into your AI tool. While your AI writes code, Crystal watches and says 'hey, that file belongs somewhere else' or 'that's a security risk.' Real-time, not after the fact.",
  },
  {
    icon: Terminal,
    title: "Before You Ship",
    label: "One Command",
    body: "Run crystal check. You get a score from A to F. It tells you what's wrong in plain English. Fix the red items. Ship with confidence. That's it.",
  },
  {
    icon: ShieldCheck,
    title: "On Every Push",
    label: "Automatic",
    body: "Add one file to your GitHub repo. Now every time anyone pushes code, Crystal checks it automatically. Bad code can't sneak through.",
  },
];

const HowItWorks = () => (
  <section id="solution" data-testid="solution-section" className="py-28 md:py-40 border-t border-white/[0.04]">
    <div className="max-w-7xl mx-auto px-6 lg:px-12">
      <Reveal>
        <p className="text-[13px] font-mono text-blue-400 tracking-[0.2em] uppercase mb-5">How It Works</p>
        <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white leading-[1.1] max-w-3xl">
          It watches your code.<br />
          <span className="text-neutral-500">So you don't have to.</span>
        </h2>
        <p className="mt-7 text-neutral-400 text-[18px] max-w-2xl leading-relaxed">
          Think of it as spell-check for your code structure. Runs quietly. Tells you when something's off.
        </p>
      </Reveal>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20">
        {pillars.map((p, i) => (
          <Reveal key={i} delay={i * 120}>
            <div
              data-testid={`pillar-card-${i}`}
              className="rounded-2xl border border-white/[0.07] bg-white/[0.015] p-9 md:p-10 card-lift h-full flex flex-col"
            >
              <div className="w-14 h-14 rounded-xl bg-blue-500/[0.08] border border-blue-500/20 flex items-center justify-center mb-7">
                <p.icon size={24} className="text-blue-400" />
              </div>
              <span className="text-[11px] font-mono text-blue-400 tracking-[0.2em] uppercase mb-2">{p.label}</span>
              <h3 className="text-[22px] font-semibold text-white">{p.title}</h3>
              <p className="mt-4 text-neutral-400 text-[15px] leading-[1.7] flex-1">{p.body}</p>
            </div>
          </Reveal>
        ))}
      </div>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   QUICK START — Three commands. That's all.
   ═══════════════════════════════════════════════════ */
const QuickStart = () => (
  <section id="quick-start" data-testid="quick-start-section" className="py-28 md:py-40 border-t border-white/[0.04]">
    <div className="max-w-7xl mx-auto px-6 lg:px-12">
      <Reveal>
        <div className="text-center mb-20">
          <p className="text-[13px] font-mono text-blue-400 tracking-[0.2em] uppercase mb-5">Get Started</p>
          <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white leading-[1.1]">
            Three commands.<br />
            <span className="text-neutral-500">That's all.</span>
          </h2>
        </div>
      </Reveal>
      <Reveal delay={150}>
        <TerminalWindow
          showCopy
          copyText="pip install crystal-guard && crystal init && crystal check"
          lines={[
            { t: "cmd", v: "pip install crystal-guard" },
            { t: "out", v: "Installed crystal-guard-0.1.0" },
            { t: "cmd", v: "crystal init" },
            { t: "ok",  v: "Found: React + Python + MongoDB" },
            { t: "ok",  v: "Created .crystal/ config" },
            { t: "ok",  v: "15 quality checks loaded" },
            { t: "cmd", v: "crystal check" },
            { t: "out", v: "" },
            { t: "ok",  v: "Architecture     PASS" },
            { t: "ok",  v: "Domain Purity    PASS" },
            { t: "warn",v: "Security         1 issue found" },
            { t: "ok",  v: "Code Hygiene     PASS" },
            { t: "out", v: "" },
            { t: "out", v: "Health: B (82/100)" },
            { t: "err", v: "[CRITICAL] API key found in src/config.js line 15" },
            { t: "out", v: "Fix: Move this key to your .env file" },
          ]}
        />
      </Reveal>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   FEATURES — The 7 things Crystal does
   ═══════════════════════════════════════════════════ */
const features = [
  { icon: FileText, title: "Picks Up Where You Left Off", body: "Every time you start a new AI chat, you lose context. Crystal reads your project and writes a summary. Paste it in. Your AI knows exactly what happened before." },
  { icon: ShieldCheck, title: "15 Automatic Checks", body: "Is your password hardcoded? Database code in the frontend? Missing tests? Crystal runs 15 checks and tells you exactly what to fix. In plain English." },
  { icon: BarChart3, title: "Tracks Your Progress", body: "Yesterday you had 47 files and 12 tests. Today it's 52 files and 11 tests. A test disappeared. Crystal notices and tells you." },
  { icon: RefreshCw, title: "Works Across Tools", body: "Start in Cursor, continue in Claude, finish in Emergent. Crystal generates a handoff that works everywhere. Your context is never locked to one tool." },
  { icon: Zap, title: "Helps Your AI in Real-Time", body: "Crystal plugs into your AI assistant via MCP. While the AI writes code, Crystal says 'that file goes in the wrong folder' before it's too late." },
  { icon: FolderTree, title: "Rules That Stick", body: "Define your project rules once. 'Keep database code in the backend.' 'No secrets in the code.' Crystal enforces them every session, every tool, every time." },
  { icon: Layers, title: "Shows Where Problems Pile Up", body: "Skipped tests here, a TODO there, a security warning ignored. Crystal tracks it all across sessions and shows you: here's your debt, here's what to fix first." },
];

const Features = () => (
  <section id="features" data-testid="features-section" className="py-28 md:py-40 border-t border-white/[0.04]">
    <div className="max-w-7xl mx-auto px-6 lg:px-12">
      <Reveal>
        <p className="text-[13px] font-mono text-blue-400 tracking-[0.2em] uppercase mb-5">What Crystal Does</p>
        <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white leading-[1.1] max-w-3xl">
          Seven things that keep<br />
          <span className="text-neutral-500">your project alive.</span>
        </h2>
      </Reveal>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mt-20">
        {features.map((f, i) => (
          <Reveal key={i} delay={i * 70}>
            <div
              data-testid={`feature-card-${i}`}
              className={`rounded-2xl border border-white/[0.07] bg-white/[0.015] p-8 card-lift h-full ${i === 6 ? "md:col-span-2 lg:col-span-1" : ""}`}
            >
              <div className="w-10 h-10 rounded-lg bg-blue-500/[0.08] border border-blue-500/20 flex items-center justify-center mb-5">
                <f.icon size={18} className="text-blue-400" />
              </div>
              <h3 className="text-[18px] font-semibold text-white leading-tight">{f.title}</h3>
              <p className="mt-3 text-neutral-400 text-[15px] leading-[1.7]">{f.body}</p>
            </div>
          </Reveal>
        ))}
      </div>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   USE CASES
   ═══════════════════════════════════════════════════ */
const useCases = [
  { title: "Building Alone", tag: "Solo", body: "You're making your app with AI. After a few sessions, things start breaking. Crystal keeps it clean so it works today, tomorrow, and next month." },
  { title: "Building with Others", tag: "Team", body: "Two people using AI on the same project. One person's AI rewrites what the other built. Crystal enforces shared rules so everyone's work stays intact." },
  { title: "Open Source", tag: "Community", body: "People contribute code using AI tools. Crystal runs on every pull request and makes sure contributions meet your standards. Automatically." },
];

const UseCases = () => (
  <section id="use-cases" data-testid="use-cases-section" className="py-28 md:py-40 border-t border-white/[0.04]">
    <div className="max-w-7xl mx-auto px-6 lg:px-12">
      <Reveal>
        <p className="text-[13px] font-mono text-blue-400 tracking-[0.2em] uppercase mb-5">Who It's For</p>
        <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white leading-[1.1] max-w-3xl">
          Anyone building<br />
          <span className="text-neutral-500">with AI.</span>
        </h2>
      </Reveal>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20">
        {useCases.map((uc, i) => (
          <Reveal key={i} delay={i * 120}>
            <div
              data-testid={`use-case-card-${i}`}
              className="rounded-2xl border border-white/[0.07] bg-white/[0.015] p-9 md:p-10 card-lift h-full flex flex-col"
            >
              <span className="inline-block self-start rounded-full border border-white/[0.08] bg-white/[0.04] px-4 py-1.5 text-[12px] font-mono text-neutral-400 tracking-wide mb-7">
                {uc.tag}
              </span>
              <h3 className="text-[22px] font-semibold text-white">{uc.title}</h3>
              <p className="mt-4 text-neutral-400 text-[15px] leading-[1.7] flex-1">{uc.body}</p>
            </div>
          </Reveal>
        ))}
      </div>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   COMMANDS — Reference table
   ═══════════════════════════════════════════════════ */
const commands = [
  { cmd: "crystal init", desc: "Set up Crystal. It figures out your tech stack automatically.", flags: "--stack react-python-mongo" },
  { cmd: "crystal check", desc: "Run all 15 checks. See your health score (A to F).", flags: "--format json" },
  { cmd: "crystal handoff", desc: "Create a summary to paste into your next AI session.", flags: "--output handoff.md" },
  { cmd: "crystal status", desc: "See how your project is doing. Score, trends, changes.", flags: "" },
  { cmd: "crystal gates", desc: "See each of the 15 checks individually. Pass or fail.", flags: "" },
  { cmd: "crystal architect", desc: "Generate an architecture.md with your project rules.", flags: "--output architecture.md" },
  { cmd: "crystal report", desc: "Create a detailed report to share or attach to a PR.", flags: "--output report.md" },
];

const Commands = () => (
  <section id="commands" data-testid="commands-section" className="py-28 md:py-40 border-t border-white/[0.04]">
    <div className="max-w-7xl mx-auto px-6 lg:px-12">
      <Reveal>
        <p className="text-[13px] font-mono text-blue-400 tracking-[0.2em] uppercase mb-5">Commands</p>
        <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white leading-[1.1] max-w-3xl">
          Type a command.<br />
          <span className="text-neutral-500">Get answers.</span>
        </h2>
      </Reveal>
      <Reveal delay={150}>
        <div className="mt-16 rounded-2xl border border-white/[0.07] overflow-hidden">
          <table data-testid="commands-table" className="w-full text-left">
            <thead>
              <tr className="border-b border-white/[0.06] bg-white/[0.02]">
                <th className="px-7 py-4 text-[11px] font-mono font-semibold text-neutral-500 uppercase tracking-[0.15em]">Command</th>
                <th className="px-7 py-4 text-[11px] font-mono font-semibold text-neutral-500 uppercase tracking-[0.15em] hidden md:table-cell">What it does</th>
                <th className="px-7 py-4 text-[11px] font-mono font-semibold text-neutral-500 uppercase tracking-[0.15em] hidden lg:table-cell">Options</th>
              </tr>
            </thead>
            <tbody>
              {commands.map((c, i) => (
                <tr key={i} data-testid={`command-row-${i}`} className="border-b border-white/[0.04] hover:bg-white/[0.015] transition-colors">
                  <td className="px-7 py-5">
                    <code className="text-[14px] font-mono font-medium text-blue-400">{c.cmd}</code>
                    <p className="md:hidden mt-2 text-[13px] text-neutral-500 leading-relaxed">{c.desc}</p>
                  </td>
                  <td className="px-7 py-5 text-[15px] text-neutral-400 hidden md:table-cell">{c.desc}</td>
                  <td className="px-7 py-5 hidden lg:table-cell">
                    {c.flags && <code className="text-[12px] font-mono text-neutral-600">{c.flags}</code>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Reveal>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   PLATFORMS
   ═══════════════════════════════════════════════════ */
const platforms = ["Cursor", "Windsurf", "Claude Desktop", "VS Code", "Bolt", "Lovable", "Replit", "Emergent"];

const Platforms = () => (
  <section data-testid="compatibility-section" className="py-20 border-t border-white/[0.04]">
    <div className="max-w-7xl mx-auto px-6 lg:px-12 text-center">
      <p className="text-[11px] font-mono text-neutral-600 tracking-[0.25em] uppercase mb-10">Works with any AI coding tool</p>
      <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-5">
        {platforms.map((p, i) => (
          <span key={i} data-testid={`platform-${i}`} className="text-[15px] text-neutral-500 font-medium">{p}</span>
        ))}
      </div>
    </div>
  </section>
);

/* ═══════════════════════════════════════════════════
   FOOTER — Final CTA
   ═══════════════════════════════════════════════════ */
const Footer = () => (
  <footer data-testid="footer-section" className="py-28 md:py-40 border-t border-white/[0.04]">
    <div className="max-w-7xl mx-auto px-6 lg:px-12 text-center">
      <Reveal>
        <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white leading-[1.1]">
          Build with AI.<br />
          <span className="text-neutral-500">Ship with Crystal.</span>
        </h2>
        <p className="mt-7 text-neutral-400 text-[18px] max-w-xl mx-auto leading-relaxed">
          Free. Open source. Takes 30 seconds to set up.<br />Works with every AI coding tool.
        </p>
        <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            data-testid="footer-github-btn"
            className="inline-flex items-center gap-2.5 rounded-lg bg-white px-9 py-4 text-[15px] font-semibold text-black hover:bg-neutral-100 transition-all duration-200 hover:shadow-[0_0_30px_rgba(255,255,255,0.1)]"
          >
            <GitBranch size={17} />
            Star on GitHub
            <ExternalLink size={14} className="opacity-40" />
          </a>
          <a
            href="#quick-start"
            data-testid="footer-quickstart-btn"
            className="inline-flex items-center gap-2 rounded-lg border border-white/15 bg-white/[0.03] px-9 py-4 text-[15px] font-medium text-white hover:bg-white/[0.08] transition-all duration-200"
          >
            Get Started
          </a>
        </div>
      </Reveal>

      {/* Footer bottom */}
      <div className="mt-28 pt-8 border-t border-white/[0.04] flex flex-col md:flex-row items-center justify-between gap-5">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-blue-500/10 border border-blue-500/25 flex items-center justify-center">
            <ShieldCheck size={13} className="text-blue-400" />
          </div>
          <span className="font-mono text-[13px] text-neutral-500">Crystal</span>
        </div>
        <p className="text-[13px] text-neutral-600">
          MIT License &middot; Free forever &middot; Built for people who build with AI
        </p>
        <div className="flex items-center gap-8">
          <a href="https://github.com" className="text-[13px] text-neutral-500 hover:text-white transition-colors">GitHub</a>
          <a href="#commands" className="text-[13px] text-neutral-500 hover:text-white transition-colors">Commands</a>
          <a href="#quick-start" className="text-[13px] text-neutral-500 hover:text-white transition-colors">Get Started</a>
        </div>
      </div>
    </div>
  </footer>
);

/* ═══════════════════════════════════════════════════
   APP
   ═══════════════════════════════════════════════════ */
function App() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Nav />
      <Hero />
      <ProblemSection />
      <HowItWorks />
      <QuickStart />
      <Features />
      <UseCases />
      <Commands />
      <Platforms />
      <Footer />
    </div>
  );
}

export default App;
