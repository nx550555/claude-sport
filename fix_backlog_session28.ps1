$file = "C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md"
$content = Get-Content -Raw -Encoding UTF8 $file

# Mark ATP GO3 as complete
$old = '- [ ] ATP GO3'
$new = '- [x] ATP GO3'
if ($content.Contains($old)) {
    $content = $content.Replace($old, $new)
    Write-Host "ATP GO3 marked done"
}

# Find and update the ATP Munich line
$anchor1 = '- [ ] ATP Munich GO3'
if ($content.Contains($anchor1)) {
    $content = $content.Replace($anchor1, '- [x] ATP Munich/Barcelona GO3')
    Write-Host "ATP Munich GO3 line updated"
}

# Find the Cobolli/Kopriva/Musetti result lines
$old2 = '- [ ] ATP GO3件（Musetti/Cobolli/Kopriva）結果確認 ← 4/14試合進行中（本日夜〜深夜に結果出る）'
if ($content.Contains($old2)) {
    $new2 = '- [x] ATP GO3件（Musetti/Cobolli/Kopriva）結果確認 ← 全HIT: Musetti 7-5 6-2 / Cobolli 6-4 7-5 / Kopriva 6-3 5-7 6-2'
    $content = $content.Replace($old2, $new2)
    Write-Host "ATP Munich line 2 updated"
}

$content | Set-Content -Path $file -Encoding UTF8 -NoNewline
Write-Host "BACKLOG updated"
