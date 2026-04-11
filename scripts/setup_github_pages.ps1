# ============================================================
# GitHub Pages 初期セットアップ（初回のみ実行）
# 実行前に: GitHubアカウント作成 & git インストール確認
# ============================================================

# ── 設定: ここだけ書き換えてください ─────────────────────
$GitHubUsername = "nx550555"               # あなたのGitHubユーザー名
$RepoName       = "claude-sport"           # リポジトリ名（変更可）
# 完成URL: https://$GitHubUsername.github.io/$RepoName/dashboard.html
# ─────────────────────────────────────────────────────────────

$ProjectDir = "C:\Users\ohwada\Desktop\claude_sport"
Set-Location $ProjectDir

Write-Host "=== GitHub Pages セットアップ ===" -ForegroundColor Cyan

# 1. git 初期化
Write-Host "1. git init..." -ForegroundColor Yellow
git init
git branch -M main

# 2. .gitignore 作成
Write-Host "2. .gitignore 作成..." -ForegroundColor Yellow
@"
# ログファイル
scripts/auto_update.log

# OS
.DS_Store
Thumbs.db
desktop.ini

# エディタ
.vscode/
*.swp
"@ | Set-Content ".gitignore"

# 3. リモート追加（GitHubでリポジトリを先に作成してから実行）
Write-Host "3. リモート設定..." -ForegroundColor Yellow
git remote add origin "https://github.com/$GitHubUsername/$RepoName.git"

# 4. 初回コミット & プッシュ
Write-Host "4. 初回コミット..." -ForegroundColor Yellow
git add -A
git commit -m "Initial commit - Sports Betting Dashboard"
git push -u origin main

Write-Host ""
Write-Host "=== 完了 ===" -ForegroundColor Green
Write-Host "次のステップ:" -ForegroundColor Cyan
Write-Host "  1. GitHub.com で $RepoName リポジトリを開く"
Write-Host "  2. Settings → Pages → Branch: main, Folder: root → Save"
Write-Host "  3. 数分後にアクセス可能になります:"
$url = "https://" + $GitHubUsername + ".github.io/" + $RepoName + "/dashboard.html"
Write-Host "     $url" -ForegroundColor Green
