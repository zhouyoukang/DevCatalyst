# DevCatalyst v5.0 — Auto-Install Instructions

> This file is read by AI and executed automatically.
> AI should execute all steps in order without interruption.
>
> **Architecture**: Two-layer design (see docs/ARCHITECTURE.md):
> - **Layer 1** (Step 1-5): Global config, deploy once
> - **Layer 2** (Step 6-7): Project-specific, AI auto-adapts

---

## Step 1: Deploy Global Skills

Copy each subdirectory from `global-skills/` to the global Skills directory:

```
Target: %USERPROFILE%\.codeium\windsurf\skills\
```

Verify: Check for 23 SKILL.md files in the target directory.

## Step 2: Deploy settings.json

**Merge** (not overwrite) `settings/settings.json.template` into user settings:

```
Target: %APPDATA%\Windsurf\User\settings.json
```

Critical settings:
- `"terminal.integrated.defaultProfile.windows": "Windows PowerShell"`
- `"terminal.integrated.shellIntegration.enabled": true`

## Step 3: Clear Global Hooks

Ensure global hooks.json is empty:

```
Target: %USERPROFILE%\.codeium\windsurf\hooks.json
Content: {"hooks": {}}
```

> **Hooks Policy (v5.0)**:
> - **Python/Node.js hooks**: Safe to use (logging, formatting, security)
> - **PowerShell hooks**: **ABSOLUTELY FORBIDDEN** (proven to break terminal)

## Step 4: Apply Global Rules

Merge `core/global-rules.md` content into:

```
File: %USERPROFILE%\.codeium\windsurf\memories\global_rules.md
```

- Character limit: 12000/file
- Takes effect in new conversations without IDE restart

## Step 5: Deploy Safe Write Tool

Copy `scripts/_safe_write.py` to global location:

```
Target: %USERPROFILE%\.codeium\windsurf\_safe_write.py
```

> This tool routes file writes through the terminal channel, bypassing IDE edit tool hangs (~25% failure rate).
> Usage: `python _safe_write.py batch <instruction.json>`

## Step 6: Windsurf UI Settings (Manual)

See `settings/WINDSURF_UI_SETUP.md` for details:
1. Cascade Gitignore access → Enable
2. Auto-run commands → Allowlist Only
3. Memory → Confirm enabled
4. Inline Completion → Confirm enabled

## Step 7: Project Layer (Layer 2)

Read `project-templates/PROJECT_SETUP.md` and auto-configure:
1. Analyze project type
2. Create `.windsurf/rules/` with kernel.md + soul.md + execution-engine.md
3. Create workflows
4. Create AGENTS.md
5. Create hooks.json (`{"hooks": {}}`)

## Step 8: Verify

1. Check global Skills count (expected: 23)
2. Check settings.json has correct terminal profile
3. Check hooks.json is safe
4. Check project rules exist

Optional: Run `scripts/verify-installation.ps1`
