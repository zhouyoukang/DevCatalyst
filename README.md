# DevCatalyst

**A tiny config that catalyzes your AI coding assistant into a truly intelligent collaborator.**

> 一小段文字，释放 AI 编程助手的全部智能。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What is this?

DevCatalyst is a **self-disciplined configuration architecture** that transforms AI coding assistants (like Windsurf Cascade) from "instruction executors" into "intelligent collaborators".

- 📦 **Minimal** — Core rules under 6000 characters, yet dramatically improve AI code quality, proactivity, and problem-solving
- 🧬 **Self-disciplined** — Built-in rule budget + change protocol + lifecycle management to **prevent config bloat**
- 🔄 **Self-evolving** — AI automatically observes, records, and optimizes its own configuration during daily work
- 🛡️ **Safe** — Cross-project modifications have protection mechanisms; global config changes require confirmation
- ⚡ **One-click deploy** — A single prompt completes full installation

## The Problem: Rule Entropy

Every AI coding assistant user encounters this:

```
Keep adding rules → Short-term effective → Long-term redundant/contradictory → AI efficiency drops → Add more rules to fix → Vicious cycle
```

Existing solutions (ARM, aicodingrules.org) solve rule **distribution**, but not **self-discipline during evolution**.

DevCatalyst's core innovation is the **Rule Compiler Pattern**:

| Mechanism | Purpose |
|-----------|--------|
| **Budget System** | always-on rules total ≤ 6000 chars, forced conciseness |
| **Change Protocol** | When user says "add a rule", AI first routes → conflict checks → budget checks |
| **Lifecycle** | New ideas default to Memory for observation; validated 3+ times before becoming rules |
| **Rule Compiler** | `/evolve` periodically deduplicates, compresses, downgrades unused rules |

## Architecture

```
┌─────────────────────────────────────┐
│  Layer 0: Kernel (≤500 chars)       │ ← 3 meta-rules, immutable
│  Budget | Change Protocol | No-blind-add │
├─────────────────────────────────────┤
│  Layer 1: Framework (≤3000 chars)   │ ← Decision framework + Execution engine
│  PREDICT | ESCALATION | Safety      │
├─────────────────────────────────────┤
│  Layer 2: Extensions (≤2500 chars)  │ ← Project-specific + User-defined
│  Language rules | Structure | Custom │
└─────────────────────────────────────┘
```

## Quick Start

### Option 1: One-click Deploy (Recommended)

In Windsurf, start a new conversation and paste:

```
Please read {path-to-DevCatalyst}/installer/INSTALLER.md and execute the full installation.
```

### Option 2: Manual Install

1. **Global Rules**: Copy `core/global-rules.md` content to Windsurf Settings → AI Rules
2. **Project Rules**: Create `.windsurf/rules/` in your project, add `soul.md` and `execution-engine.md`
3. **Verify**: Run `/health-check` to confirm installation

## What's Included

```
DevCatalyst/
├── core/                       # Core rules (Layer 0+1)
│   ├── kernel.md               # 3 immutable meta-rules
│   ├── global-rules.md         # Global behavior rules
│   ├── soul.md                 # AI thinking kernel
│   └── execution-engine.md     # Execution engine
├── project-templates/          # Project templates (Layer 2)
│   ├── PROJECT_SETUP.md        # Auto-init guide for AI
│   ├── AGENTS.md.template      # Directory-level instructions
│   ├── hooks.json              # Safe hooks template
│   ├── skills/                 # Project skill templates
│   └── workflows/              # Project workflow templates
├── global-skills/              # 23+ global skills
│   ├── code-review/            # Code review
│   ├── error-diagnosis/        # Error diagnosis
│   ├── refactor-code/          # Code refactoring
│   ├── ... and 20 more
├── workflows/                  # 12 standard workflows
│   ├── blueprint.md            # Plan-Review-Execute blueprint
│   ├── evolve.md               # Self-evolution
│   ├── health-check.md         # Health check
│   ├── onboard.md              # New project onboarding
│   └── ... and 8 more
├── installer/                  # Installation system
│   ├── INSTALLER.md            # Auto-install instructions
│   └── INSTALL_PROMPT.md       # Starter prompt
├── hooks/examples/             # Python hook examples
├── settings/                   # IDE config templates
│   ├── settings.json.template
│   ├── MCP_GUIDE.md            # MCP recommendation guide
│   └── WINDSURF_UI_SETUP.md
├── scripts/                    # Automation scripts
│   └── verify-installation.ps1
└── docs/                       # Documentation
    ├── ARCHITECTURE.md          # Two-layer architecture
    └── ARCHITECTURE_v5.md       # v5.0 self-discipline design
```

