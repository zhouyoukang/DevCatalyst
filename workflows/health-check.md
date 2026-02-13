---
description: System health check — detect config completeness, auto-recover if missing
---

# Health Check Workflow

## Phase 1: File Existence

### 1.1 Global Config
// turbo
- `~/.codeium/windsurf/memories/global_rules.md`
- `~/.codeium/windsurf/hooks.json` — must be `{"hooks": {}}` (no PowerShell!)

### 1.2 Project Rules
// turbo
- `.windsurf/rules/soul.md` (required)
- `.windsurf/rules/execution-engine.md` (required)
- `.windsurf/rules/project-structure.md` (required)

### 1.3-1.6 Skills, Workflows, AGENTS.md, hooks.json
// turbo
Check existence and safety.

## Phase 2: Content Integrity
1. global_rules.md — contains `PREDICT`
2. soul.md — contains `ESCALATION`
3. execution-engine.md — contains PowerShell hooks forbidden
4. hooks.json — no `powershell` or `pre_run_command`

## Phase 3: Recovery
- Global rules: recover from DevCatalyst `core/global-rules.md`
- Project rules: recover from `.windsurf/backups/rules/` or DevCatalyst `core/`
- Contaminated hooks.json: clear to `{"hooks": {}}`

## Phase 4: Report
```
| Category | Files | Status | Missing |
|----------|-------|--------|---------|
| Global Rules | 1/1 | ✅ | - |
| Project Rules | N/N | ✅ | - |
| Skills | N/N | ✅ | - |
| Workflows | N/N | ✅ | - |
| AGENTS.md | N/N | ✅ | - |
| hooks.json | Safe | ✅ | - |
```
