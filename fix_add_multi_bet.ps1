$enc = [System.Text.Encoding]::UTF8

# ============================================================
# 1. dashboard.html - タブ追加 + コンテンツセクション追加
# ============================================================
$dashPath = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$dash = [System.IO.File]::ReadAllText($dashPath, $enc)

# --- (1a) id="tab-excluded" の行末に新タブ2つを挿入 ---
$marker1 = 'id="tab-excluded"'
$idx1 = $dash.IndexOf($marker1)
if ($idx1 -lt 0) { Write-Error "tab-excluded not found"; exit 1 }
$lineEnd1 = $dash.IndexOf([char]10, $idx1)
$newTabs = "`n  <div class=`"tab`" id=`"tab-highprob`" onclick=`"showTab('highprob')`">&#x1F3AF; 高確率予想</div>`n  <div class=`"tab`" id=`"tab-multi`" onclick=`"showTab('multi')`">&#x1F517; マルチベット</div>"
$dash = $dash.Substring(0, $lineEnd1) + $newTabs + $dash.Substring($lineEnd1)

# --- (1b) <div class="footer"> の直前にコンテンツセクション2つを挿入 ---
$marker2 = '<div class="footer">'
$idx2 = $dash.IndexOf($marker2)
if ($idx2 -lt 0) { Write-Error "footer not found"; exit 1 }

$newContent = @'

<!-- ===== 高確率予想 (Output A) ===== -->
<div class="tab-content" id="content-highprob">
  <div class="section">
    <div class="section-title">高確率予想リスト（出力A）</div>
    <p style="color:var(--text2);font-size:12px;margin-bottom:16px;line-height:1.7;">
      L1〜L4の4層評価で<strong style="color:var(--text);">確実視できる</strong>と判断した試合のみ掲載。少しでも迷いがある試合は含めない。
      確実性が高い順に並ぶ。
    </p>
    <div class="table-wrap">
      <table class="data-table" id="highprob-table">
        <thead>
          <tr>
            <th>No.</th>
            <th>試合名</th>
            <th>種目</th>
            <th>推奨</th>
            <th>推定勝率</th>
            <th>オッズ</th>
            <th>確実と判断した理由</th>
            <th>結果</th>
          </tr>
        </thead>
        <tbody id="highprob-rows">
          <tr>
            <td colspan="8" style="text-align:center;color:var(--text2);padding:40px;font-size:13px;">
              次回の分析セッションから記録開始
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div id="highprob-session-info" style="margin-top:10px;font-size:11px;color:var(--text2);"></div>
  </div>
</div>

<!-- ===== マルチベット (Output B) ===== -->
<div class="tab-content" id="content-multi">
  <div class="section">
    <div class="section-title">高確率マルチベット（出力B）</div>
    <p style="color:var(--text2);font-size:12px;margin-bottom:16px;line-height:1.7;">
      出力Aの試合のみ使用。マルチEV = (全体推定勝率 × マルチオッズ) − 1。EV+の組み合わせを高い順に上位5パターン表示。
    </p>
    <div id="multi-rows" style="display:flex;flex-direction:column;gap:12px;">
      <div style="text-align:center;color:var(--text2);padding:40px;font-size:13px;background:var(--surface);border:1px solid var(--border);border-radius:8px;">
        次回の分析セッションから記録開始。出力Aが2件以上の場合に表示。
      </div>
    </div>
    <div id="multi-session-info" style="margin-top:10px;font-size:11px;color:var(--text2);"></div>
  </div>
</div>

'@

$dash = $dash.Substring(0, $idx2) + $newContent + $dash.Substring($idx2)
[System.IO.File]::WriteAllText($dashPath, $dash, $enc)
Write-Host "dashboard.html: OK"

# ============================================================
# 2. CLAUDE.md - スクリーニング後フロー追記
# ============================================================
$claudePath = "C:\Users\ohwada\Desktop\claude_sport\CLAUDE.md"
$claude = [System.IO.File]::ReadAllText($claudePath, $enc)

$claudeMarker = '**【会話終了時】'
$cidx = $claude.IndexOf($claudeMarker)
if ($cidx -lt 0) { Write-Error "CLAUDE.md marker not found"; exit 1 }

$newSection = @'
**【スクリーニング完了後・毎回必須】高確率予想・マルチベット出力：**
全スポーツのスクリーニングが完了したら以下を実行する：

1. **出力A（高確率予想リスト）**を生成する
   - L1〜L4で「確実視できる」と判断した試合のみ抽出（少しでも迷いがある試合は含めない）
   - 確実性が高い順に出力。該当なし→「該当なし」と出力
   - 出力形式: No. | 試合名 | スポーツ | 推奨 | 推定勝率 | オッズ | 確実と判断した理由
2. **出力B（高確率マルチベット）**を計算する
   - 出力Aが2件以上の場合のみ実行（1件以下→「マルチ構成不可」と出力）
   - マルチオッズ = 各オッズの積 / 全体推定勝率 = 各勝率の積 / マルチEV = (全体推定勝率 × マルチオッズ) - 1
   - EV+の組み合わせをマルチEV高い順に上位5パターン出力
   - 全組み合わせがEV-なら「EV+の組み合わせなし」と出力
3. `records/multi_bets.json` の sessions 配列に追記する
4. `dashboard.html` の「高確率予想」「マルチベット」タブを更新する

'@

$claude = $claude.Substring(0, $cidx) + $newSection + $claude.Substring($cidx)
[System.IO.File]::WriteAllText($claudePath, $claude, $enc)
Write-Host "CLAUDE.md: OK"
