$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# アクティブカード修正
$old = [System.IO.File]::ReadAllText("$base\dash_broncos_old.txt", [System.Text.Encoding]::UTF8)
$new = [System.IO.File]::ReadAllText("$base\dash_broncos_new.txt", [System.Text.Encoding]::UTF8)
if ($content.Contains($old)) {
    $content = $content.Replace($old, $new)
    Write-Host "  OK: active card Broncos odds updated"
} else {
    Write-Host "  NG: active card anchor not found"
}

# 履歴テーブルの odds 1.46 → 2.50 (Broncos行)
$old2 = '<td style="color:#e3b341;">1.46</td>'
$new2 = '<td style="color:#e3b341;">2.50</td>'
if ($content.Contains($old2)) {
    $content = $content.Replace($old2, $new2)
    Write-Host "  OK: history table odds 1.46->2.50"
} else {
    Write-Host "  NG: history odds not found"
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done."
