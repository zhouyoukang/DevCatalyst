---
name: code-review
description: Comprehensive code review checking logic errors, security vulnerabilities, performance issues, and code style.
---

## Review Dimensions

### 1. Correctness
- Logic correct, edge cases covered
- Null checks complete
- Exception handling appropriate

### 2. Security
- Input validated and escaped
- Sensitive data not exposed
- SQL injection/XSS/CSRF risks

### 3. Performance
- Algorithm complexity reasonable
- No unnecessary loops/repeated computation
- Memory leak risks (unclosed resources)

### 4. Maintainability
- Semantic naming
- Single responsibility functions
- No magic numbers/hardcoded values

### 5. Best Practices
- Guard clauses / early return (not deep nesting)
- Functions >30 lines should be split
- Semantic naming (`isLoading` not `flag1`)
- No debug code remnants (console.log, print)

## Output Format
```
## Code Review Results

### 🔴 Must Fix
- [file:line] Issue → Fix suggestion

### 🟡 Suggested Improvements
- [file:line] Issue → Improvement

### 🟢 Well Done
- Highlights
```
