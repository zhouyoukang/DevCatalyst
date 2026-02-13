#!/usr/bin/env python3
"""
Cascade Hook: Block AI from reading/modifying sensitive files
Uses pre-hook exit code 2 to block the action

Usage in .windsurf/hooks.json:
{
  "hooks": {
    "pre_read_code": [{"command": "python3 .windsurf/hooks/block_sensitive_files.py", "show_output": true}],
    "pre_write_code": [{"command": "python3 .windsurf/hooks/block_sensitive_files.py", "show_output": true}]
  }
}
"""

import sys
import json

BLOCKED_PATTERNS = [
    ".env",
    "secrets",
    "credentials",
    "private_key",
    ".pem",
    ".key",
]

def main():
    try:
        data = json.loads(sys.stdin.read())
        tool_info = data.get("tool_info", {})
        file_path = tool_info.get("file_path", "").lower()
        
        for pattern in BLOCKED_PATTERNS:
            if pattern in file_path:
                print(f"\ud83d\udd12 Blocked: AI cannot access files matching '{pattern}'", file=sys.stderr)
                sys.exit(2)  # Exit code 2 = block the action
        
    except json.JSONDecodeError:
        pass  # Allow action if can't parse input

if __name__ == "__main__":
    main()
