---
description: Analyze and optimize code performance — slow code, high memory, performance tuning
---

# /optimize — Performance Optimization Workflow

## Phase 1: Locate Bottleneck
1. **Time complexity** — Find O(n²) or worse
2. **I/O bottleneck** — File/network/DB call frequency
3. **Memory** — Large allocs, leak risks
4. **Hot functions** — Frequently called paths

## Phase 2: Choose Strategy
| Bottleneck | Strategy | Risk |
|-----------|----------|------|
| Algorithm O(n²) | Better data structure/algorithm | Low |
| Repeated computation | Cache/memoize | Low |
| Many small I/O | Batch processing | Medium |
| Sync blocking | Async/concurrent | Medium |
| Frequent large allocs | Object pool/reuse | Medium |
| Unnecessary loading | Lazy load/on-demand | Low |

## Phase 3: Implement
- Measure → optimize → measure again
- One bottleneck per pass
- Don't sacrifice readability

## Phase 4: Verify
```
## Optimization Results
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| [metric] | [val] | [val] | [%] |
```
