---
name: architecture-design
description: Design and evaluate software architecture. Triggered when planning feature architecture, evaluating tech choices, or making architecture decisions.
---

## Architecture Decision Flow

### 1. Clarify Requirements
- Functional requirements (must implement)
- Non-functional (performance/security/scalability)
- Constraints (tech stack/team/timeline)

### 2. Compare Options
| Dimension | Option A | Option B |
|-----------|----------|----------|
| Complexity | | |
| Performance | | |
| Maintainability | | |
| Learning curve | | |
| Ecosystem | | |

### 3. Common Patterns
- **Layered**: UI → Business → Data (most common)
- **Microservices**: Independently deployable services
- **Event-driven**: Pub/sub decoupling
- **CQRS**: Read/write separation
- **Clean Architecture**: Dependency inversion

### 4. Output ADR
```markdown
# ADR-YYYYMMDD: Title
## Context
## Decision
## Rationale
## Consequences
## Alternatives
```
