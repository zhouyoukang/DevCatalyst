---
name: regex-helper
description: Write and debug regular expressions - text matching, replacement, extraction, input validation.
---

## Common Patterns
| Pattern | Regex | Description |
|---------|-------|------------|
| Email | `[\w.+-]+@[\w-]+\.[\w.]+` | Basic email validation |
| URL | `https?://[^\s<>"]+` | HTTP/HTTPS links |
| IP | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` | IPv4 |
| Date | `\d{4}-\d{2}-\d{2}` | YYYY-MM-DD |
| Phone (CN) | `1[3-9]\d{9}` | Chinese mobile number |
| Chinese | `[\u4e00-\u9fff]+` | Chinese characters |

## Advanced Techniques
- **Non-greedy**: `.*?` instead of `.*`
- **Named capture**: `(?<name>...)` or `(?P<name>...)`
- **Lookahead**: `(?=...)` positive, `(?!...)` negative
- **Lookbehind**: `(?<=...)` positive, `(?<!...)` negative

## Debugging Method
1. Start with simple pattern, add complexity incrementally
2. Test each step with concrete test strings
3. Watch for escape character differences across languages
