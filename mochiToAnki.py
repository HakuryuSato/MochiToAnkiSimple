import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# .envファイルから環境変数をロード
load_dotenv()

# APIキーを取得
API_KEY = os.getenv("MOCHI_API_KEY")

if not API_KEY:
    raise ValueError("APIキーが設定されていません。.envファイルを確認してください。")

# APIのエンドポイント
API_BASE_URL = "https://app.mochi.cards/api"

# 認証情報の設定
auth = HTTPBasicAuth(API_KEY, '')

# デッキの一覧を取得する関数
def get_deck_list():
    url = f"{API_BASE_URL}/decks"
    response = requests.get(url, auth=auth)
    response.raise_for_status()  # エラーがあれば例外を発生
    return response.json()

# 特定のデッキのカードを取得する関数
def get_cards(deck_id, limit=10):
    url = f"{API_BASE_URL}/decks/{deck_id}/cards"
    params = {"limit": limit}  # 上限を設定
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    return response.json()

# メイン処理
def main():
    try:
        # デッキの一覧を取得
        print("デッキ一覧を取得中...")
        decks = get_deck_list()

        if not decks:
            print("デッキが見つかりませんでした。")
            return

        # デッキ一覧を表示
        print("取得したデッキ一覧:")
        for idx, deck in enumerate(decks):
            print(f"{idx + 1}: {deck['name']} (ID: {deck['id']})")

        # 最初のデッキを選択
        first_deck = decks[0]
        print(f"\n最初のデッキを選択: {first_deck['name']} (ID: {first_deck['id']})")

        # 選択したデッキからカードを取得
        print(f"\nデッキ '{first_deck['name']}' からカードを取得中...")
        cards = get_cards(first_deck["id"], limit=10)

        # カードを出力
        print(f"デッキ '{first_deck['name']}' の最初の10枚のカード:")
        for card in cards:
            print(f"- {card['front']}")  # フロントの内容を表示（必要に応じて修正）

    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
