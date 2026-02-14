---
name: shell-scripting
description: Write shell scripts and command-line operations - PowerShell, Bash, batch processing.
---

## PowerShell Quick Reference
```powershell
$name = "value"
if ($x -eq 1) { } elseif ($x -gt 2) { } else { }
foreach ($item in $list) { }
Get-Content file.txt
Set-Content -Path file.txt -Value "content"
Test-Path "file.txt"
Get-Process | Where-Object { $_.CPU -gt 100 } | Sort-Object CPU -Descending | Select-Object -First 5
```

## Bash Quick Reference
```bash
if [ "$x" -eq 1 ]; then echo "yes"; fi
[[ -f "file.txt" ]] && echo "exists"
for f in *.txt; do echo "$f"; done
${var:-default}  # Default value
${var%.*}        # Remove suffix
find . -name "*.py" -type f
grep -rn "pattern" --include="*.js"
```

## Cross-Platform Notes
- Windows paths: `\`, Linux/Mac: `/`
- Windows: `findstr`, Linux: `grep`
- PowerShell `curl` is alias, real curl: `curl.exe`
