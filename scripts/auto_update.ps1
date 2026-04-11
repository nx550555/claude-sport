$ErrorActionPreference = "Stop"
$ProjectDir = "C:\Users\ohwada\Desktop\claude_sport"
$ClaudeExe  = "C:\Users\ohwada\.local\bin\claude.exe"
$LogFile    = "$ProjectDir\scripts\auto_update.log"

Set-Location $ProjectDir

$now     = Get-Date
$nowStr  = $now.ToString("yyyy/MM/dd HH:mm") + " JST"
$nextRun = $now.AddHours(12).ToString("yyyy/MM/dd HH:mm") + " JST"

function Write-Log($msg) {
    $line = "[" + $now.ToString("yyyy-MM-dd HH:mm:ss") + "] " + $msg
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

Write-Log "=== Auto update start ==="

$prompt = "Read BACKLOG.md and stats/cumulative.json. Check pending results (hit:null) via WebSearch. Update records/ files and dashboard.html (set last-updated-time to '" + $nowStr + "' and next-update-time to '" + $nextRun + "'). Update stats/cumulative.json and BACKLOG.md. Reply only in Japanese. Keep it concise."

Write-Log "Running Claude..."

$job = Start-Process -FilePath $ClaudeExe `
    -ArgumentList "-p", "--permission-mode", "bypassPermissions", "--max-budget-usd", "1.00", $prompt `
    -WorkingDirectory $ProjectDir `
    -NoNewWindow -PassThru

$timeout = 600
if (-not $job.WaitForExit($timeout * 1000)) {
    $job.Kill()
    Write-Log "ERROR: Timeout after $timeout seconds - killed"
    exit 1
}

Write-Log "Claude done (exit code: $($job.ExitCode))"

Write-Log "Pushing to GitHub Pages..."
try {
    git add -A
    $changed = git status --porcelain
    if ($changed) {
        git commit -m ("Auto update " + $now.ToString("yyyy-MM-dd HH:mm"))
        git push origin main
        Write-Log "Push complete"
    } else {
        Write-Log "No changes - skip push"
    }
} catch {
    Write-Log ("ERROR: git push failed - " + $_)
    exit 1
}

Write-Log "=== Auto update complete ==="
