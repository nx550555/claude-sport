$ProjectDir = "C:\Users\ohwada\Desktop\claude_sport"
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

Write-Log "=== Auto push start: $nowStr ==="

# dashboard.html のタイムスタンプを更新
$html = [System.IO.File]::ReadAllText("$ProjectDir\dashboard.html", [System.Text.Encoding]::UTF8)
$html = $html -replace '(<span id="last-updated-time">)[^<]*(</span>)', ('${1}' + $nowStr + '${2}')
$html = $html -replace '(<span id="next-update-time">)[^<]*(</span>)', ('${1}' + $nextRun + '${2}')
[System.IO.File]::WriteAllText("$ProjectDir\dashboard.html", $html, [System.Text.Encoding]::UTF8)
Write-Log "Timestamp updated"

# GitHub Pages へ push
git add -A
$changed = git status --porcelain
if ($changed) {
    git commit -m ("Auto push " + $now.ToString("yyyy-MM-dd HH:mm"))
    git push origin main
    Write-Log "Push complete"
} else {
    Write-Log "No changes - skip push"
}

Write-Log "=== Done ==="
