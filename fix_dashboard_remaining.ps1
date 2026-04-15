$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

function ReplaceFromFiles($c, $oldFile, $newFile) {
    $o = [System.IO.File]::ReadAllText($oldFile, [System.Text.Encoding]::UTF8)
    $n = [System.IO.File]::ReadAllText($newFile, [System.Text.Encoding]::UTF8)
    if ($c.Contains($o)) {
        Write-Host "  REPLACED: $oldFile"
        return $c.Replace($o, $n)
    } else {
        Write-Host "  NOT FOUND: $oldFile"
        return $c
    }
}

# 1. GAMBLE_BET (line ~2199)
$content = ReplaceFromFiles $content "$base\gb1_old.txt" "$base\gb1_new.txt"

# 2. GAMBLE_BET (line ~2349)
$content = ReplaceFromFiles $content "$base\gb2_old.txt" "$base\gb2_new.txt"

# 3. Stuttgart UPSET line 914
$content = ReplaceFromFiles $content "$base\upset1_old.txt" "$base\upset1_new.txt"

# 4. Stuttgart UPSET line 1090
$content = ReplaceFromFiles $content "$base\upset2_old.txt" "$base\upset2_new.txt"

# 5. Stuttgart UPSET line 1815
$content = ReplaceFromFiles $content "$base\upset3_old.txt" "$base\upset3_new.txt"

# 6. R001 proposal panel -> implemented
$content = ReplaceFromFiles $content "$base\r001_old.txt" "$base\r001_new.txt"

# 7. Rules history insertion (before first rule-entry)
$anchor = [System.IO.File]::ReadAllText("$base\rules_anchor.txt", [System.Text.Encoding]::UTF8)
$insert = [System.IO.File]::ReadAllText("$base\rules_insert.txt", [System.Text.Encoding]::UTF8)
if ($content.Contains($anchor)) {
    $content = $content.Replace($anchor, $insert + $anchor)
    Write-Host "  INSERTED: rules_insert.txt"
} else {
    Write-Host "  NOT FOUND: rules_anchor.txt"
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "All done."
