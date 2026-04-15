# Add UFL Week 4 Louisville Kings game to records/ufl/2026.json
$uflPath = "C:\Users\ohwada\Desktop\claude_sport\records\ufl\2026.json"
$ufl = Get-Content $uflPath -Raw -Encoding UTF8 | ConvertFrom-Json

# Check if Louisville already exists
$existing = $ufl.games | Where-Object { $_.match -like "*Louisville*" }
if ($existing) {
    Write-Host "Louisville already exists, skipping"
    exit
}

$newGame = [PSCustomObject]@{
    week        = 4
    date        = "2026-04-17"
    start_time  = "TBD"
    match       = "Houston Gamblers vs Louisville Kings"
    venue       = "TBD"
    tier        = "go"
    rec         = "Louisville Kings"
    rec_odds    = 1.65
    ev_est      = 35.3
    confidence  = 82
    ev_calc     = "(0.82 x 1.65) - 1 = +35.3%"
    adjustments = [PSCustomObject]@{
        qb_edge         = "Bean (Louisville) W3 352yd 3TD vs Tagovailoa W3 21/40 171yd (7-45 blowout loss)"
        houston_qb_note = "Dekkers shoulder W1 injury -> Tagovailoa started W3, poor performance"
        threshold       = "Week4 GO threshold: conf >= 80%"
    }
    status      = "pending"
    result      = $null
    score       = $null
    hit         = $null
    actual_ev   = $null
    rules_applied = @("GEN001", "UFL_v1.0")
    note        = "Houston QB situation unstable (Dekkers W1 shoulder injury, Tagovailoa fill-in W3 171yd 7-45 loss). Louisville QB Bean excellent W3 (352yd 3TD). Home/away TBD. GO per all-source check 2026-04-15. conf 82% > W4 threshold 80%."
}

$newList = [System.Collections.ArrayList]$ufl.games
$newList.Add($newGame) | Out-Null
$ufl.games = $newList.ToArray()

# Update summary
$ufl.summary.total_go = ($ufl.summary.total_go + 1)
$ufl.summary.pending = ($ufl.summary.pending + 1)

$ufl | ConvertTo-Json -Depth 10 | Set-Content $uflPath -Encoding UTF8
Write-Host "UFL 2026.json: Louisville Kings W4 added."
