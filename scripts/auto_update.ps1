$ProjectDir = "C:\Users\ohwada\Desktop\claude_sport"
$ClaudeExe  = "C:\Users\ohwada\.local\bin\claude.exe"
$LogFile    = "$ProjectDir\scripts\auto_update.log"
$DashFile   = "$ProjectDir\dashboard.html"
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

# ---------------------------------------------------------------
# Prompt: English only to avoid encoding issues
# STEP2 now enforces trusted-source-only result verification
# ---------------------------------------------------------------
$p = "AUTOMATED ANALYSIS MODE. " +
     "Current time: $nowStr. Next run: $nextRun. " +
     "Project: C:\Users\ohwada\Desktop\claude_sport " +
     "Execute these steps in order. After EACH step write one line: [STEP N DONE: brief result]. " +

     "STEP1: Read BACKLOG.md and records/ files. Also read core/trusted_sources.json. " +
     "List all games where hit=null or status=pending. " +

     "STEP2-A [RESULT VERIFICATION - STRICT]: " +
     "For each pending game, determine the sport type and look up the primary_url from core/trusted_sources.json. " +
     "Search WebSearch using ONLY that primary URL as the source (use allowed_domains or site: query). " +
     "Example: for NHL use 'site:nhl.com {team1} {team2} result', for ATP use 'site:atptour.com {player1} {player2} result'. " +
     "If the primary_url returns no confirmed result, try fallback_url once. " +
     "If NEITHER source confirms the result, set hit=null and status=pending. DO NOT guess, infer, or use blog/news sites for win/loss. " +
     "Max 6 searches for result verification. " +

     "STEP2-B [CONTEXT GATHERING]: " +
     "For confirmed results (and separately for new GO candidates), search context_sources from trusted_sources.json. " +
     "Gather: injury updates, lineup changes, notable plays. Max 4 searches. " +

     "STEP3: Update the records/ JSON files and stats/cumulative.json with confirmed results only. " +
     "For any result still unconfirmed after STEP2-A, leave hit=null. " +

     "STEP4: For any new miss (hit=false), check upset_patterns.json and add entry if needed. " +
     "Check if any rule in core/rules_*.json needs updating. " +

     "STEP5: Search for games in next 24 hours for active sports. " +
     "Use only official league sites or sports-reference sites. Max 5 searches. " +

     "STEP6: Apply L1 screening rules from core/rules_*.json. " +
     "If GO candidate exists (confidence>=75 and EV>5%), add to records/. " +

     "STEP7: Update dashboard.html (at project root, NOT dashboard/index.html). " +
     "Set <span id='last-updated-time'> to '$nowStr' and <span id='next-update-time'> to '$nextRun'. " +
     "Update all KPI numbers (hit rate, EV, GO count, pending count), active recommendation cards, and history table. " +
     "Update the notice div with today's most important pending predictions and results. " +

     "STEP8: Update BACKLOG.md - mark completed items [x], add new pending items [ ]. " +

     "STEP9: Write a Japanese daily report to $reportFile with sections: " +
     "results confirmed today (with source URL noted), new GO candidates, misses and analysis, rule changes, summary stats. " +

     "After all steps: output one line: AUTO_COMPLETE"

Write-Log "Starting Claude analysis (budget: USD2.00, auto-permissions)..."
Write-Host "--- Claude output below ---"

$output = & $ClaudeExe -p "--permission-mode" "bypassPermissions" "--model" "claude-haiku-4-5-20251001" "--max-budget-usd" "2.00" $p 2>&1

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

# Timestamp update fallback (in case Claude missed the span tags)
if (Test-Path $DashFile) {
    $html = [System.IO.File]::ReadAllText($DashFile, [System.Text.Encoding]::UTF8)
    $html = $html -replace '(<span id="last-updated-time">)[^<]*(</span>)', ('${1}' + $nowStr + '${2}')
    $html = $html -replace '(<span id="next-update-time">)[^<]*(</span>)', ('${1}' + $nextRun + '${2}')
    [System.IO.File]::WriteAllText($DashFile, $html, [System.Text.Encoding]::UTF8)
    Write-Log "Timestamp updated in dashboard/index.html"
} else {
    Write-Log "ERROR: dashboard/index.html not found at $DashFile"
}

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
