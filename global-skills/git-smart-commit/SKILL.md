---
name: git-smart-commit
description: Smart Git commits - analyze changes, generate conventional commit messages, handle staging and pushing.
---

## Commit Message Convention
Format: `<type>(<scope>): <description>`

Types:
- `feat` — New feature
- `fix` — Bug fix
- `refactor` — Refactoring (no behavior change)
- `docs` — Documentation
- `style` — Formatting (no logic change)
- `perf` — Performance
- `test` — Tests
- `chore` — Build/tools/dependencies

Examples:
```
feat(auth): add OAuth2 login support
fix(api): prevent null pointer in user query
refactor(utils): extract date formatting to shared module
```

## Commit Flow
```bash
git status --short
git diff --stat
git add -A
git commit -m "<message>"
```

## Principles
- One commit = one thing
- No debug code remnants
- Never commit build artifacts or secrets
