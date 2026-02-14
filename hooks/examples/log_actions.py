#!/usr/bin/env python3
"""
Cascade Hook: Log all AI actions to a file
Safe: Python hooks do not interfere with terminal prompt detection

Usage in .windsurf/hooks.json:
{
  "hooks": {
    "post_write_code": [{"command": "python3 .windsurf/hooks/log_actions.py", "show_output": false}],
    "post_run_command": [{"command": "python3 .windsurf/hooks/log_actions.py", "show_output": false}]
  }
}
"""

import sys
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "cascade_actions.log"

def main():
    try:
        data = json.loads(sys.stdin.read())
        action = data.get("agent_action_name", "unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        tool_info = data.get("tool_info", {})
        summary = ""
        
        if "file_path" in tool_info:
            summary = f"file={tool_info['file_path']}"
        elif "command" in tool_info:
            cmd = tool_info["command"][:80]
            summary = f"cmd={cmd}"
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {action}: {summary}\n")
            
    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
