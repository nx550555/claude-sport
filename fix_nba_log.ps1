$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\records\nba\2025-26.json"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

$anchor = "      ]
    }
  ]
}"
$insertContent = [System.IO.File]::ReadAllText("$base\nba_log_insert.txt", [System.Text.Encoding]::UTF8)
$newEnding = "      ]
    }" + $insertContent + "
  ]
}"

if ($content.Contains($anchor)) {
    $content = $content.Replace($anchor, $newEnding)
    Write-Host "  INSERTED: NBA play-in screening log"
} else {
    Write-Host "  NOT FOUND: anchor"
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done: nba/2025-26.json updated"
