# NRL R7 + Super League R8 record updates (2026-04-15 session)
# NRL: Broncos revoked, Panthers/Rabbitohs -> skip
# SL: Warrington confidence 85->80, EV 40.3->32.0 (Tanginoa+Yates both out)

$nrlPath = "C:\Users\ohwada\Desktop\claude_sport\records\nrl\2026.json"
$slPath  = "C:\Users\ohwada\Desktop\claude_sport\records\superleague\2026.json"

# ---- NRL updates ----
$nrl = Get-Content $nrlPath -Raw -Encoding UTF8 | ConvertFrom-Json

# Broncos -> revoked
$broncos = $nrl.pending_games | Where-Object { $_.match -like "*Broncos*" }
if ($broncos) {
    $broncos.status = "revoked"
    $broncos.tier   = "revoked"
    $broncos | Add-Member -NotePropertyName "revoke_date"   -NotePropertyValue "2026-04-15" -Force
    $broncos | Add-Member -NotePropertyName "revoke_reason" -NotePropertyValue "R7_analysis_2026-04-15: (1) Luai returns from suspension - Tigers key playmaker back. (2) Carrigan suspended - Broncos lose captain/key prop. (3) Market confirms: Tigers 1.52 / Broncos 2.55, statsinsider Tigers 69% favorite. GEN002_ALERT confirmed as real squad-change gap, not data error. GO revoked." -Force
    Write-Host "Broncos: revoked"
}

# Panthers -> skip
$panthers = $nrl.pending_games | Where-Object { $_.match -like "*Panthers*" }
if ($panthers) {
    $panthers.status = "skip"
    $panthers | Add-Member -NotePropertyName "skip_reason" -NotePropertyValue "odds_too_short_final: 1.14 EV+9.2% insufficient return. Originally CAUTION, formally SKIP after 2026-04-15 review." -Force
    Write-Host "Panthers: skip"
}

# Rabbitohs vs Dragons -> skip
$rabbitohs = $nrl.pending_games | Where-Object { $_.match -like "*Rabbitohs*Dragons*" }
if ($rabbitohs) {
    $rabbitohs.status = "skip"
    $rabbitohs | Add-Member -NotePropertyName "skip_reason" -NotePropertyValue "odds_short_final: 1.18 EV+6.8% at threshold limit, no margin for error. Originally CAUTION, formally SKIP after 2026-04-15 review." -Force
    Write-Host "Rabbitohs vs Dragons: skip"
}

$nrl | ConvertTo-Json -Depth 10 | Set-Content $nrlPath -Encoding UTF8
Write-Host "NRL 2026.json updated."

# ---- Super League SL-002 Warrington update ----
$sl = Get-Content $slPath -Raw -Encoding UTF8 | ConvertFrom-Json

$warrington = $sl.games | Where-Object { $_.id -eq "SL-002" }
if ($warrington) {
    $warrington.confidence = 80
    $warrington.ev         = 32.0
    $warrington | Add-Member -NotePropertyName "ev_calc" -NotePropertyValue "(0.80 x 1.65) - 1 = +32.0% (revised 2026-04-15 after squad news)" -Force
    # Add injury_penalty to adjustments
    $warrington.adjustments | Add-Member -NotePropertyName "injury_penalty" -NotePropertyValue "-5% (Tanginoa OUT + Luke Yates OUT, two key back-rowers confirmed absent for R8 vs Catalans)" -Force
    $warrington | Add-Member -NotePropertyName "squad_note" -NotePropertyValue "2026-04-15 confirmed: Tanginoa and Luke Yates both injured. Doubts: Niu, Brand, Hughes. Marc Sneyd returns to halves. Still GO but confidence reduced 85->80." -Force
    Write-Host "SL-002 Warrington: confidence 85->80, EV 40.3->32.0"
}

$sl.summary.pending = 2
$sl | ConvertTo-Json -Depth 10 | Set-Content $slPath -Encoding UTF8
Write-Host "superleague 2026.json updated."

Write-Host "All updates complete."
