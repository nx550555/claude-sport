$file = "C:\Users\ohwada\Desktop\claude_sport\records\tennis\2026-ATP.json"
$content = Get-Content -Raw -Encoding UTF8 $file

# Musetti vs Landaluce (Barcelona R1) HIT 7-5 6-2
$anchor = '"Musetti L.(2) vs Landaluce M."'
$idx = $content.IndexOf($anchor)
if ($idx -ge 0) {
    $segment = $content.Substring($idx)
    $old = '"result": null, "score": null, "hit": null, "actual_ev": null,'
    $new = '"result": "Musetti", "score": "7-5 6-2", "hit": true, "actual_ev": 0.27,'
    $pos = $segment.IndexOf($old)
    if ($pos -ge 0 -and $pos -lt 600) {
        $content = $content.Substring(0, $idx + $pos) + $new + $content.Substring($idx + $pos + $old.Length)
        Write-Host "Musetti updated"
    } else { Write-Host "Musetti: old string not found within range" }
} else { Write-Host "Musetti anchor not found" }

# Cobolli vs Dedura-Palmero (Munich R1) HIT 6-4 7-5
$anchor = '"Cobolli F.(4) vs Dedura-Palmero D."'
$idx = $content.IndexOf($anchor)
if ($idx -ge 0) {
    $segment = $content.Substring($idx)
    $old = '"result": null, "score": null, "hit": null, "actual_ev": null,'
    $new = '"result": "Cobolli", "score": "6-4 7-5", "hit": true, "actual_ev": 0.21,'
    $pos = $segment.IndexOf($old)
    if ($pos -ge 0 -and $pos -lt 600) {
        $content = $content.Substring(0, $idx + $pos) + $new + $content.Substring($idx + $pos + $old.Length)
        Write-Host "Cobolli updated"
    } else { Write-Host "Cobolli: old string not found within range" }
} else { Write-Host "Cobolli anchor not found" }

# Kopriva vs Engel (Munich R1) HIT 6-3 5-7 6-2
$anchor = '"Engel J.(WC) vs Kopriva V."'
$idx = $content.IndexOf($anchor)
if ($idx -ge 0) {
    $segment = $content.Substring($idx)
    $old = '"result": null, "score": null, "hit": null, "actual_ev": null,'
    $new = '"result": "Kopriva", "score": "6-3 5-7 6-2", "hit": true, "actual_ev": 0.36,'
    $pos = $segment.IndexOf($old)
    if ($pos -ge 0 -and $pos -lt 600) {
        $content = $content.Substring(0, $idx + $pos) + $new + $content.Substring($idx + $pos + $old.Length)
        Write-Host "Kopriva updated"
    } else { Write-Host "Kopriva: old string not found within range" }
} else { Write-Host "Kopriva anchor not found" }

$content | Set-Content -Path $file -Encoding UTF8 -NoNewline
Write-Host "ATP W16 results updated successfully"
