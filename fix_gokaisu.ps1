# fix_gokaisu.ps1 — UFL GO回数を1に戻し、NRL GO回数を3にする
$f = 'C:\Users\ohwada\Desktop\claude_sport\dashboard.html'
$enc = [System.Text.Encoding]::UTF8
$raw = [System.IO.File]::ReadAllBytes($f)
$content = $enc.GetString($raw)
$content = $content.Replace("`r`n", "`n")

$gokaisu = "GO" + [char]0x56DE + [char]0x6570  # GO回数

# UFL カードのheader（color:#fca5a5）に続くGO回数を3→1に戻す
$uflSection = [char]0x2665  # just a placeholder approach
# Better: find UFL header and fix its GO回数
$uflHeader = 'style="color:#fca5a5;">' + [char]0x1F3C8 + ' UFL '
$uflIdx = $content.IndexOf($uflHeader, [System.StringComparison]::Ordinal)
if ($uflIdx -lt 0) {
    # Try without emoji
    $uflHeader = 'style="color:#fca5a5;">'
    $uflIdx = $content.IndexOf($uflHeader, [System.StringComparison]::Ordinal)
}

# Find GO回数 section AFTER UFL header
$goLabel = '<div class="sm-label">' + $gokaisu + '</div><div class="sm-val">3</div></div>'
$goLabelFixed = '<div class="sm-label">' + $gokaisu + '</div><div class="sm-val">1</div></div>'
$goIdx = $content.IndexOf($goLabel, $uflIdx, [System.StringComparison]::Ordinal)

if ($goIdx -lt 0) {
    Write-Warning "UFL GO回数 not found near UFL header"
} else {
    $content = $content.Substring(0, $goIdx) + $goLabelFixed + $content.Substring($goIdx + $goLabel.Length)
    Write-Output "UFL GO count restored to 1"
}

# NRL カードのheader（color:#86efac）に続くGO回数を1→3にする
$nrlHeader = 'style="color:#86efac;">'
$nrlIdx = $content.IndexOf($nrlHeader, [System.StringComparison]::Ordinal)
$nrlGoLabel = '<div class="sm-label">' + $gokaisu + '</div><div class="sm-val">1</div></div>'
$nrlGoFixed = '<div class="sm-label">' + $gokaisu + '</div><div class="sm-val">3</div></div>'
$nrlGoIdx = $content.IndexOf($nrlGoLabel, $nrlIdx, [System.StringComparison]::Ordinal)

if ($nrlGoIdx -lt 0) {
    Write-Warning "NRL GO回数 not found near NRL header"
} else {
    $content = $content.Substring(0, $nrlGoIdx) + $nrlGoFixed + $content.Substring($nrlGoIdx + $nrlGoLabel.Length)
    Write-Output "NRL GO count set to 3"
}

$bytes = $enc.GetBytes($content)
[System.IO.File]::WriteAllBytes($f, $bytes)
Write-Output "Done"
