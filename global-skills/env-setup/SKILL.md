---
name: env-setup
description: Development environment setup - install toolchains, configure env vars, manage runtime versions.
---

## Environment Checklist
1. Language runtime version correct
2. Package manager installed
3. Environment variables configured
4. IDE plugins/extensions installed
5. Database/middleware available

## Version Managers
- **Node.js**: nvm / fnm
- **Python**: pyenv / conda
- **Java**: sdkman / jabba
- **Go**: goenv

## Environment Variables Best Practices
- Dev: `.env` file (add to .gitignore)
- Prod: system env vars or secret management service
- Different envs: `.env.development` / `.env.production`
- Use `dotenv` libraries to auto-load

## Common Issues
- **PATH not finding command**: Check PATH, restart terminal
- **Permission denied**: chmod (Linux/Mac), admin rights (Windows)
- **Port in use**: `netstat -ano | findstr :<port>`
