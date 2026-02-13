---
name: refactor-code
description: Safely refactor code - extract functions, rename, simplify logic, eliminate duplication.
---

## Refactoring Principles
- One refactoring technique per pass
- Ensure test coverage before refactoring (write tests first if none)
- Maintain behavior (external behavior unchanged)

## Common Techniques

### 1. Guard Clauses / Early Return (Highest Priority)
```kotlin
// ✗ Deep nesting
fun process(input: String?) {
    if (input != null) {
        if (input.isNotEmpty()) {
            // actual logic
        }
    }
}

// ✓ Early Return
fun process(input: String?) {
    if (input.isNullOrEmpty()) return
    // actual logic (happy path last)
}
```

### 2. Extract Function (when >30 lines)
### 3. Eliminate Duplication (DRY, extract when same logic appears 2x)
### 4. Rename (semantic: `isLoading` / `hasError` not `flag1`)
### 5. Extract Constants (eliminate magic numbers)
### 6. Merge Conditions (simplify complex if/else chains)
### 7. Extract Interface (abstract common behavior)
### 8. Move Method (to more appropriate module/class)

## Safety Checklist
- [ ] All call sites updated
- [ ] No missing imports/exports
- [ ] Compiles successfully after refactoring
- [ ] Tests pass (if available)
- [ ] No external behavior change
