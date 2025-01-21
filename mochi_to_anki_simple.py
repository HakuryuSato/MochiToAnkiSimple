import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import json
import datetime

# ---------------------------------------------------------
# 1. Mochi Cards からのデータ取得
# ---------------------------------------------------------

load_dotenv()
API_KEY = os.getenv("MOCHI_API_KEY")
if not API_KEY:
    raise ValueError("API key is not set. Please check your .env file.")

MOCHI_API_BASE_URL = "https://app.mochi.cards/api"


async def fetch_cards(session, url, params):
    """
    Fetches a batch of cards from the Mochi Cards API using aiohttp.
    Raises an exception if the response status is not successful.
    """
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


async def get_all_cards_async():
    """
    Retrieves all cards from the Mochi Cards API by following bookmark pagination.
    Returns a list of card dictionaries.
    """
    url = f"{MOCHI_API_BASE_URL}/cards"
    all_cards = []
    limit = 100
    bookmark = None
    seen_bookmarks = set()

    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(API_KEY, "")) as session:
        while True:
            params = {"limit": limit}
            if bookmark:
                params["bookmark"] = bookmark

            data = await fetch_cards(session, url, params)
            cards = data.get("docs", [])
            all_cards.extend(cards)

            # Debug print; can be removed if not needed
            bookmark = data.get("bookmark")
            print("Current bookmark:", bookmark)

            # If there's no bookmark or we've seen it before, break the loop
            if (not bookmark) or (bookmark in seen_bookmarks):
                print("complete get_all_cards_async()")
                break
            seen_bookmarks.add(bookmark)

    return all_cards

def get_deck_list():
    """
    Retrieves a list of decks from the Mochi Cards API.
    Returns a list of deck dictionaries.
    """
    url = f"{MOCHI_API_BASE_URL}/decks"
    auth = HTTPBasicAuth(API_KEY, "")
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    data = response.json()
    return data.get("docs", [])


# ---------------------------------------------------------
# 2. JSONファイルへの書き出し
# ---------------------------------------------------------

def create_json_filename(prefix="mochi_cards_full_data"):
    """
    Creates a JSON filename with the current date-time appended.
    """
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    return f"{prefix}_{now_str}.json"


def write_cards_to_json(file_name, decks, all_cards):
    """
    Writes card data to a JSON file. Additionally adds "deck-name" to each card
    by looking up the corresponding deck ID in the provided decks list.
    """
    # デッキID -> デッキ名 の辞書を作成
    deck_dict = {deck["id"]: deck["name"] for deck in decks}

    # カードごとに deck-name を付与する
    for card in all_cards:
        deck_id = card.get("deck-id")
        deck_name = deck_dict.get(deck_id, "Unknown Deck")
        card["deck-name"] = deck_name

    # JSONとして書き出し
    with open(file_name, mode="w", encoding="utf-8") as json_file:
        # ensure_ascii=False で日本語を文字列のまま書き出し
        # indent=2 は可読性のために整形出力
        json.dump(all_cards, json_file, ensure_ascii=False, indent=2)

    print(f"\nJSON file '{file_name}' has been created successfully.")


# ---------------------------------------------------------
# 3. AnkiConnect を使って Anki にアップロード
# ---------------------------------------------------------

def import_to_anki(json_file_path):
    """
    Reads the specified JSON (exported from Mochi Cards),
    and imports the data into Anki via AnkiConnect.
    Each card's "deck-name" becomes the Anki deck name.
    "name" is Front, "content" is Back, as a basic example.
    """

    # AnkiConnect のデフォルトURL (Ankiが起動している & アドオンが有効になっていること)
    ANKI_CONNECT_URL = "http://localhost:8765"

    with open(json_file_path, "r", encoding="utf-8") as f:
        mochi_cards = json.load(f)

    # Ankiに追加するノート群を作成
    notes_for_anki = []
    for card in mochi_cards:
        deck_name = card.get("deck-name", "Mochi Imported")
        front_text = card.get("name", "")
        back_text = card.get("content", "")

        # AnkiConnectのaddNotesに渡すフォーマット
        note = {
            "deckName": deck_name,             # 該当のデッキが無い場合は自動で作成される
            "modelName": "Basic",              # Anki標準の「Basic」モデルを使用
            "fields": {
                "Front": front_text,
                "Back": back_text
            },
            "tags": ["mochiImport"]            # 全てのカードに "mochiImport" タグ付与
        }
        notes_for_anki.append(note)

    # addNotes リクエスト本体
    payload = {
        "action": "addNotes",
        "version": 6,
        "params": {
            "notes": notes_for_anki
        }
    }

    print("\nSending notes to Anki...")
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        print("AnkiConnect response:", result)
    except requests.exceptions.RequestException as e:
        print("Failed to send notes to Anki:", e)


# ---------------------------------------------------------
# 4. メインフロー
# ---------------------------------------------------------
def main():
    try:
        print("Retrieving deck list from Mochi...")
        decks = get_deck_list()

        if not decks:
            print("No decks found in Mochi.")
            return

        # Retrieve all cards asynchronously
        print("Retrieving card list from Mochi...")
        all_cards = asyncio.run(get_all_cards_async())
        if not all_cards:
            print("No cards found at all.")
            return

        # JSONファイル名を作成して書き出し
        json_file_name = create_json_filename()
        write_cards_to_json(json_file_name, decks, all_cards)

        # JSONを読み込み、Ankiへインポート
        import_to_anki(json_file_name)

    except requests.exceptions.RequestException as e:
        print(f"An error has occurred while fetching from Mochi: {e}")


if __name__ == "__main__":
    main()
