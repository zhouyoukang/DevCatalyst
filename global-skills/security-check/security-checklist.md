# Security Checklist (Copy and Use Directly)

## Before Code Commit

### Input Validation
- [ ] All user input validated and escaped
- [ ] SQL uses parameterized queries (no string concatenation)
- [ ] HTML output escaped (prevent XSS)
- [ ] File uploads restrict type, size, and path

### Authentication & Authorization
- [ ] Passwords hashed with bcrypt/scrypt/Argon2
- [ ] JWT/Session has reasonable expiration
- [ ] API endpoints have permission checks
- [ ] CORS allows only necessary domains
- [ ] Sensitive operations have CSRF protection

### Sensitive Data
- [ ] API keys/passwords not hardcoded
- [ ] .env / secrets in .gitignore
- [ ] Logs don't contain passwords/tokens/personal data
- [ ] HTTPS for all external communication
- [ ] Database connection strings not exposed in frontend

### Dependency Security
- [ ] Ran `npm audit` / `pip audit` / `./gradlew dependencyCheckAnalyze`
- [ ] No known high-severity CVEs
- [ ] Dependency versions locked (lockfile committed)

### Error Handling
- [ ] Error messages don't leak implementation details
- [ ] 500 errors return generic message (no stack trace)
- [ ] Exceptions are caught and logged (not silently swallowed)

## Before Deployment

### Configuration
- [ ] Debug mode disabled
- [ ] Default passwords changed
- [ ] Unnecessary ports/services closed
- [ ] HTTP security headers configured (CSP, HSTS, X-Frame-Options)

### Monitoring
- [ ] Logging includes sufficient audit info
- [ ] Alert on anomalies configured
- [ ] Backup strategy implemented
