---
name: dependency-manage
description: Manage project dependencies - add/update/remove packages, resolve version conflicts.
---

## Package Managers
| Language | Manager | Lock File | Install |
|----------|---------|-----------|--------|
| Node.js | npm/yarn/pnpm | package-lock.json | `npm ci` |
| Python | pip/poetry | requirements.txt | `pip install -r` |
| Java/Kotlin | Gradle/Maven | gradle.lockfile | `./gradlew dependencies` |
| Go | go mod | go.sum | `go mod tidy` |
| Rust | cargo | Cargo.lock | `cargo build` |

## Common Operations
```bash
# Node.js
npm outdated          # Check outdated
npm audit             # Security audit
npm update <pkg>      # Update single package

# Python
pip list --outdated
pip install --upgrade <pkg>

# Gradle
./gradlew dependencies
./gradlew dependencyUpdates
```

## Conflict Resolution
1. View dependency tree to find conflict source
2. Use `resolutionStrategy` (Gradle) or `overrides` (npm) to force version
3. Upgrade to compatible versions
