$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

function ReplaceFile($c, $oldFile, $newFile) {
    $o = [System.IO.File]::ReadAllText($oldFile, [System.Text.Encoding]::UTF8)
    $n = [System.IO.File]::ReadAllText($newFile, [System.Text.Encoding]::UTF8)
    if ($c.Contains($o)) { Write-Host "  OK: $oldFile"; return $c.Replace($o, $n) }
    Write-Host "  NG: $oldFile"; return $c
}
function InsertBefore($c, $anchorFile, $insertFile) {
    $a = [System.IO.File]::ReadAllText($anchorFile, [System.Text.Encoding]::UTF8)
    $i = [System.IO.File]::ReadAllText($insertFile, [System.Text.Encoding]::UTF8)
    if ($c.Contains($a)) { Write-Host "  OK: insert $insertFile"; return $c.Replace($a, $i + $a) }
    Write-Host "  NG: anchor $anchorFile"; return $c
}

# 1. Header GO count: 22->24, 待機 7->9
$content = ReplaceFile $content "$base\dash_go24_old.txt" "$base\dash_go24_new.txt"

# 2. Big stat bs-val: 22->24
$old2 = '<div class="bs-val">22</div>'
$new2 = '<div class="bs-val">24</div>'
if ($content.Contains($old2)) { $content = $content.Replace($old2, $new2); Write-Host "  OK: bs-val" }
else { Write-Host "  NG: bs-val" }

# 3. Add Super League sport card before NFL preseason card
$content = InsertBefore $content "$base\dash_sl_nfl_anchor.txt" "$base\dash_sl_sport_card.txt"

# 4. Add Super League active cards before closing active section
$content = InsertBefore $content "$base\dash_active_anchor.txt" "$base\dash_sl_active_cards.txt"

# 5. Add Super League history rows (before first existing history section)
$histAnchor = "        <!-- == WTA Stuttgart 2026-04-12"
$slHistory = [System.IO.File]::ReadAllText("$base\dash_sl_history.txt", [System.Text.Encoding]::UTF8)
if ($content.Contains($histAnchor)) {
    $content = $content.Replace($histAnchor, $slHistory + "        <!-- == WTA Stuttgart 2026-04-12")
    Write-Host "  OK: SL history rows"
} else { Write-Host "  NG: history anchor" }

# 6. Remove Super League from excluded tab
$content = ReplaceFile $content "$base\dash_sl_excluded_old.txt" "$base\dash_sl_excluded_new.txt"

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "All done."
