# Session_62 フェーズ6 統合動作確認 / A-3 遡及判断 議題リスト

> **目的**: フェーズ6 (統合動作確認) または A-3 遡及判断タスク実施時に参照する議題集積ファイル。
> **記録方針**: 各フェーズ進行中に発生した「次フェーズ以降で検討すべき論点」を時系列で蓄積する。
> **本ファイルは実装変更を伴わない議題記録専用**。実装は議題承認後に別タスクで実施する。

---

## 議題1: evidence の時間的独立性 (Session_62 フェーズ2 完了時 追加)

**追加日**: 2026-04-27 (フェーズ2 完了時、ユーザー指示により追加記録)

**論点**:
R024 (form slump 補正) の実装プロセス問題について、Session_61 handoff で指摘された「同一 turn 内 evidence 3/3 → implement」だけでなく、**evidence 3件目 (A041 Baptiste-Paolini) 自体が同一 turn 内の「ついで検出」であった**点も新プロトコル違反に該当する。

**具体的経緯**:
- evidence 1件目: A001 Lys-Badosa (旧セッション)
- evidence 2件目: A007 Sonmez-Paolini (旧セッション)
- evidence 3件目: A041 Baptiste-Paolini (Session_61 で Phase2 scope外UPSET スキャン中に検出)
- 同 Session_61 の同一 turn 内で evidence 3/3 到達 → R024 implement

→ evidence 3件目自体がユーザー質問契機の「ついで検出」だったため、(a) 同一 turn 内 implement、(b) 同一 turn 内 evidence 検出、の二重の時間的依存が発生していた。

**新プロトコルへの追加検討事項**:
`forbidden_practices` または `approval_workflow.step1_threshold_reached` に以下のチェックを加えるべきか検討:

- 「evidence 3件は時間的に独立した観察として蓄積されているか」の確認
- 具体判定基準案:
  - (案A) evidence 3件が **異なるセッション** での独立検出であること
  - (案B) evidence 3件が **異なる試合日** (例: 連続する3試合日以外) での検出であること
  - (案C) 同一セッション内で複数件 evidence が追加された場合は、最後の追加から **次セッション以降に proposal 生成** を必須化
  - (案D) ユーザー質問契機での scope外 UPSET 検出 evidence は、自発検出 evidence とは別カウントとして扱う

**判断必要時期**: フェーズ6 統合動作確認時、または A-3 遡及判断 (R024 取り消し / 承認 / 修正後再構築) 時。

**現時点のステータス**: **議題記録のみ。実装変更なし**。

---

## 議題2: STEP 0.5 実施を毎回確実に保証する仕組み (Session_62 フェーズ3 完了時 追加)

**追加日**: 2026-04-27 (フェーズ3 完了時、ユーザー指示により追加記録)

**論点**:
CLAUDE.md 新設【結果反映 STEP 0.5・毎回必須】scope外 UPSET スキャン SOP のサブセクション6 (Session_61 逸脱パターンの再発防止) で定義した検証方法は、現時点では以下のみ:

> 「結果反映 commit と同時に『STEP 0.5 実施済』ログを `monitoring/pending_actions.md` または記録 commit message に明示」

この検証方法は **弱い**。理由:
- commit message は人間が事後で読み返すものであり、Claude が毎回必ず明示するという保証がない (CLAUDE.md 規定の遵守は Claude の自律性に依存)
- 過去 Session_30〜43 で multi_bets.json 更新が抜け続けた事故 (Session_44 で発覚) と同じ構造的リスク
- ユーザー側で「STEP 0.5 を実施したかどうか」を後から検証する手段が乏しい

**論点に含めるべき検討事項**:

フェーズ6 統合動作確認時に、以下のいずれか (または組合せ) を検討すべきか議題化:

- **(案A) 機械的チェッカー導入**: `scripts/verify_step05_executed.py` を作成し、結果反映 commit に対し直前 N時間以内の STEP 0.5 実行ログがあるか自動検証。`monitoring/health_check.py` から呼び出して WARN/ALERT 化
- **(案B) 構造化ログファイル新設**: `monitoring/step05_log.jsonl` を新設し、STEP 0.5 実行のたびに JSON Lines 形式で「実行日時 / 対象スポーツ / 検出件数 / ユーザー判断結果」を append。pending_actions.md 任意記述ではなく構造化された強制ログ
- **(案C) commit hook / pre-push hook**: 結果反映を含む commit に対し、commit message に `[STEP05:DONE]` または `[STEP05:N/A]` タグが含まれていることを必須化する Git hook を導入
- **(案D) records JSON の prediction_hit 更新時にフィールド追加**: `prediction_hit` を `true`/`false` 更新する際に、同じ entry に `step05_scanned_at` フィールドを必須化。未付与の prediction_hit 更新は health_check で検知
- **(案E) 出力フォーマット強制**: 結果反映タスクの最終報告フォーマットに「STEP 0.5 実施結果: N件検出 / 0件 (該当なし)」の行を必須化し、抜けたら自己チェック (CHECK-4) で気付ける構造

**判断必要時期**: フェーズ6 統合動作確認時。フェーズ4-5 完了後にユーザーと協議して、上記案 (またはその他案) のいずれを採用するか確定する。

**現時点のステータス**: **議題記録のみ。実装変更なし**。

---

## (今後の議題追加スペース)

フェーズ4〜5 進行中に発生した追加論点は、本ファイルに「議題3」「議題4」... として時系列追記する。