## Core Concepts

### PREDICT Decision Framework

- **P**redict — What will the user need next?
- **R**esearch — Is there a better approach? Search first.
- **E**xecute — Complete in one shot, no half-finished work
- **D**ocument — Write findings to Memory, not "in your head"
- **I**terate — Reflect: what could be better?
- **C**omplete — Proactively fill gaps the user didn't mention
- **T**ransfer — Can this experience transfer to other scenarios?

### ESCALATION Problem-Solving

1. **L1** Self-solve (simple changes only)
2. **L2** Research (default starting point) — search + docs + community
3. **L3** Collaborate — ask user to observe what AI can't see
4. **L4** User-directed — admit failure, ask for direction

### Self-Disciplined Evolution

- **Dual Output**: Every interaction produces task result + system evolution
- **Rule Routing**: 80% of "rule requests" should go to Memory or Skills, not rule files
- **Quality Gate**: Repeatability + Generality + Actionability + No-conflict → all 4 Yes to solidify

## Workflows

| Command | Function |
|---------|----------|
| `/blueprint` | Plan-Review-Execute: research → plan → review → execute → verify |
| `/evolve` | System evolution: audit + compile + optimize rules/Skills/Memory |
| `/evolve-auto` | Auto-evolution: scan conversations → extract patterns → optimize |
| `/health-check` | Health check: detect config completeness + budget usage |
| `/review` | Code review |
| `/debug-escalation` | Layered debug escalation |
| `/refactor` | Code refactoring |
| `/optimize` | Performance optimization |
| `/test` | Test writing |
| `/doc` | Documentation generation |
| `/onboard` | New project: scan → detect stack → auto-configure |
| `/observatory` | AI Observatory: monitoring + dashboard |

## Comparison

| Feature | DevCatalyst | ARM | .cursorrules |
|---------|-------------|-----|-------------|
| Distribution | ✅ One-click | ✅ Package manager | ❌ Manual copy |
| Anti-bloat | ✅ Budget + Compiler | ❌ | ❌ |
| Self-evolution | ✅ Passive + Active | ❌ | ❌ |
| Change Protocol | ✅ Route + Conflict + Budget | ❌ | ❌ |
| Lifecycle | ✅ proposed→validated→deprecated | ❌ | ❌ |
| Cross-IDE | ⏳ Windsurf (expanding) | ✅ Multi-IDE | ❌ Cursor only |

## Compatibility

- ✅ **Windsurf (Cascade)** — Full support
- ⏳ **Cursor** — Planned
- ⏳ **GitHub Copilot** — Planned
- ⏳ **Claude Code** — Planned

## Version History

- **v5.1** — Human-AI collaboration + anti-degradation + full-cycle autonomy
- **v5.0** — Self-discipline architecture: Budget + Change Protocol + Rule Compiler + Lifecycle
- v4.0 — Rules reduced 75% + Hooks policy fix + MCP guide + Context Engineering
- v3.0 — Living Intelligence Architecture + Two-layer separation
- v2.0 — Incident-driven upgrade
- v1.0 — Initial version

## Contributing

Contributions welcome! Especially:
- New IDE adapters (Cursor / Copilot / Claude Code)
- New global Skills
- New workflow templates
- Bug reports and improvement suggestions

## License

MIT
