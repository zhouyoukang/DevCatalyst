---
name: log-analysis
description: Analyze logs and debug output - interpret error logs, trace request chains, locate anomalies.
---

## Analysis Flow

### 1. Quick Locate
```bash
# Search error keywords
grep -i "error\|exception\|fatal\|fail" app.log | tail -20

# Filter by time range
grep "2026-02-13T02:" app.log

# Count error frequency
grep -c "ERROR" app.log
```

### 2. Log Levels
| Level | Meaning | Priority |
|-------|---------|----------|
| FATAL | System crash | 🔴 Immediate |
| ERROR | Operation failed | 🔴 Fix needed |
| WARN | Potential issue | 🟡 Monitor |
| INFO | Normal event | 🟢 Reference |
| DEBUG | Debug detail | ⚪ Dev only |

### 3. Android logcat
```bash
adb logcat -s "MyTag"
adb logcat --pid=$(adb shell pidof com.example.app)
adb logcat -d -t 50
```

### 4. Output Format
```
## Log Analysis Results
- **Key log lines**: <quote>
- **Impact scope**: <description>
- **Recommendation**: <fix plan>
```
