"""Safe file writer v2 - bypasses IDE edit tool's RPC channel.

Usage:
  # Single replace (v1 compatible)
  python _safe_write.py replace <file> <old_file> <new_file>
  python _safe_write.py overwrite <file> <content_file>
  python _safe_write.py append <file> <content_file>

  # Batch mode: JSON instruction file (v2 - saves tool calls)
  python _safe_write.py batch <instruction.json>

  instruction.json format:
  {
    "file": "path/to/target.md",
    "edits": [
      {"old": "text to find", "new": "replacement text"},
      {"old": "another find", "new": "another replace"}
    ]
  }
"""
import sys
import json


def do_replace(target, old_str, new_str):
    content = open(target, "r", encoding="utf-8").read()
    if old_str not in content:
        return False, f"old_string not found in {target}"
    content = content.replace(old_str, new_str, 1)
    open(target, "w", encoding="utf-8").write(content)
    return True, "replaced"


def main():
    if len(sys.argv) < 3:
        print("Usage: python _safe_write.py <mode> <args...>")
        print("Modes: replace, overwrite, append, batch")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "batch":
        instr = json.loads(open(sys.argv[2], "r", encoding="utf-8").read())
        target = instr["file"]
        content = open(target, "r", encoding="utf-8").read()
        applied = 0
        for i, edit in enumerate(instr["edits"]):
            if edit["old"] not in content:
                print(f"WARN: edit #{i} old_string not found, skipped")
                continue
            content = content.replace(edit["old"], edit["new"], 1)
            applied += 1
        open(target, "w", encoding="utf-8").write(content)
        print(f"OK: {applied}/{len(instr['edits'])} edits applied to {target}")

    elif mode == "replace":
        old_str = open(sys.argv[3], "r", encoding="utf-8").read()
        new_str = open(sys.argv[4], "r", encoding="utf-8").read()
        ok, msg = do_replace(sys.argv[2], old_str, new_str)
        print(f"{'OK' if ok else 'ERROR'}: {msg}")
        if not ok:
            sys.exit(1)

    elif mode == "overwrite":
        new_content = open(sys.argv[3], "r", encoding="utf-8").read()
        open(sys.argv[2], "w", encoding="utf-8").write(new_content)
        print(f"OK: overwritten {sys.argv[2]}")

    elif mode == "append":
        new_content = open(sys.argv[3], "r", encoding="utf-8").read()
        with open(sys.argv[2], "a", encoding="utf-8") as f:
            f.write(new_content)
        print(f"OK: appended to {sys.argv[2]}")

    else:
        print(f"ERROR: unknown mode '{mode}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
