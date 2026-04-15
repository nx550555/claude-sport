$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

$anchor = [System.IO.File]::ReadAllText("$base\dash_rules_insert_anchor.txt", [System.Text.Encoding]::UTF8)
$insert = [System.IO.File]::ReadAllText("$base\dash_gen001_rule_new.txt", [System.Text.Encoding]::UTF8)

if ($content.Contains($anchor)) {
    $content = $content.Replace($anchor, $insert + $anchor)
    Write-Host "  OK: GEN001/GEN002 rule inserted"
} else {
    Write-Host "  NG: anchor not found"
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done."
