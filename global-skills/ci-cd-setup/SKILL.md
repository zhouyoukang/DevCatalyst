---
name: ci-cd-setup
description: Configure CI/CD pipelines with GitHub Actions, GitLab CI, automated testing and deployment.
---

## GitHub Actions Template
```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - run: npm run build
```

## Pipeline Stages
1. **Lint** — Code style check
2. **Test** — Unit + integration tests
3. **Build** — Compile/package
4. **Deploy** — Deploy to target environment

## Best Practices
- Cache dependencies to speed up builds
- Run independent tests in parallel
- Use env vars for secrets (never hardcode)
- PRs must pass CI before merge
