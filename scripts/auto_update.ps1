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
Write-Log ("Now: " + $nowStr + " / Next: " + $nextRun)

$p1 = "Auto execution mode. Current time: " + $nowStr + ". Next scheduled run: " + $nextRun + ". "
$p2 = "Please do the following in order, in Japanese: "
$p3 = "1. Read BACKLOG.md and stats/cumulative.json, identify unconfirmed results (hit:null or status:pending). "
$p4 = "2. Search for each result using WebSearch and update records/ files. "
$p5 = "3. Screen today and tomorrow games (NRL/NHL/NBA/SuperRugby/UFL/Tennis) using rules in core/rules_*.json. "
$p6 = "4. If GO candidate found, add to records/. "
$p7 = "5. Update dashboard.html: set last-updated-time to '" + $nowStr + "', next-update-time to '" + $nextRun + "', update KPI/active/history/analysis-log sections. "
$p8 = "6. Update stats/cumulative.json. "
$p9 = "7. Update BACKLOG.md completed items to [x]."
$prompt = $p1 + $p2 + $p3 + $p4 + $p5 + $p6 + $p7 + $p8 + $p9

Write-Log "Running Claude..."
try {
    & $ClaudeExe -p $prompt
    Write-Log "Claude done"
} catch {
    Write-Log ("ERROR: Claude failed - " + $_)
    exit 1
}

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
