# ============================================================
# Sports Betting Dashboard - 自動更新スクリプト
# スケジュール: 1日2回 (タスクスケジューラから実行)
# ============================================================

$ErrorActionPreference = "Stop"
$ProjectDir = "C:\Users\ohwada\Desktop\claude_sport"
$ClaudeExe  = "C:\Users\ohwada\.local\bin\claude.exe"
$LogFile    = "$ProjectDir\scripts\auto_update.log"

Set-Location $ProjectDir

# ── タイムスタンプ計算 ─────────────────────────────────────
$now     = Get-Date
$nowStr  = $now.ToString("yyyy/MM/dd HH:mm") + " JST"

# 次回は12時間後（朝8:30→夜20:30、夜20:30→翌朝8:30）
$nextRun = $now.AddHours(12).ToString("yyyy/MM/dd HH:mm") + " JST"

# ── ログ記録 ──────────────────────────────────────────────
function Write-Log($msg) {
    $line = "[$($now.ToString('yyyy-MM-dd HH:mm:ss'))] $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

Write-Log "=== 自動更新開始 ==="
Write-Log "現在: $nowStr  /  次回: $nextRun"

# ── Claude 分析プロンプト ────────────────────────────────
$prompt = @"
【完全自動実行モード】人間の確認なしに以下を順番に実行してください。

現在時刻: $nowStr
次回自動更新予定: $nextRun

## 実行手順

### 手順1: 状況把握
BACKLOG.md と stats/cumulative.json を読んで、
「hit: null」または「status: pending」の未確認試合を洗い出す。

### 手順2: 結果確認
未確認の各試合について WebSearch で結果を検索して確認する。
（例: "NRL 2026 Round 6 Rabbitohs Raiders result"）
確認できたら records/ の該当ファイルを更新する（hit/score/actual_ev）。

### 手順3: 新規試合スクリーニング
今日・明日に予定されている対象試合（NRL/NHL/NBA/SuperRugby/UFL/Tennis）を
WebSearch で確認し、core/rules_*.json の L1〜L4 に従って分析する。
GO候補があれば records/ に追記する。

### 手順4: ダッシュボード更新
dashboard.html を更新する:
- ヘッダーの last-updated-time を「$nowStr」に変更
- ヘッダーの next-update-time を「$nextRun」に変更
- KPI数値（総GO数・正答率・EV合計・待機数）を最新値に更新
- アクティブ推奨タブ（GO中の試合カード）を更新
- 全履歴タブに新規結果行を追加
- 分析ログタブに今回のスクリーニング結果を追加

### 手順5: 集計ファイル更新
stats/cumulative.json の数値を最新状態に更新する。

### 手順6: BACKLOG更新
BACKLOG.md の完了項目を [x] に更新し、新規 [ ] 項目があれば追加する。

### 注意事項
- GO判断は信頼度≥75% AND EV>+5% の両方を満たす場合のみ
- テニスはcElo差≥150ptが基本（rules_tennis_atp.json参照）
- NRL R3-R8はL1閾値12pt（R012）
- すべてのファイル更新後に「完了: [更新内容のサマリー]」を出力する
"@

# ── Claude 実行 ────────────────────────────────────────────
Write-Log "Claude 分析開始..."
try {
    & $ClaudeExe -p $prompt
    Write-Log "Claude 分析完了"
} catch {
    Write-Log "ERROR: Claude 実行失敗 - $_"
    exit 1
}

# ── GitHub Pages へプッシュ ────────────────────────────────
Write-Log "GitHub Pages へプッシュ中..."
try {
    git add -A
    $changed = git status --porcelain
    if ($changed) {
        $commitMsg = "Auto update $($now.ToString('yyyy-MM-dd HH:mm'))"
        git commit -m $commitMsg
        git push origin main
        Write-Log "プッシュ完了: $commitMsg"
    } else {
        Write-Log "変更なし - プッシュスキップ"
    }
} catch {
    Write-Log "ERROR: git push 失敗 - $_"
    exit 1
}

Write-Log "=== 自動更新完了 ==="
