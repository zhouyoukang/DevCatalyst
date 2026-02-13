---
description: Full-stack dev pipeline — from one-line requirement to complete delivery
---

# /dev — Full-Stack Development Pipeline

> Copy to `.windsurf/workflows/dev.md`, replace `<PLACEHOLDER>` with project values.

## Phase 0: Understand (30 sec)
Decompose: **what** + **where** + **affected**
Classify: `NEW_FEATURE` | `BUG_FIX` | `REFACTOR` | `CONFIG` | `DOC`

## Phase 1: Impact Analysis (1-2 min)
Locate modules, read AGENTS.md, search code, assess sync needs.

## Phase 2: Design (NEW_FEATURE only)
Search existing patterns, follow them, determine approach.

## Phase 3: Implement
Backend first → frontend sync → related changes.
Use `multi_edit`, maintain style, no unnecessary comments.

## Phase 4: Build
```
<BUILD_COMMAND_PLACEHOLDER>
```
Max 2 fix rounds if compile fails.

## Phase 5: Deploy & Test
```
<DEPLOY_COMMAND_PLACEHOLDER>
<VERIFY_COMMAND_PLACEHOLDER>
```

## Phase 6: Documentation
Update status docs, module docs, API docs, ADR as needed.

## Phase 7: Summary
What was done + files modified + status + items needing user verification.

## Adaptation
| Placeholder | Example |
|-------------|---------|
| `<BUILD_COMMAND>` | `./gradlew assembleDebug` |
| `<DEPLOY_COMMAND>` | `adb push + install` |
| `<VERIFY_COMMAND>` | `curl http://localhost:8080/` |
