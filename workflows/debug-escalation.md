---
description: Layered bug debugging escalation — avoid blind fixes that cause more problems
---

# Bug Debug Escalation Workflow

## When to Use
- Bug cause is unclear
- Involves IDE/system/global config issues
- First fix attempt failed

## Flow

### Phase 1: Freeze the Scene (Do This First)
1. **Record current state**: List all related file contents (`read_file`)
2. **Record symptoms**: Precisely describe what happened
3. **Create rollback point**: Backup files before modifying

### Phase 2: L1 Self-Analysis (Max 2 Rounds)
1. Analyze possible causes with existing knowledge
2. **Single-variable change**: Only modify one thing at a time
3. Ask user to confirm actual effect
4. If 2 rounds unsolved → immediately enter Phase 3

### Phase 3: L2 Research
1. `search_web`: official docs + GitHub Issues + community
2. Compare search results with current symptoms
3. Found solution → execute; Not found → enter Phase 4

### Phase 4: L3 Human-AI Collaboration
Structured help request with: Current Problem, Already Tried, Need Help With, Guesses

### Phase 5: L4 User-Directed
User provides direction, AI investigates and executes.

## Key Discipline
- **Never exceed 2 rounds in Phase 2**
- **Backup before every modification**
- **Recovery over rebuild**: rollback first if fix causes new issues
