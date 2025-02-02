# 自動論文収集プログラム

## 概要
このプログラムは、arXivから論文を収集し、Notionデータベースに登録し、Slackに通知します。

## セットアップ
1. 必要なライブラリをインストールします。
   ```
   pip install -r requirements.txt
   ```
2. `config/.env`ファイルにAPIキーを設定します。
3. Github Actionsを設定して定時実行を有効にします。

## 使用方法
- `src/main.py`を実行して、論文収集を開始します。 