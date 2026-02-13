---
name: database-design
description: Design database schemas, write SQL, optimize queries.
---

## Design Principles
- Table names plural (users, orders)
- Primary key: id (auto-increment or UUID)
- Foreign key naming: `<singular_table>_id`
- Timestamps: `created_at`, `updated_at`
- Soft delete: `deleted_at`

## Common SQL Patterns
```sql
-- Pagination
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;

-- Join with aggregation
SELECT u.name, COUNT(o.id) as order_count
FROM users u LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id HAVING order_count > 5;

-- Existence check (faster than COUNT)
SELECT EXISTS(SELECT 1 FROM users WHERE email = ?);
```

## Index Optimization
- Add indexes on frequently WHERE/JOIN/ORDER BY columns
- Composite indexes follow leftmost prefix rule
- Don't index low-cardinality columns alone
- Use EXPLAIN to analyze query plans

## ORM Notes
- N+1 query problem: use JOIN or eager loading
- Avoid queries inside loops
- Large datasets: use cursor/stream, not full load
