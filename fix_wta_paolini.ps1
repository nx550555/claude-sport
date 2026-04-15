$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\records\wta\2026.json"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# 1. Paolini entry: tier skip -> go, update odds
$old1 = '"celo_sonmez": 1616.0, "celo_paolini": 1916.2, "l1_diff": 300.2, "l1_pass": true,
          "tier": "skip", "rec": null,
          "odds_paolini": 1.23, "odds_sonmez": 3.85,
          "est_win_pct_paolini": 84.9,
          "ev_est_paolini": 4.4,'
$new1 = '"celo_sonmez": 1616.0, "celo_paolini": 1916.2, "l1_diff": 300.2, "l1_pass": true,
          "tier": "go", "rec": "Paolini", "rec_odds": 1.24,
          "odds_paolini": 1.24, "odds_sonmez": 3.80,
          "est_win_pct_paolini": 85.0,
          "ev_est_paolini": 5.4,'
if ($content.Contains($old1)) {
    $content = $content.Replace($old1, $new1)
    Write-Host "  REPLACED: Paolini tier skip->go"
} else {
    Write-Host "  NOT FOUND: Paolini entry"
}

# 2. Paolini actual_odds_at_start: 1.23 -> 1.24
$old2 = '"actual_odds_at_start": { "sonmez": 3.85, "paolini": 1.23 },'
$new2 = '"actual_odds_at_start": { "sonmez": 3.80, "paolini": 1.24 },'
if ($content.Contains($old2)) {
    $content = $content.Replace($old2, $new2)
    Write-Host "  REPLACED: Paolini actual_odds_at_start"
} else {
    Write-Host "  NOT FOUND: Paolini actual_odds_at_start"
}

# 3. Stuttgart tournament status: r1_complete -> r1_partial (2 matches pending on 4/15)
$old3 = '"status": "r1_complete",'
$new3 = '"status": "r1_partial",'
if ($content.Contains($old3)) {
    $content = $content.Replace($old3, $new3)
    Write-Host "  REPLACED: Stuttgart status"
} else {
    Write-Host "  NOT FOUND: Stuttgart status"
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done: wta/2026.json updated"
