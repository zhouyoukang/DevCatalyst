---
description: System self-evolution — audit rules/Skills/Memory/MCP, find improvements and implement
---

# /evolve — System Self-Evolution (DevCatalyst v5.0)

## Phase 0: Budget Audit
// turbo
1. Read all `.windsurf/rules/*.md` with `trigger: always_on`
2. Count chars per file and total
3. Compare with 6000 char budget
4. Output: usage % + per-file breakdown

## Phase 1: Rules Audit
// turbo
Check for: outdated, conflicting, missing, bloated rules

## Phase 2: Skills Audit
// turbo
Check: validity, repeated operations needing new Skills, underused global Skills

## Phase 3: Memory Audit
Check: stale, duplicate, missing memories

## Phase 4: Tools & MCP Audit
Check: usage, underutilized capabilities, new services worth suggesting

## Phase 5: User Pattern Analysis
Check: common tasks, prompt quality trends, uncovered scenarios

## Phase 5.5: Rule Compilation (Anti-Entropy Core)
1. **Deduplicate**: Merge semantically duplicate rules
2. **Compress**: Simplify while preserving semantics (5-15% per pass)
3. **Downgrade**: Unused rules → Memory, free budget
4. **Upgrade**: Memory validated 3+ times → rules (if budget allows)
5. **Conflict scan**: Detect contradictions

## Phase 6: Implement
1. Fix immediately: clear errors, outdated info
2. Suggest: trade-off improvements for user choice
3. Record: uncertain → Memory for observation
4. Plan: large changes → next /evolve todo

## Phase 7: Report
```
## 🧬 Evolution Report
### Scope
Rules: N | Skills: N | Memory: N | MCP: N

### Findings
| Category | Finding | Action | Status |
|----------|---------|--------|--------|

### Metrics
- Budget: [N/6000] ([X%])
- Health: [score]
- Compilation: compressed [N] chars | upgraded [N] | downgraded [N]
```
