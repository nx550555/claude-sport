# Add GEN003 rule to dashboard + fix Session 29 summary numbers
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# == 1. Fix Session 29 summary: 通算数値を修正 ==
# "27GO / 21確定 / 16HIT 76.2% / EV+2.831u" -> "27GO / 20確定 / 16HIT 80.0% / EV+3.831u"
$html = $html.Replace('27GO / 21' + [char]0x78BA + [char]0x5B9A + ' / 16HIT 76.2% / EV+2.831u', '27GO / 20' + [char]0x78BA + [char]0x5B9A + ' / 16HIT 80.0% / EV+3.831u (Paolini ' + [char]0x7D50 + [char]0x679C + [char]0x5F85 + [char]0x6A5F + ')')
Write-Host "1. Session 29 summary numbers fixed"

# == 2. Insert GEN003 rule entry before the first rule-entry div ==
$anchor = '<div class="rules-list">'
$pos = $html.IndexOf($anchor)
if ($pos -ge 0) {
    $insertAt = $pos + $anchor.Length
    $gen003 = @"


    <div class="rule-entry" style="border-color:#f8514940;">
      <div class="rule-header">
        <span style="color:#f85149;">&#x26A0;&#xFE0F; &#x5168;&#x30B9;&#x30DD;&#x30FC;&#x30C4;&#x5171;&#x901A;</span>
        <span class="rule-ver-badge">GEN003 &#x65B0;&#x8A2D;</span>
        <span class="rule-date">2026-04-15</span>
      </div>
      <div class="rule-trigger">&#x1F6A8; &#x30C8;&#x30EA;&#x30AC;&#x30FC;: WTA Stuttgart R1 Paolini vs Sonmez &#x2014; &#x63D0;&#x4F9B;JSON&#x306E;&#x30C7;&#x30FC;&#x30BF;&#x6C5A;&#x67D3;&#x8A3C;&#x62E0;&#x3060;&#x3051;&#x3067;MISS&#x3068;&#x8AA4;&#x8A18;&#x9332;&#x3002;WTA&#x516C;&#x5F0F;&#x78BA;&#x8A8D;&#x3067;&#x300C;1st Set Suspended&#xFF08;&#x8A66;&#x5408;&#x672A;&#x5B8C;&#x4E86;&#xFF09;&#x300D;&#x3068;&#x5224;&#x660E;&#x3002;</div>
      <ul class="rule-changes">
        <li><strong>GEN003&#x65B0;&#x8A2D;: &#x8ABF;&#x67FB;&#x53EF;&#x80FD;&#x306A;&#x60C5;&#x5831;&#x306F;&#x5FC5;&#x305A;&#x4E00;&#x6B21;&#x30BD;&#x30FC;&#x30B9;&#x3067;&#x78BA;&#x8A8D;&#x3059;&#x308B;</strong>
          &#x2014; &#x8A66;&#x5408;&#x7D50;&#x679C;&#x30FB;&#x30AA;&#x30C3;&#x30BA;&#x30FB;&#x30B9;&#x30BF;&#x30C3;&#x30C4;&#x7B49;&#x3001;&#x8ABF;&#x3079;&#x308C;&#x3070;&#x6B63;&#x78BA;&#x306B;&#x78BA;&#x8A8D;&#x3067;&#x304D;&#x308B;&#x60C5;&#x5831;&#x306B;&#x5BFE;&#x3057;&#x3066;&#x3001;&#x63A8;&#x8AD6;&#x30FB;&#x4E88;&#x6E2C;&#x30FB;&#x30C7;&#x30FC;&#x30BF;&#x89E3;&#x91C8;&#x3067;&#x300C;&#x4E8B;&#x5B9F;&#x300D;&#x3068;&#x3057;&#x3066;&#x6271;&#x3046;&#x3053;&#x3068;&#x306F;&#x7D76;&#x5BFE;&#x7981;&#x6B62;&#x3002;</li>
        <li>JSON&#x30C7;&#x30FC;&#x30BF;&#x306B;&#x7D50;&#x679C;&#x3089;&#x3057;&#x304D;&#x60C5;&#x5831;&#x304C;&#x3042;&#x3063;&#x3066;&#x3082;&#x3001;WebSearch/WebFetch&#x3067;&#x516C;&#x5F0F;&#x30BD;&#x30FC;&#x30B9;&#x3092;&#x78BA;&#x8A8D;&#x3059;&#x308B;&#x307E;&#x3067;&#x300C;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#x300D;&#x3068;&#x3057;&#x3066;&#x6271;&#x3046;&#x3002;</li>
        <li>&#x4E8B;&#x5B9F;&#x3068;&#x4E88;&#x6E2C;&#x30FB;&#x63A8;&#x8AD6;&#x306F;&#x5E38;&#x306B;&#x660E;&#x793A;&#x7684;&#x306B;&#x533A;&#x5225;&#x3057;&#x3066;&#x4F1D;&#x3048;&#x308B;&#x3002;</li>
      </ul>
      <div class="rule-result">&#x5909;&#x66F4;&#x524D;: <span style="color:#f85149;">&#x8ABF;&#x67FB;&#x3059;&#x308C;&#x3070;&#x5206;&#x304B;&#x308B;&#x60C5;&#x5831;&#x3092;&#x63A8;&#x8AD6;&#x3067;&#x4EE3;&#x66FF;</span> &#x2192; &#x5909;&#x66F4;&#x5F8C;: <span style="color:#3fb950;">WebSearch&#x3067;&#x4E00;&#x6B21;&#x30BD;&#x30FC;&#x30B9;&#x5FC5;&#x9808;&#x78BA;&#x8A8D;&#x5F8C;&#x306B;&#x8A18;&#x9332;</span></div>
      <div class="rule-note">&#x1F4A1; Paolini(MISS&#x8AA4;&#x8A18;&#x9332;)&#x2192;&#x5373;&#x5EA7;&#x306B;WTA&#x516C;&#x5F0F;&#x30B5;&#x30A4;&#x30C8;&#x3067;&#x78BA;&#x8A8D;&#x3057;&#x8A02;&#x6B63;&#x3002;&#x8AAD;&#x307F;&#x53D6;&#x308C;&#x308B;&#x30C7;&#x30FC;&#x30BF;&#x3068;&#x78BA;&#x5B9A;&#x3057;&#x305F;&#x4E8B;&#x5B9F;&#x306F;&#x5225;&#x7269;&#x3002;</div>
    </div>
"@
    $html = $html.Substring(0, $insertAt) + $gen003 + $html.Substring($insertAt)
    Write-Host "2. GEN003 rule inserted"
} else {
    Write-Host "2. rules-list anchor not found"
}

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "GEN003 addition complete."
