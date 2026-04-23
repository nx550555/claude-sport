# メール通知セットアップ手順 (Gmail SMTP)

このドキュメントは、正式 GO 候補が発生した時のメール通知機能を動かすための認証情報セットアップ手順です。所要時間 5〜10 分。

---

## 必要な GitHub Secrets (6 件)

| Name | Value | 備考 |
|---|---|---|
| `SMTP_HOST` | `smtp.gmail.com` | 固定 |
| `SMTP_PORT` | `465` | 固定 (SSL) |
| `SMTP_USER` | Gmail アドレス | 送信元として使う Gmail |
| `SMTP_PASS` | Gmail App Password (16 桁) | 通常ログインパスワードでは NG |
| `NOTIFY_TO` | `ohwada@ad-link.co.jp` | 通知先メールアドレス |
| `NOTIFY_FROM` | Gmail アドレス | `SMTP_USER` と同じで OK |

---

## STEP 1: Google アカウントで 2 段階認証を有効化

App Password は 2 段階認証が有効なアカウントでしか作れません。

1. https://myaccount.google.com/security にアクセス
2. 「2 段階認証プロセス」→ 画面指示で有効化
3. 「オン」になっていることを確認

---

## STEP 2: App Password 生成

1. https://myaccount.google.com/apppasswords にアクセス
2. アプリ名を入力 (例: `claude-sport-notify`)
3. 「作成」ボタンを押す
4. 表示された 16 桁 (例: `abcd efgh ijkl mnop`) をコピー
   - **二度と表示されない**のでそのまま次の STEP へ
   - スペースは入力時に除去 (例: `abcdefghijklmnop`)

---

## STEP 3: GitHub Secrets に登録

1. `https://github.com/nx550555/claude-sport/settings/secrets/actions` にアクセス
2. `[New repository secret]` を押す
3. 上記テーブルの値を **1 件ずつ** 追加 (計 6 件)
4. 保存後は値を再表示できない仕様 (名前のみ一覧に残る)

---

## トラブルシューティング

| 症状 | 原因と対処 |
|---|---|
| `myaccount.google.com/apppasswords` が開けない | 2 段階認証が未有効 → STEP 1 をやり直す |
| App Password が「利用できません」と表示 | Google Workspace (会社ドメイン) アカウントで管理者が App Password を禁止 → 個人 Gmail を使う |
| GitHub Secrets 画面が見当たらない | リポジトリの `Settings` → `Secrets and variables` → `Actions` |
| 会社ドメイン `@ad-link.co.jp` から送りたい | Gmail SMTP の仕様上 SMTP_USER の Gmail アドレスが強制送信元になる。会社ドメインから送りたい場合は Google Workspace SMTP 設定または SendGrid への切替が必要 |

---

## 動作確認

Secrets を登録後、GitHub Actions で `notify_go.yml` を手動 dispatch すると接続テストメールが送信されます。

```
Actions タブ → "Notify GO Candidate" ワークフロー → "Run workflow"
```

受信 BOX に以下のようなメールが届けば OK:

```
Subject: [claude-sport] テスト通知
Body:   メール通知システムは正常に動作しています。
```

---

## 通知トリガー (C モード)

本システムは以下の 2 系統でメールを送信します:

1. **即時通知 (A 系)**: スタメン確認後の EV 再計算で正式 GO に昇格した瞬間、1 試合 1 メール
2. **日次ダイジェスト (B 系)**: JST 23:00 に当日昇格分をまとめて 1 メール

通知されるスポーツ: NBA / NFL / ラグビー全種 / サッカー / MLB
(それ以外のスポーツは従来通り records JSON 追記のみで、メール通知はしません)
