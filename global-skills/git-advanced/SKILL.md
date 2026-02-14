---
name: git-advanced
description: Advanced Git operations - branch management, conflict resolution, rebase, cherry-pick, history rewriting.
---

## Branch Strategy
```bash
git checkout -b feature/xxx     # Feature branch
git checkout -b fix/xxx         # Fix branch
git checkout -b release/x.x     # Release branch
```

## Merge Conflict Resolution
```bash
git merge feature/xxx
# Manually resolve <<<< ==== >>>> markers
git add <resolved-files>
git merge --continue
```

## Rebase (Linear History)
```bash
git rebase main                 # Rebase onto main
git rebase -i HEAD~3            # Interactive rebase
```

## Cherry-pick
```bash
git cherry-pick <commit-sha>    # Pick single commit
git cherry-pick A..B            # Pick range
```

## Safety Principles
- `git log --oneline -5` before pushing
- Never force push on public branches
- Create backup branch before major operations
