$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$lines = Get-Content -Path $file -Encoding UTF8

# ===== Active Recommendations Table =====
# Musetti row: lines 641,642,643 (index 640,641,642)
if ($lines[640] -match 'badge-pending') {
    $lines[640] = '          <td><span class="badge badge-hit">&#x2713; HIT</span></td>'
    $lines[641] = '          <td style="color:#3fb950;">Musetti 7-5 6-2</td>'
    $lines[642] = '          <td class="ev-pos">+0.270</td>'
    Write-Host "Musetti row updated"
}

# Cobolli row: lines 655,656,657 (index 654,655,656)
if ($lines[654] -match 'badge-pending') {
    $lines[654] = '          <td><span class="badge badge-hit">&#x2713; HIT</span></td>'
    $lines[655] = '          <td style="color:#3fb950;">Cobolli 6-4 7-5</td>'
    $lines[656] = '          <td class="ev-pos">+0.210</td>'
    Write-Host "Cobolli row updated"
}

# Kopriva row: lines 669,670,671 (index 668,669,670)
if ($lines[668] -match 'badge-pending') {
    $lines[668] = '          <td><span class="badge badge-hit">&#x2713; HIT</span></td>'
    $lines[669] = '          <td style="color:#3fb950;">Kopriva 6-3 5-7 6-2</td>'
    $lines[670] = '          <td class="ev-pos">+0.360</td>'
    Write-Host "Kopriva row updated"
}

# ===== Screening Log: add HIT notes =====
# Musetti screening row line 1279 (index 1278)
if ($lines[1278] -match 'rec: Musetti') {
    $lines[1278] = $lines[1278] -replace '</td>$', ' <b style="color:#3fb950;">&#x2192; HIT 7-5 6-2 +0.27u</b></td>'
    Write-Host "Musetti screening updated"
}
# Cobolli screening row line 1307 (index 1306)
if ($lines[1306] -match 'rec: Cobolli') {
    $lines[1306] = $lines[1306] -replace '</td>$', ' <b style="color:#3fb950;">&#x2192; HIT 6-4 7-5 +0.21u</b></td>'
    Write-Host "Cobolli screening updated"
}
# Kopriva screening row line 1314 (index 1313)
if ($lines[1313] -match 'rec: Kopriva') {
    $lines[1313] = $lines[1313] -replace '</td>$', ' <b style="color:#3fb950;">&#x2192; HIT 6-3 5-7 6-2 +0.36u</b></td>'
    Write-Host "Kopriva screening updated"
}

# ===== Note update line 1835 (index 1834) =====
if ($lines[1834] -match 'ATP W16') {
    $lines[1834] = $lines[1834] -replace 'ATP W16 R1[^<]*', 'ATP W16 R1&#x5168;HIT(Musetti/Cobolli/Kopriva)'
    Write-Host "Note updated"
}

$lines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done"
