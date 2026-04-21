# Playwright セットアップ手順（A案 / GEN006）

ユーザー側で以下を 1 回だけ実行してください（Claude は実行権限がないため）。

## Windows PowerShell

```powershell
cd C:\Users\ohwada\Desktop\claude_sport
pip install playwright
playwright install chromium
```

インストール容量: Chromium 約 400MB, Playwright パッケージ約 30MB。

## 動作確認

```powershell
python scripts\fetch_moneypuck.py --days-stale 0
python scripts\fetch_basketball_reference.py --days-stale 0
```

成功すると `stats/external_feeds/nhl_moneypuck_YYYY-MM-DD.json` と `nba_bbref_YYYY-MM-DD.json` が生成されます。

## GitHub Actions (D案) の有効化

1. リポジトリの Settings → Actions → General で "Allow all actions" を有効化
2. Settings → Actions → General → "Workflow permissions" を "Read and write permissions" に変更
3. リモート `origin` が GitHub リポジトリに向いていれば、次回 push 後から自動で `.github/workflows/fetch_stats.yml` が JST 09:00 / 21:00 に稼働

## 失敗時

- Chromium がロードに失敗する → `playwright install --with-deps chromium`
- MoneyPuck が bot 検知で 403 → GEN006 でユーザー依頼発動（Claude セッション内で Claude が案内）
- サイト構造変更でカラム取得失敗 → scripts/fetch_moneypuck.py の `idx()` 内のキー名を修正

## 備考

- Claude Code (CLI) は Playwright を `Bash` 経由で起動するのみ。ブラウザ UI 操作は不可
- 認証必要サイト (例: Hockey-Reference 一部有料ページ) はこの仕組みでは取得できない → GEN006 で手動依頼
- 地理制限 (一部 NFL/NBA 統計) は GitHub Actions 上の ubuntu-latest で回避できる場合あり（D案の強み）
