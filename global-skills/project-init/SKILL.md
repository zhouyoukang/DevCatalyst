---
name: project-init
description: Initialize Windsurf intelligent configuration for new projects. Triggered when starting a new project or configuring Windsurf rules/Skills/AGENTS.md.
---

## New Project Windsurf Config Init

> **If you have the distribution pack**: Read `project-templates/PROJECT_SETUP.md` and follow its full flow.
> Below is a simplified flow without the distribution pack.

### 1. Auto-detect Project Type
// turbo
Use `find_by_name` to detect:
- `package.json` → Node.js | `build.gradle*` → Android/JVM
- `requirements.txt` / `pyproject.toml` → Python | `Cargo.toml` → Rust
- `go.mod` → Go | `*.sln` / `*.csproj` → .NET

### 2. Create Directory Structure
// turbo
```
.windsurf/rules/          ← Rule files
.windsurf/skills/          ← Project skills
.windsurf/workflows/       ← Workflows
.windsurf/backups/rules/   ← Rule backups
```

### 3. Create Core Rule Files
- `.windsurf/rules/kernel.md` (Always On) — 3 immutable meta-rules
- `.windsurf/rules/soul.md` (Always On) — AI thinking kernel
- `.windsurf/rules/execution-engine.md` (Always On) — Execution engine
- `.windsurf/rules/project-structure.md` (Always On) — **Must create based on project**
- Tech-stack rules (Glob) — based on detected stack

### 4. Create AGENTS.md
Root directory required, key subdirectories optional.

### 5. Create Workflows
- `debug-escalation.md` + `evolve.md` + `health-check.md` + `review.md` (universal)
- `dev.md` (adapt to project build commands)

### 6. Create hooks.json
`{"hooks": {}}` — **Never place any PowerShell hooks**

### 7. Init Backup System
- Copy rules/*.md → backups/rules/
- Create backups/MANIFEST.md

### Checklist
- [ ] `.windsurf/rules/` has soul + execution-engine + project-structure
- [ ] Root `AGENTS.md` created
- [ ] `.windsurf/hooks.json` is empty hooks
- [ ] `.windsurf/backups/` initialized
- [ ] Workflows: at least debug-escalation + health-check + dev
