$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

function ReplaceFromFiles($c, $oldFile, $newFile) {
    $o = [System.IO.File]::ReadAllText($oldFile, [System.Text.Encoding]::UTF8)
    $n = [System.IO.File]::ReadAllText($newFile, [System.Text.Encoding]::UTF8)
    if ($c.Contains($o)) {
        Write-Host "  OK: $oldFile"
        return $c.Replace($o, $n)
    } else {
        Write-Host "  NG: $oldFile"
        return $c
    }
}

$content = ReplaceFromFiles $content "$base\dash_ng1_old.txt" "$base\dash_ng1_new.txt"
$content = ReplaceFromFiles $content "$base\dash_ng2_old.txt" "$base\dash_ng2_new.txt"
$content = ReplaceFromFiles $content "$base\dash_ng3_old.txt" "$base\dash_ng3_new.txt"

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done."
