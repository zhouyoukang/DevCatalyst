# DevCatalyst v5.0 - Installation Verification Script
# Usage: powershell -ExecutionPolicy Bypass -File verify-installation.ps1
# Checks Layer 1 (global) + Layer 2 (project) configuration completeness

param(
    [string]$ProjectPath = "."
)

$ErrorActionPreference = "Continue"
$passed = 0
$failed = 0
$warnings = 0

function Test-Item {
    param([string]$Path, [string]$Description, [bool]$Required = $true)
    if (Test-Path $Path) {
        Write-Host "  [OK] $Description" -ForegroundColor Green
        $script:passed++
        return $true
    }
    else {
        if ($Required) {
            Write-Host "  [FAIL] $Description - NOT FOUND: $Path" -ForegroundColor Red
            $script:failed++
        }
        else {
            Write-Host "  [WARN] $Description - not found (optional)" -ForegroundColor Yellow
            $script:warnings++
        }
        return $false
    }
}

function Test-Content {
    param([string]$Path, [string]$Pattern, [string]$Description)
    if (Test-Path $Path) {
        $content = Get-Content $Path -Raw -ErrorAction SilentlyContinue
        if ($content -match [regex]::Escape($Pattern)) {
            Write-Host "  [OK] $Description" -ForegroundColor Green
            $script:passed++
        }
        else {
            Write-Host "  [FAIL] $Description - pattern not found in $Path" -ForegroundColor Red
            $script:failed++
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " DevCatalyst v5.0 Installation Verify" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# === Layer 1: Global ===
Write-Host "--- Layer 1: Global Configuration ---" -ForegroundColor Cyan

$globalSkillsPath = Join-Path $env:USERPROFILE ".codeium\windsurf\skills"
$globalHooksPath = Join-Path $env:USERPROFILE ".codeium\windsurf\hooks.json"
$globalRulesPath = Join-Path $env:USERPROFILE ".codeium\windsurf\memories\global_rules.md"

if (Test-Path $globalSkillsPath) {
    $skillCount = (Get-ChildItem $globalSkillsPath -Directory).Count
    if ($skillCount -ge 20) {
        Write-Host "  [OK] Global Skills: $skillCount found" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  [WARN] Global Skills: only $skillCount found (expected 23)" -ForegroundColor Yellow
        $warnings++
    }
} else {
    Write-Host "  [FAIL] Global Skills directory not found" -ForegroundColor Red
    $failed++
}

if (Test-Path $globalHooksPath) {
    $hooksContent = Get-Content $globalHooksPath -Raw -ErrorAction SilentlyContinue
    if ($hooksContent -match "powershell\.exe|pwsh") {
        Write-Host "  [FAIL] Global hooks.json contains PowerShell hooks (forbidden)!" -ForegroundColor Red
        $failed++
    } else {
        Write-Host "  [OK] Global hooks.json is safe" -ForegroundColor Green
        $passed++
    }
} else {
    Write-Host "  [OK] Global hooks.json not present (safe)" -ForegroundColor Green
    $passed++
}

Test-Item $globalRulesPath "Global rules (global_rules.md)"

$settingsPath = Join-Path $env:APPDATA "Windsurf\User\settings.json"
if (Test-Path $settingsPath) {
    Test-Content $settingsPath "Windows PowerShell" "Terminal profile set to Windows PowerShell"
    Test-Content $settingsPath "shellIntegration" "Shell integration configured"
} else {
    Write-Host "  [WARN] Windsurf settings.json not found" -ForegroundColor Yellow
    $warnings++
}

# === Layer 2: Project ===
Write-Host "`n--- Layer 2: Project Configuration ---" -ForegroundColor Cyan

$rulesPath = Join-Path $ProjectPath ".windsurf\rules"
$workflowsPath = Join-Path $ProjectPath ".windsurf\workflows"

Test-Item (Join-Path $rulesPath "soul.md") "Rule: soul.md"
Test-Item (Join-Path $rulesPath "execution-engine.md") "Rule: execution-engine.md"
Test-Item (Join-Path $rulesPath "project-structure.md") "Rule: project-structure.md"
Test-Item (Join-Path $workflowsPath "debug-escalation.md") "Workflow: debug-escalation"
Test-Item (Join-Path $ProjectPath "AGENTS.md") "Root AGENTS.md"

# === Summary ===
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " Results: $passed passed, $failed failed, $warnings warnings" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
Write-Host "========================================`n" -ForegroundColor Cyan

if ($failed -eq 0) { Write-Host " All checks passed!" -ForegroundColor Green }
else { Write-Host " $failed issues found. Run /health-check in Cascade to auto-fix." -ForegroundColor Red }

exit $failed
