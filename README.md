# Mochi to Anki Converter

MochiカードからAnkiへカードをインポートするためのPythonスクリプト。

## 機能

- Mochi Cards APIからデッキとカードを取得
- カード情報をJSONファイルに保存
- AnkiConnectを使用してAnkiへカードをインポート

## 必要条件

- Python 3.7以上
- Anki 2.1.x
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) アドオン
- Mochi Cards API キー

## セットアップ

1. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

2. `.env`ファイルを作成し、Mochi Cards APIキーを設定:
```
MOCHI_API_KEY=your_api_key_here
```

3. Ankiを起動し、AnkiConnectアドオンがインストールされていることを確認

## 使用方法

1. Ankiを起動した状態で以下のコマンドを実行:
```bash
python main.py
```

2. スクリプトは以下の処理を行います:
   - Mochiからデッキ一覧を取得
   - 全てのカードを取得
   - カード情報をJSONファイルに保存
   - AnkiConnectを使用してAnkiへカードをインポート

## ファイル構成

- `main.py`: メインの実行ファイル
- `config.py`: 設定と定数
- `mochi_api.py`: Mochi Cards APIとの通信
- `json_handler.py`: JSONファイルの操作
- `anki_connect.py`: AnkiConnectとの通信

## 注意事項

- Ankiは実行中である必要があります
- AnkiConnectアドオンがインストールされている必要があります
- 有効なMochi Cards APIキーが必要です
