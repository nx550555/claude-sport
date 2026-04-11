# ============================================================
# Windows タスクスケジューラへの登録（管理者権限で実行）
# 右クリック > 「管理者として実行」で実行してください
# ============================================================

$ScriptPath = "C:\Users\ohwada\Desktop\claude_sport\scripts\auto_update.ps1"
$TaskName   = "SportsDashboardAutoUpdate"

# ── 既存タスクを削除してから再登録 ────────────────────────
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "既存タスクを削除しました" -ForegroundColor Yellow
}

# ── アクション: PowerShell でスクリプト実行 ───────────────
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -NonInteractive -WindowStyle Hidden -File `"$ScriptPath`""

# ── トリガー: 毎日 08:30 と 20:30 ────────────────────────
$triggerMorning = New-ScheduledTaskTrigger -Daily -At "08:30"
$triggerEvening = New-ScheduledTaskTrigger -Daily -At "20:30"

# ── 設定: ネットワーク接続後に実行・失敗時は1分後に再試行 ─
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -RestartCount 2 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# ── 現在のユーザーで実行（パスワード入力あり）───────────────
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Highest

# ── 登録 ─────────────────────────────────────────────────
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $triggerMorning, $triggerEvening `
    -Settings $settings `
    -Principal $principal `
    -Description "Sports Betting Dashboard を1日2回自動更新してGitHub Pagesへ公開"

Write-Host ""
Write-Host "=== タスク登録完了 ===" -ForegroundColor Green
Write-Host "タスク名: $TaskName"
Write-Host "実行時刻: 毎日 08:30 と 20:30"
Write-Host ""
Write-Host "確認方法: タスクスケジューラを開いて '$TaskName' を探してください"
Write-Host "手動テスト: " -NoNewline
Write-Host "Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Cyan
