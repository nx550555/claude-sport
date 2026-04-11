$ProjectDir = "C:\Users\ohwada\Desktop\claude_sport"
$ClaudeExe  = "C:\Users\ohwada\.local\bin\claude.exe"
$LogFile    = "$ProjectDir\scripts\auto_update.log"
Set-Location $ProjectDir

$now     = Get-Date
$nowStr  = $now.ToString("yyyy/MM/dd HH:mm") + " JST"
$nextRun = $now.AddHours(12).ToString("yyyy/MM/dd HH:mm") + " JST"
$dateStr = $now.ToString("yyyy-MM-dd")
$reportFile = "$ProjectDir\daily_reports\$dateStr.md"

function Write-Log($msg) {
    $line = "[" + $now.ToString("yyyy-MM-dd HH:mm:ss") + "] " + $msg
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

Write-Log "=== Auto update start: $nowStr ==="

# Prompt: English only to avoid encoding issues
# Claude will respond and write files in Japanese
$p = "AUTOMATED ANALYSIS MODE. " +
     "Current time: $nowStr. Next run: $nextRun. " +
     "Project: C:\Users\ohwada\Desktop\claude_sport " +
     "Execute these steps in order. After EACH step write one line: [STEP N DONE: brief result]. " +
     "STEP1: Read BACKLOG.md and records/ files. List all games where hit=null or status=pending. " +
     "STEP2: For each pending game, search WebSearch for the result. Max 8 searches. " +
     "STEP3: Update the records/ JSON files and stats/cumulative.json with confirmed results. " +
     "STEP4: For any new miss (hit=false), check upset_patterns.json and add entry if needed. Check if any rule in core/rules_*.json needs updating. " +
     "STEP5: Search for games in next 24 hours for active sports (NRL, NHL, NBA, SuperRugby, UFL). Max 5 searches. " +
     "STEP6: Apply L1 screening rules from core/rules_*.json. If GO candidate exists (confidence>=75 and EV>5%), add to records/. " +
     "STEP7: Update dashboard.html - set last-updated-time to '$nowStr', next-update-time to '$nextRun', update all KPI numbers, active recommendations, and history. " +
     "STEP8: Update BACKLOG.md - mark completed items [x], add new pending items [ ]. " +
     "STEP9: Write a Japanese daily report to file $reportFile with sections: results confirmed today, new GO candidates, misses and analysis, rule changes, summary. " +
     "After all steps: output one line: AUTO_COMPLETE"

Write-Log "Starting Claude analysis (budget: USD2.00, auto-permissions)..."
Write-Host "--- Claude output below ---"

$output = & $ClaudeExe -p "--permission-mode" "bypassPermissions" "--max-budget-usd" "2.00" $p 2>&1

Write-Host "--- Claude output end ---"
Write-Log ("Claude finished. Lines: " + ($output | Measure-Object -Line).Lines)

# Check if completed
$completed = $output | Where-Object { $_ -match "AUTO_COMPLETE" }
if ($completed) {
    Write-Log "Analysis completed successfully"
} else {
    Write-Log "WARNING: AUTO_COMPLETE not found - may have been budget-limited or incomplete"
}

# Save full output as fallback report if daily report wasn't created
if (-not (Test-Path $reportFile)) {
    Write-Log "Daily report not found - saving raw output as report"
    $header = "# Auto Report $nowStr (raw output)`n`n"
    $header + ($output -join "`n") | Out-File -FilePath $reportFile -Encoding UTF8
}

# Timestamp update (fallback in case Claude missed it)
$html = [System.IO.File]::ReadAllText("$ProjectDir\dashboard.html", [System.Text.Encoding]::UTF8)
$html = $html -replace '(<span id="last-updated-time">)[^<]*(</span>)', ('${1}' + $nowStr + '${2}')
$html = $html -replace '(<span id="next-update-time">)[^<]*(</span>)', ('${1}' + $nextRun + '${2}')
[System.IO.File]::WriteAllText("$ProjectDir\dashboard.html", $html, [System.Text.Encoding]::UTF8)
Write-Log "Timestamp updated (fallback)"

# Push to GitHub Pages
Write-Log "Pushing to GitHub Pages..."
git add -A
$changed = git status --porcelain
if ($changed) {
    git commit -m ("Auto update " + $now.ToString("yyyy-MM-dd HH:mm"))
    git push origin main
    Write-Log "Push complete"
} else {
    Write-Log "No changes to push"
}

Write-Log "=== Auto update complete ==="
