---
name: api-testing
description: Test HTTP API endpoints. Triggered when verifying API functionality, health checks, or debugging HTTP services.
---

## Testing Tools

### curl Quick Test
```bash
# GET
curl -s http://localhost:3000/api/users | jq

# POST (JSON)
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"test","email":"test@example.com"}'

# With auth
curl -H "Authorization: Bearer <token>" http://localhost:3000/api/me
```

### Batch Test Template
```bash
BASE="http://localhost:3000/api"
echo "=== Health ===" && curl -s "$BASE/health"
echo "=== List ===" && curl -s "$BASE/users" | head -c 200
```

## Checklist
- Status codes correct (200/201/400/404/500)
- Response format matches spec
- Error cases return meaningful messages
- Edge cases: empty body, oversized payload, invalid JSON

## Windows Note
- Use `curl.exe` (not PowerShell alias)
- Double quotes in JSON need escaping `\"`
