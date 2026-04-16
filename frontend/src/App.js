import { useState, useEffect, useRef } from "react";
import "./App.css";
import { Server, Terminal, ShieldCheck, FolderTree, Layers, GitBranch, ArrowRight, Check, Copy, ExternalLink, ChevronDown, BarChart3, FileText, RefreshCw, Zap } from "lucide-react";

const HERO_BG = "https://static.prod-images.emergentagent.com/jobs/3778f3fa-dbe3-475d-870a-0b138480ff3d/images/5562c81e28f7695995a13ea769adea0593fe6447e0c319030cb8381c3bf4fc80.png";

/* ─── Animated Section Wrapper ─── */
const AnimatedSection = ({ children, className = "", delay = 0 }) => {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setVisible(true); },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  return (
    <div
      ref={ref}
      className={`${className} transition-all duration-700 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
};

/* ─── Navigation ─── */
const Nav = () => {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", handler);
    return () => window.removeEventListener("scroll", handler);
  }, []);
  return (
    <nav
      data-testid="main-navigation"
      className={`fixed top-0 left-0 right-0 z-50 glass-nav border-b transition-all duration-300 ${scrolled ? "border-white/10" : "border-transparent"}`}
    >
      <div className="max-w-7xl mx-auto px-6 md:px-12 flex items-center justify-between h-16">
        <a href="#hero" data-testid="nav-logo" className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-md bg-white/10 border border-white/20 flex items-center justify-center">
            <ShieldCheck size={14} className="text-blue-400" />
          </div>
          <span className="font-mono text-sm font-semibold tracking-tight text-white">Crystal</span>
        </a>
        <div className="flex items-center gap-6">
          <a href="#quick-start" data-testid="nav-docs-link" className="hidden md:inline text-sm text-neutral-400 hover:text-white transition-colors">
            Get Started
          </a>
          <a href="#features" data-testid="nav-features-link" className="hidden md:inline text-sm text-neutral-400 hover:text-white transition-colors">
            Features
          </a>
          <a href="#commands" data-testid="nav-commands-link" className="hidden md:inline text-sm text-neutral-400 hover:text-white transition-colors">
            Commands
          </a>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            data-testid="nav-github-btn"
            className="inline-flex items-center gap-2 rounded-md bg-white px-4 py-2 text-sm font-medium text-black hover:bg-neutral-200 transition-colors"
          >
            <GitBranch size={14} />
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
};

/* ─── Hero ─── */
const Hero = () => (
  <section id="hero" data-testid="hero-section" className="relative min-h-screen flex items-center justify-center hero-gradient pt-16">
    <div
      className="absolute inset-0 opacity-[0.07] pointer-events-none"
      style={{
        backgroundImage: `url(${HERO_BG})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        maskImage: "radial-gradient(ellipse 70% 60% at 50% 50%, black, transparent)",
        WebkitMaskImage: "radial-gradient(ellipse 70% 60% at 50% 50%, black, transparent)",
      }}
    />
    <div className="relative z-10 max-w-5xl mx-auto px-6 md:px-12 text-center">
      <div className="animate-fade-in-up">
        <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-4 py-1.5 mb-8">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
          <span className="text-xs font-mono text-neutral-400 tracking-wide">Open Source &middot; Works with any AI coding tool</span>
        </div>
      </div>
      <h1
        data-testid="hero-title"
        className="text-5xl md:text-7xl lg:text-8xl tracking-tighter font-semibold text-white leading-[0.95] animate-fade-in-up animation-delay-100"
        style={{ opacity: 0, animationFillMode: "forwards" }}
      >
        Crystal
      </h1>
      <p
        data-testid="hero-tagline"
        className="mt-6 text-2xl md:text-3xl tracking-tight font-medium text-neutral-300 animate-fade-in-up animation-delay-200"
        style={{ opacity: 0, animationFillMode: "forwards" }}
      >
        Your AI coding buddy that protects<br className="hidden md:block" />{" "}
        <span className="text-blue-400">architecture integrity</span> and <span className="text-blue-400">domain purity</span>
      </p>
      <p
        data-testid="hero-subtitle"
        className="mt-5 text-lg text-neutral-500 max-w-2xl mx-auto leading-relaxed animate-fade-in-up animation-delay-300"
        style={{ opacity: 0, animationFillMode: "forwards" }}
      >
        So your project ships clean. Every time.
      </p>
      <div
        className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in-up animation-delay-400"
        style={{ opacity: 0, animationFillMode: "forwards" }}
      >
        <a
          href="#quick-start"
          data-testid="hero-get-started-btn"
          className="inline-flex items-center gap-2 rounded-md bg-white px-7 py-3.5 text-sm font-medium text-black hover:bg-neutral-200 transition-colors"
        >
          Get Started
          <ArrowRight size={16} />
        </a>
        <a
          href="https://github.com"
          target="_blank"
          rel="noopener noreferrer"
          data-testid="hero-github-btn"
          className="inline-flex items-center gap-2 rounded-md border border-white/20 bg-transparent px-7 py-3.5 text-sm font-medium text-white hover:bg-white/10 transition-colors"
        >
          <GitBranch size={16} />
          View on GitHub
        </a>
      </div>
      {/* Terminal preview */}
      <div
        className="mt-16 animate-fade-in-up animation-delay-500"
        style={{ opacity: 0, animationFillMode: "forwards" }}
      >
        <TerminalBlock
          lines={[
            { type: "command", text: "pip install crystal-guard" },
            { type: "output", text: "Installed crystal-guard-0.1.0" },
            { type: "command", text: "crystal init" },
            { type: "success", text: "Found: React + Python + MongoDB" },
            { type: "success", text: "15 quality checks loaded" },
            { type: "command", text: "crystal check" },
            { type: "success", text: "15/15 checks passed | Health: A (100/100)" },
            { type: "command", text: "crystal handoff" },
            { type: "success", text: "Handoff ready. Paste into your next AI session." },
          ]}
        />
      </div>
      <div className="mt-16 animate-fade-in-up animation-delay-700" style={{ opacity: 0, animationFillMode: "forwards" }}>
        <ChevronDown size={20} className="mx-auto text-neutral-600 animate-bounce" />
      </div>
    </div>
  </section>
);

