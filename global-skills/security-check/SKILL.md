---
name: security-check
description: Check code for security vulnerabilities and risks - security audits, sensitive data handling, pre-deployment checks.
---

## Checklist

### Input Validation
- [ ] All user input validated and escaped
- [ ] SQL uses parameterized queries (no string concatenation)
- [ ] HTML output escaped (prevent XSS)
- [ ] File uploads restrict type and size

### Authentication & Authorization
- [ ] Passwords hashed with bcrypt/scrypt (not MD5/SHA)
- [ ] JWT has reasonable expiration
- [ ] API endpoints have permission checks
- [ ] CORS configured for necessary domains only

### Sensitive Data
- [ ] API keys not hardcoded in code
- [ ] .env files in .gitignore
- [ ] Logs don't contain passwords/tokens
- [ ] HTTPS for all external communication

### Dependency Security
- [ ] Dependencies regularly updated
- [ ] Known vulnerabilities checked (npm audit / pip audit)

## Security Principles
- **Least privilege**: Only grant necessary permissions
- **Defense in depth**: Multiple security layers
- **Secure by default**: Default configs should be secure
