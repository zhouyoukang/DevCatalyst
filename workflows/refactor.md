---
description: Safe code refactoring — extract functions, rename, simplify logic, eliminate duplication
---

# /refactor — Code Refactoring Workflow

## Phase 1: Analyze (Read-only)
1. Locate target code with `grep_search` + `read_file`
2. Identify type: Extract Function | Eliminate Duplication | Simplify Conditions | Rename | Move Method | Extract Interface

## Phase 2: Safety Assessment
1. Confirm scope: files + call sites
2. Check test coverage (write tests first if none)
3. Confirm no external behavior change

## Phase 3: Execute
- One refactoring technique per pass
- Use `multi_edit` for same-file changes
- Update all call sites synchronously
- Maintain existing code style

## Phase 4: Verify
1. All imports updated
2. All call sites synchronized
3. Build verification (if applicable)
4. Run tests (if available)

## Phase 5: Summary
```
## Refactoring Complete
- **Technique**: [type]
- **Files Modified**: N
- **Verification**: [status]
```
