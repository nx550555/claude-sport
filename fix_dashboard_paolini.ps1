$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# 1. Header: GO 21->22, 待機 6->7
$old1 = "GO 21件 / 確定 15件 / 待機 6件"
$new1 = "GO 22件 / 確定 15件 / 待機 7件"
if ($content.Contains($old1)) { $content = $content.Replace($old1, $new1); Write-Host "  OK: header stats" }
else { Write-Host "  NG: header stats" }

# 2. Big stat Total GO 21->22
$old2 = '<div class="bs-val">21</div>'
$new2 = '<div class="bs-val">22</div>'
if ($content.Contains($old2)) { $content = $content.Replace($old2, $new2); Write-Host "  OK: bs-val GO count" }
else { Write-Host "  NG: bs-val GO count" }

# 3. WTA 次回: R2待 -> Paolini @1.24
$old3 = '<div class="sm-val" style="color:#8b949e;">R2待</div>'
$new3 = '<div class="sm-val" style="color:#e3b341;">Paolini @1.24</div>'
if ($content.Contains($old3)) { $content = $content.Replace($old3, $new3); Write-Host "  OK: WTA next" }
else { Write-Host "  NG: WTA next" }

# 4. Tigers odds 1.46 -> 1.47 (in active card acm-v)
$old4 = '<div class="acm-v odds">1.46</div>'
$new4 = '<div class="acm-v odds">1.47</div>'
if ($content.Contains($old4)) { $content = $content.Replace($old4, $new4); Write-Host "  OK: Tigers odds" }
else { Write-Host "  NG: Tigers odds" }

# 5. Warriors odds 1.22 -> 1.25
$old5 = '<div class="acm-v odds">1.22</div>'
$new5 = '<div class="acm-v odds">1.25</div>'
if ($content.Contains($old5)) { $content = $content.Replace($old5, $new5); Write-Host "  OK: Warriors odds" }
else { Write-Host "  NG: Warriors odds" }

# 6. Warriors EV +10.7% -> +13.4%
$old6 = '<div class="acm-v ev">+10.7%</div>'
$new6 = '<div class="acm-v ev">+13.4%</div>'
if ($content.Contains($old6)) { $content = $content.Replace($old6, $new6); Write-Host "  OK: Warriors EV" }
else { Write-Host "  NG: Warriors EV" }

# 7. Last updated date
$old7 = "2026/04/13 手動更新 JST"
$new7 = "2026/04/14 手動更新 JST"
if ($content.Contains($old7)) { $content = $content.Replace($old7, $new7); Write-Host "  OK: last updated" }
else { Write-Host "  NG: last updated" }

# 8. Add Paolini active card (insert before closing active section)
$activeAnchor = [System.IO.File]::ReadAllText("$base\dash_active_anchor.txt", [System.Text.Encoding]::UTF8)
$paoliniCard = [System.IO.File]::ReadAllText("$base\dash_paolini_card.txt", [System.Text.Encoding]::UTF8)
if ($content.Contains($activeAnchor)) {
    $content = $content.Replace($activeAnchor, $paoliniCard + $activeAnchor)
    Write-Host "  OK: Paolini active card inserted"
} else { Write-Host "  NG: active anchor not found" }

# 9. Add Paolini history row (insert before ATP section in history table)
$historyAnchor = [System.IO.File]::ReadAllText("$base\dash_history_anchor.txt", [System.Text.Encoding]::UTF8)
$paoliniRow = [System.IO.File]::ReadAllText("$base\dash_paolini_history.txt", [System.Text.Encoding]::UTF8)
if ($content.Contains($historyAnchor)) {
    $content = $content.Replace($historyAnchor, $paoliniRow + "        " + $historyAnchor)
    Write-Host "  OK: Paolini history row inserted"
} else { Write-Host "  NG: history anchor not found" }

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "All done."
