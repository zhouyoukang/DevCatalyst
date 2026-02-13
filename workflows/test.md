---
description: Write and run tests — add tests, verify correctness, improve coverage
---

# /test — Testing Workflow

## Phase 1: Analyze Test Needs
1. Determine type: Unit | Integration | E2E | Regression
2. Determine framework:
   | Language | Framework | Command |
   |----------|-----------|--------|
   | Kotlin/Java | JUnit5 + MockK | `./gradlew test` |
   | TypeScript | Jest / Vitest | `npm test` |
   | Python | pytest | `pytest -v` |
   | Go | testing | `go test ./...` |
   | Rust | cargo test | `cargo test` |

## Phase 2: Write Tests
**AAA Pattern** (Arrange → Act → Assert)

**Must cover**:
- ✅ Happy path
- ✅ Boundary conditions (null, zero, max, empty)
- ✅ Error paths (bad input, no permission, network failure)
- ✅ Concurrency (if applicable)

**Naming**: `should_[expected]_when_[condition]`

## Phase 3: Run Tests
// turbo
Execute test command, analyze results.

## Phase 4: Coverage (Optional)
```bash
./gradlew jacocoTestReport  # Kotlin/Java
npx jest --coverage          # JavaScript
pytest --cov=src             # Python
```

## Phase 5: Summary
```
## Test Results
- **New tests**: N
- **Coverage**: happy/boundary/error/concurrency
- **Result**: all passed / N failed
```
