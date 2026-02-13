---
name: api-design
description: Design RESTful API interfaces. Triggered when creating HTTP endpoints, designing API structure, or standardizing API style.
---

## RESTful Design Principles

### URL Naming
```
GET    /users          → List
GET    /users/:id      → Detail
POST   /users          → Create
PUT    /users/:id      → Full update
PATCH  /users/:id      → Partial update
DELETE /users/:id      → Delete
```

### Nested Resources
```
GET    /users/:id/orders        → User's order list
POST   /users/:id/orders        → Create order for user
```

### Query Parameters
```
GET /users?page=1&limit=20&sort=name&order=asc&status=active
```

## Response Format
```json
{
  "code": 200,
  "message": "success",
  "data": { },
  "meta": { "total": 100, "page": 1, "limit": 20 }
}
```

## Error Response
```json
{
  "code": 400,
  "message": "Validation failed",
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
```

## HTTP Status Codes
- 200 OK / 201 Created / 204 No Content
- 400 Bad Request / 401 Unauthorized / 403 Forbidden / 404 Not Found
- 500 Internal Server Error
