# Project Layer Auto-Init Guide

> AI reads this file in new projects to auto-create project-specific rules and config.
> AI should adapt based on the actual project, not mechanically copy.

## Trigger

When AI first works in a project without `.windsurf/rules/`, auto-execute this flow.

## Phase 1: Project Analysis

1. Detect project type via config files (package.json, build.gradle, requirements.txt, etc.)
2. Analyze directory structure
3. Identify tech stack (language, framework, build system)

## Phase 2: Create Rules

### Required files:
- `.windsurf/rules/kernel.md` — Copy from core/kernel.md (immutable meta-rules)
- `.windsurf/rules/soul.md` — Copy from core/soul.md (AI thinking kernel)
- `.windsurf/rules/execution-engine.md` — Copy from core/execution-engine.md
- `.windsurf/rules/project-structure.md` — **Create based on project analysis**

### Optional (based on detected tech stack):
- `kotlin-android.md` / `typescript-react.md` / `python.md` etc.

## Phase 3: Create Workflows

### Required:
- `debug-escalation.md` — Copy from workflows/ (100% universal)
- `evolve.md` — Copy from workflows/ (100% universal)
- `health-check.md` — Adapt based on project file list
- `dev.md` — Adapt build/deploy commands for project

### Optional (copy from workflows/):
- review.md, refactor.md, optimize.md, test.md, doc.md

## Phase 4: Create AGENTS.md

Create in root and key subdirectories with module responsibilities and constraints.

## Phase 5: Initialize Backups

1. Create `.windsurf/backups/rules/`
2. Copy all rules to backup
3. Create MANIFEST.md

## Phase 6: Create hooks.json

```json
{"hooks": {}}
```

> Python/Node.js hooks: safe. PowerShell hooks: **FORBIDDEN**.