/* ─── Terminal Block Component ─── */
const TerminalBlock = ({ lines, showCopy = false, copyText = "" }) => {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(copyText || lines.filter(l => l.type === "command").map(l => l.text).join("\n"));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <div data-testid="terminal-block" className="rounded-xl overflow-hidden border border-white/10 bg-[#0A0A0A] shadow-2xl w-full max-w-3xl mx-auto text-left">
      <div className="flex items-center justify-between px-4 py-3 bg-[#171717] border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
          <div className="w-3 h-3 rounded-full bg-[#FEBC2E]" />
          <div className="w-3 h-3 rounded-full bg-[#28C840]" />
        </div>
        <span className="text-xs font-mono text-neutral-500">terminal</span>
        {showCopy && (
          <button
            data-testid="copy-command-btn"
            onClick={handleCopy}
            className="flex items-center gap-1.5 text-xs text-neutral-500 hover:text-white transition-colors"
          >
            {copied ? <Check size={12} className="text-green-400" /> : <Copy size={12} />}
            {copied ? "Copied" : "Copy"}
          </button>
        )}
      </div>
      <div className="p-5 space-y-1.5 font-mono text-sm overflow-x-auto">
        {lines.map((line, i) => (
          <div key={i} className="flex items-start gap-2">
            {line.type === "command" && (
              <>
                <span className="text-blue-400 select-none shrink-0">$</span>
                <span className="text-neutral-200">{line.text}</span>
              </>
            )}
            {line.type === "output" && (
              <span className="text-neutral-500 pl-4">{line.text}</span>
            )}
            {line.type === "success" && (
              <>
                <Check size={14} className="text-green-400 mt-0.5 shrink-0" />
                <span className="text-green-400">{line.text}</span>
              </>
            )}
            {line.type === "error" && (
              <span className="text-red-400 pl-4">{line.text}</span>
            )}
            {line.type === "warning" && (
              <span className="text-yellow-400 pl-4">{line.text}</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

/* ─── Problem Stats ─── */
const stats = [
  { value: "36%", label: "of people using AI to code never test it", source: "arxiv, 2025" },
  { value: "1.7x", label: "more bugs in AI-written code vs human code", source: "GitHub Study, 2025" },
  { value: "45%", label: "of AI code has security holes", source: "daily.dev, 2025" },
  { value: "63%", label: "spend more time fixing AI code than writing it themselves", source: "Dev Survey, 2025" },
];

const ProblemSection = () => (
  <section id="problem" data-testid="problem-section" className="py-24 md:py-32 relative">
    <div className="max-w-7xl mx-auto px-6 md:px-12">
      <AnimatedSection>
        <p className="text-sm font-mono text-blue-400 tracking-wider uppercase mb-4">The Problem</p>
        <h2 className="text-3xl md:text-5xl tracking-tighter font-semibold text-white max-w-3xl">
          AI builds fast.<br />
          <span className="text-neutral-500">Then things break.</span>
        </h2>
        <p className="mt-6 text-neutral-400 text-lg max-w-2xl leading-relaxed">
          You tell AI to build something. It works. Next session, you add a feature. Old stuff breaks. Nobody knows why. Sound familiar?
        </p>
      </AnimatedSection>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
        {stats.map((stat, i) => (
          <AnimatedSection key={i} delay={i * 100}>
            <div
              data-testid={`stat-card-${i}`}
              className="stat-card rounded-xl border border-white/10 bg-white/[0.02] p-8 card-hover"
            >
              <span className="text-4xl md:text-5xl font-semibold tracking-tighter text-white">{stat.value}</span>
              <p className="mt-3 text-neutral-400 text-sm leading-relaxed">{stat.label}</p>
              <p className="mt-2 text-xs text-neutral-600 font-mono">{stat.source}</p>
            </div>
          </AnimatedSection>
        ))}
      </div>
    </div>
  </section>
);

/* ─── How It Works — 3 Pillars ─── */
const pillars = [
  {
    icon: Server,
    title: "While You Code",
    subtitle: "MCP Connection",
    description: "Crystal plugs into your AI tool (Cursor, Claude, VS Code). While your AI writes code, Crystal watches and says 'hey, that file belongs somewhere else' or 'that's a security risk.'",
  },
  {
    icon: Terminal,
    title: "Before You Ship",
    subtitle: "One Command",
    description: "Run crystal check. You get a score from A to F. It tells you what's wrong in plain English. Fix the red items. Ship with confidence. That's it.",
  },
  {
    icon: ShieldCheck,
    title: "On Every Push",
    subtitle: "Automatic",
    description: "Add one file to your GitHub repo. Now every time you push code, Crystal checks it automatically. Bad code can't sneak through.",
  },
];

const SolutionSection = () => (
  <section id="solution" data-testid="solution-section" className="py-24 md:py-32 border-t border-white/[0.05]">
    <div className="max-w-7xl mx-auto px-6 md:px-12">
      <AnimatedSection>
        <p className="text-sm font-mono text-blue-400 tracking-wider uppercase mb-4">How It Works</p>
        <h2 className="text-3xl md:text-5xl tracking-tighter font-semibold text-white max-w-3xl">
          It watches your code.<br />
          <span className="text-neutral-500">So you don't have to.</span>
        </h2>
        <p className="mt-6 text-neutral-400 text-lg max-w-2xl leading-relaxed">
          Crystal doesn't slow you down. It runs quietly and tells you when something's off. Think of it as spell-check, but for your code structure.
        </p>
      </AnimatedSection>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 mt-16">
        {pillars.map((pillar, i) => (
          <AnimatedSection key={i} delay={i * 150}>
            <div
              data-testid={`pillar-card-${i}`}
              className="rounded-xl border border-white/10 bg-white/[0.02] p-8 md:p-10 card-hover h-full flex flex-col"
            >
              <div className="w-12 h-12 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-6">
                <pillar.icon size={22} className="text-blue-400" />
              </div>
              <p className="text-xs font-mono text-blue-400 tracking-wider uppercase mb-2">{pillar.subtitle}</p>
              <h3 className="text-xl md:text-2xl font-medium text-white tracking-tight">{pillar.title}</h3>
              <p className="mt-4 text-neutral-400 text-sm leading-relaxed flex-1">{pillar.description}</p>
            </div>
          </AnimatedSection>
        ))}
      </div>
    </div>
  </section>
);

/* ─── Quick Start ─── */
const QuickStartSection = () => (
  <section id="quick-start" data-testid="quick-start-section" className="py-24 md:py-32 border-t border-white/[0.05]">
    <div className="max-w-7xl mx-auto px-6 md:px-12">
      <AnimatedSection>
        <div className="text-center mb-16">
          <p className="text-sm font-mono text-blue-400 tracking-wider uppercase mb-4">Get Started</p>
          <h2 className="text-3xl md:text-5xl tracking-tighter font-semibold text-white">
            Three commands.<br />
            <span className="text-neutral-500">That's all.</span>
          </h2>
        </div>
      </AnimatedSection>
      <AnimatedSection delay={200}>
        <TerminalBlock
          showCopy
          copyText="pip install crystal-guard && crystal init && crystal check"
          lines={[
            { type: "command", text: "pip install crystal-guard" },
            { type: "output", text: "Installed crystal-guard-0.1.0" },
            { type: "command", text: "crystal init" },
            { type: "success", text: "Found: React + Python + MongoDB" },
            { type: "success", text: "Created .crystal/ config" },
            { type: "success", text: "15 quality checks loaded" },
            { type: "command", text: "crystal check" },
            { type: "output", text: "" },
            { type: "success", text: "Architecture     PASS" },
            { type: "success", text: "Domain Purity    PASS" },
            { type: "warning", text: "Security         1 issue found" },
            { type: "success", text: "Code Hygiene     PASS" },
            { type: "output", text: "" },
            { type: "output", text: "Health: B (82/100)" },
            { type: "error", text: "[CRITICAL] API key found in src/config.js line 15" },
            { type: "output", text: "Fix: Move this key to your .env file" },
          ]}
        />
      </AnimatedSection>
    </div>
  </section>
);

/* ─── Features Grid — The 7 Things Crystal Does ─── */
const features = [
  {
    icon: FileText,
    title: "Picks Up Where You Left Off",
    description: "Every time you start a new AI chat, you lose context. Crystal reads your project and writes a summary. Paste it in. Your AI knows exactly what happened before.",
  },
  {
    icon: ShieldCheck,
    title: "15 Automatic Checks",
    description: "Is your password hardcoded? Is there database code in your frontend? Missing tests? Crystal runs 15 checks and tells you exactly what to fix, in plain English.",
  },
  {
    icon: BarChart3,
    title: "Tracks Your Progress",
    description: "Yesterday you had 47 files and 12 tests. Today you have 52 files and 11 tests. One test disappeared. Crystal notices and tells you.",
  },
  {
    icon: RefreshCw,
    title: "Works Across Tools",
    description: "Start in Cursor, continue in Claude, finish in Emergent. Crystal generates a handoff that works everywhere. Your context is never locked to one tool.",
  },
  {
    icon: Zap,
    title: "Helps Your AI in Real-Time",
    description: "Crystal plugs into your AI assistant via MCP. While the AI writes code, Crystal can say 'that file goes in the wrong folder' before it's too late.",
  },
  {
    icon: FolderTree,
    title: "Rules That Stick",
    description: "You define your project rules once. 'Keep database code in the backend.' 'No secrets in the code.' Crystal enforces them every session, every tool, every time.",
  },
  {
    icon: Layers,
    title: "Shows Where Problems Pile Up",
    description: "Skipped tests here, a TODO there, a security warning ignored. Crystal tracks it all across sessions and shows you: here's your debt, here's what to fix first.",
  },
];

const FeaturesSection = () => (
  <section id="features" data-testid="features-section" className="py-24 md:py-32 border-t border-white/[0.05]">
    <div className="max-w-7xl mx-auto px-6 md:px-12">
      <AnimatedSection>
        <p className="text-sm font-mono text-blue-400 tracking-wider uppercase mb-4">What Crystal Does</p>
        <h2 className="text-3xl md:text-5xl tracking-tighter font-semibold text-white max-w-3xl">
          Seven things that keep<br />
          <span className="text-neutral-500">your project alive.</span>
        </h2>
      </AnimatedSection>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-16">
        {features.map((feat, i) => (
          <AnimatedSection key={i} delay={i * 100}>
            <div
              data-testid={`feature-card-${i}`}
              className="rounded-xl border border-white/10 bg-white/[0.02] p-8 card-hover h-full"
            >
              <feat.icon size={20} className="text-blue-400 mb-4" />
              <h3 className="text-lg font-medium text-white tracking-tight">{feat.title}</h3>
              <p className="mt-3 text-neutral-400 text-sm leading-relaxed">{feat.description}</p>
            </div>
          </AnimatedSection>
        ))}
      </div>
    </div>
  </section>
);

/* ─── Use Cases ─── */
const useCases = [
  {
    title: "Building Alone",
    description: "You're making your app with AI. After a few sessions, things start breaking. Crystal keeps your project clean so it works today, tomorrow, and next month.",
    tag: "Solo",
  },
  {
    title: "Building with Others",
    description: "Two people using AI on the same project. One person's AI rewrites what the other built. Crystal enforces shared rules so everyone's work stays intact.",
    tag: "Team",
  },
  {
    title: "Open Source Projects",
    description: "People contribute code using AI tools. Crystal runs on every pull request and makes sure contributions meet your standards. Automatically.",
    tag: "Community",
  },
];

const UseCasesSection = () => (
  <section id="use-cases" data-testid="use-cases-section" className="py-24 md:py-32 border-t border-white/[0.05]">
    <div className="max-w-7xl mx-auto px-6 md:px-12">
      <AnimatedSection>
        <p className="text-sm font-mono text-blue-400 tracking-wider uppercase mb-4">Who It's For</p>
        <h2 className="text-3xl md:text-5xl tracking-tighter font-semibold text-white max-w-3xl">
          Anyone building<br />
          <span className="text-neutral-500">with AI.</span>
        </h2>
      </AnimatedSection>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 mt-16">
        {useCases.map((uc, i) => (
          <AnimatedSection key={i} delay={i * 150}>
            <div
              data-testid={`use-case-card-${i}`}
              className="rounded-xl border border-white/10 bg-white/[0.02] p-8 md:p-10 card-hover h-full flex flex-col"
            >
              <span className="inline-block self-start rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs font-mono text-neutral-400 mb-6">
                {uc.tag}
              </span>
              <h3 className="text-xl md:text-2xl font-medium text-white tracking-tight">{uc.title}</h3>
              <p className="mt-4 text-neutral-400 text-sm leading-relaxed flex-1">{uc.description}</p>
            </div>
          </AnimatedSection>
        ))}
      </div>
    </div>
  </section>
);

/* ─── Commands Reference ─── */
const commands = [
  { command: "crystal init", description: "Set up Crystal for your project. It figures out your tech stack automatically.", flags: "--stack react-python-mongo" },
  { command: "crystal check", description: "Run all 15 checks and see your project's health score (A to F).", flags: "--format json" },
  { command: "crystal handoff", description: "Create a summary to paste into your next AI coding session.", flags: "--output handoff.md" },
  { command: "crystal status", description: "See how your project is doing — score, trends, what changed.", flags: "" },
  { command: "crystal gates", description: "See each of the 15 checks one by one, with pass or fail.", flags: "" },
  { command: "crystal architect", description: "Generate an architecture.md file with your project's rules.", flags: "--output architecture.md" },
  { command: "crystal report", description: "Create a detailed report you can share or attach to a pull request.", flags: "--output report.md" },
];

const CommandsSection = () => (
  <section id="commands" data-testid="commands-section" className="py-24 md:py-32 border-t border-white/[0.05]">
    <div className="max-w-7xl mx-auto px-6 md:px-12">
      <AnimatedSection>
        <p className="text-sm font-mono text-blue-400 tracking-wider uppercase mb-4">Commands</p>
        <h2 className="text-3xl md:text-5xl tracking-tighter font-semibold text-white max-w-3xl">
          Type a command.<br />
          <span className="text-neutral-500">Get answers.</span>
        </h2>
      </AnimatedSection>
      <AnimatedSection delay={200}>
        <div className="mt-16 rounded-xl border border-white/10 overflow-hidden">
          <table data-testid="commands-table" className="w-full text-left">
            <thead>
              <tr className="border-b border-white/10 bg-white/[0.02]">
                <th className="px-6 py-4 text-xs font-mono font-medium text-neutral-400 uppercase tracking-wider">Command</th>
                <th className="px-6 py-4 text-xs font-mono font-medium text-neutral-400 uppercase tracking-wider hidden md:table-cell">What it does</th>
                <th className="px-6 py-4 text-xs font-mono font-medium text-neutral-400 uppercase tracking-wider hidden lg:table-cell">Options</th>
              </tr>
            </thead>
            <tbody>
              {commands.map((cmd, i) => (
                <tr key={i} data-testid={`command-row-${i}`} className="border-b border-white/[0.05] hover:bg-white/[0.02] transition-colors">
                  <td className="px-6 py-4">
                    <code className="text-sm font-mono text-blue-400">{cmd.command}</code>
                    <p className="md:hidden mt-1 text-xs text-neutral-500">{cmd.description}</p>
                  </td>
                  <td className="px-6 py-4 text-sm text-neutral-400 hidden md:table-cell">{cmd.description}</td>
                  <td className="px-6 py-4 hidden lg:table-cell">
                    {cmd.flags && <code className="text-xs font-mono text-neutral-600">{cmd.flags}</code>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </AnimatedSection>
    </div>
  </section>
);

/* ─── Platform Compatibility ─── */
const platforms = ["Cursor", "Windsurf", "Claude Desktop", "VS Code", "Bolt", "Lovable", "Replit", "Emergent"];

const CompatibilityStrip = () => (
  <section data-testid="compatibility-section" className="py-16 border-t border-white/[0.05]">
    <div className="max-w-7xl mx-auto px-6 md:px-12 text-center">
      <p className="text-xs font-mono text-neutral-600 uppercase tracking-widest mb-8">Works with any AI coding tool</p>
      <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-4">
        {platforms.map((p, i) => (
          <span key={i} data-testid={`platform-${i}`} className="text-sm text-neutral-500 font-medium">{p}</span>
        ))}
      </div>
    </div>
  </section>
);

/* ─── Footer CTA ─── */
const Footer = () => (
  <footer data-testid="footer-section" className="py-24 md:py-32 border-t border-white/[0.05]">
    <div className="max-w-7xl mx-auto px-6 md:px-12 text-center">
      <AnimatedSection>
        <h2 className="text-3xl md:text-5xl tracking-tighter font-semibold text-white">
          Build with AI.<br />
          <span className="text-neutral-500">Ship with Crystal.</span>
        </h2>
        <p className="mt-6 text-neutral-400 text-lg max-w-xl mx-auto">
          Free. Open source. Takes 30 seconds to set up. Works with every AI coding tool.
        </p>
        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            data-testid="footer-github-btn"
            className="inline-flex items-center gap-2 rounded-md bg-white px-8 py-4 text-sm font-medium text-black hover:bg-neutral-200 transition-colors"
          >
            <GitBranch size={16} />
            Star on GitHub
            <ExternalLink size={14} className="opacity-50" />
          </a>
          <a
            href="#quick-start"
            data-testid="footer-quickstart-btn"
            className="inline-flex items-center gap-2 rounded-md border border-white/20 bg-transparent px-8 py-4 text-sm font-medium text-white hover:bg-white/10 transition-colors"
          >
            Get Started
          </a>
        </div>
      </AnimatedSection>
      <div className="mt-24 pt-8 border-t border-white/[0.05] flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-md bg-white/10 border border-white/20 flex items-center justify-center">
            <ShieldCheck size={12} className="text-blue-400" />
          </div>
          <span className="font-mono text-xs text-neutral-500">Crystal</span>
        </div>
        <p className="text-xs text-neutral-600">
          MIT License. Free forever. Built for people who build with AI.
        </p>
        <div className="flex items-center gap-6">
          <a href="https://github.com" className="text-xs text-neutral-500 hover:text-white transition-colors">GitHub</a>
          <a href="#commands" className="text-xs text-neutral-500 hover:text-white transition-colors">Commands</a>
          <a href="#quick-start" className="text-xs text-neutral-500 hover:text-white transition-colors">Get Started</a>
        </div>
      </div>
    </div>
  </footer>
);

/* ─── App ─── */
function App() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Nav />
      <Hero />
      <ProblemSection />
      <SolutionSection />
      <QuickStartSection />
      <FeaturesSection />
      <UseCasesSection />
      <CommandsSection />
      <CompatibilityStrip />
      <Footer />
    </div>
  );
}

export default App;
