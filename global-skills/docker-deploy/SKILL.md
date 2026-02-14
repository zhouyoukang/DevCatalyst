---
name: docker-deploy
description: Docker containerized deployment - Dockerfile, docker-compose, container debugging.
---

## Dockerfile Best Practices
```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## docker-compose Template
```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    environment: ["NODE_ENV=production"]
    depends_on: [db]
  db:
    image: postgres:16-alpine
    volumes: [db-data:/var/lib/postgresql/data]
volumes:
  db-data:
```

## Debug Commands
```bash
docker logs <container>
docker exec -it <container> sh
docker compose logs -f
```
