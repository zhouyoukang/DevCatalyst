---
name: error-diagnosis
description: Systematic diagnosis and resolution of code errors - bugs, exceptions, crashes, unexpected behavior.
---

## Diagnosis Flow

### 1. Reproduce & Confirm
- Complete error message recorded
- Clear reproduction steps
- Environment info (OS/language/dependency versions)

### 2. Root Cause Location
- Trace from error stack to source
- Check recent changes (git diff/log)
- Narrow scope: binary search elimination

### 3. Error Patterns
| Type | Keywords | Common Cause |
|------|----------|-------------|
| NPE | `null`, `undefined`, `None` | Missing null check |
| ClassCast | `cannot be cast`, `TypeError` | Type mismatch |
| OOM | `OutOfMemory`, `heap` | Large objects/leak |
| Timeout | `timeout`, `ETIMEDOUT` | Network/deadlock |
| Permission | `denied`, `EACCES`, `403` | Insufficient permissions |
| Port conflict | `EADDRINUSE` | Port already in use |

### 4. Fix Principles
- Fix root cause, not symptoms
- Minimal change principle
- Add defensive code to prevent recurrence
- Add test covering this scenario

### 5. Record
- Write error pattern to Memory (create_memory)
- Major incidents go into rule files
