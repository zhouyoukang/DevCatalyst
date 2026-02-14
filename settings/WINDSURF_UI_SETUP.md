# Windsurf UI Setup Checklist

> These settings can only be configured through the Windsurf UI, not via settings.json.

## Required (Core AI capability)

### 1. Cascade Gitignore Access
- **Path**: Windsurf Settings → Search "Cascade Gitignore"
- **Action**: **Enable** "Allow Cascade to access files matching .gitignore patterns"
- **Impact**: AI can read config files blocked by .gitignore

### 2. Auto-Run Commands
- **Path**: Windsurf Settings → Search "Auto Run"
- **Recommended**: `Allowlist Only`

### 3. Memory
- **Path**: Windsurf Settings → Search "Memory"
- **Action**: Confirm enabled

## Recommended

### 4. Inline Completion
- Confirm enabled for real-time code suggestions

### 5. Supercomplete
- Enable if available for multi-line completions

## Verification

- [ ] Type `@code-review` in Cascade to test skill trigger
- [ ] Run `echo test` in terminal to confirm normal closure
- [ ] Try AI reading `.vscode/settings.json` to confirm gitignore access
