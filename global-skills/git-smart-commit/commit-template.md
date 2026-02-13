# Git Commit Message Template

## Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Type Quick Reference
| Type | Use | Example |
|------|-----|--------|
| feat | New feature | `feat(auth): add OAuth2 login` |
| fix | Bug fix | `fix(api): prevent NPE in user query` |
| refactor | Refactoring | `refactor(utils): extract date formatting` |
| perf | Performance | `perf(db): add index on user_email` |
| docs | Documentation | `docs(readme): update installation guide` |
| style | Formatting | `style: fix indentation in config` |
| test | Tests | `test(auth): add login failure cases` |
| chore | Build/deps | `chore(deps): upgrade kotlin to 2.0` |
| ci | CI/CD | `ci: add GitHub Actions workflow` |

## Scope Suggestions
- Use module/directory name as scope
- Omit scope if affecting multiple modules

## Subject Rules
- Max 60 characters
- Imperative mood (add, fix, update — not added, fixed)
- No period
- Lowercase first letter

## Body (Optional)
- Explain WHY, not WHAT (code already shows what)
- Blank line before body
- Max 72 chars per line

## Footer (Optional)
- `BREAKING CHANGE: <description>` — Breaking changes
- `Closes #123` — Close issue
- `Refs #456` — Reference issue
