"""Module for interacting with AnkiConnect."""

import requests
from config import ANKI_CONNECT_URL, DEFAULT_MODEL_NAME


def ensure_basic_model(model_name: str = DEFAULT_MODEL_NAME):
    """
    Checks if a model with the given name exists in Anki.
    If not, creates the model via AnkiConnect.
    """
    # 1) まず Anki に存在するモデル一覧を取得
    payload = {"action": "modelNames", "version": 6}
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()

    if response.get("error"):
        print("Error retrieving model names from Anki:", response["error"])
        return

    model_names = response.get("result", [])
    print("Existing Anki models:", model_names)

    # 2) 指定した model_name がなければ新規作成
    if model_name not in model_names:
        print(f"Model '{model_name}' not found. Creating it in Anki...")

        create_payload = {
            "action": "createModel",
            "version": 6,
            "params": {
                "modelName": model_name,
                "inOrderFields": ["Front", "Back"],
                "css": ".card {\n font-family: arial;\n font-size: 20px;\n}\n",
                "isCloze": False,
                "cardTemplates": [
                    {
                        "Name": "Card 1",
                        "Front": "{{Front}}",
                        "Back": "{{Back}}"
                    }
                ]
            }
        }
        create_response = requests.post(ANKI_CONNECT_URL, json=create_payload).json()
        if create_response.get("error"):
            print("Error creating model in Anki:", create_response["error"])
        else:
            print(f"Model '{model_name}' has been created successfully.")
    else:
        print(f"Model '{model_name}' already exists in Anki.")


def ensure_decks_exist(deck_names: set):
    """
    Checks if each deck in deck_names exists in Anki.
    If not, creates the deck via AnkiConnect.
    """
    # 1) Anki に存在するデッキ一覧を取得
    payload = {"action": "deckNames", "version": 6}
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    if response.get("error"):
        print("Error retrieving deck names from Anki:", response["error"])
        return

    existing_decks = set(response.get("result", []))
    print("Existing Anki decks:", existing_decks)

    # 2) デッキがなければ createDeck で作成
    for deck_name in deck_names:
        if deck_name not in existing_decks:
            print(f"Deck '{deck_name}' not found. Creating it in Anki...")
            create_payload = {
                "action": "createDeck",
                "version": 6,
                "params": {
                    "deck": deck_name
                }
            }
            create_response = requests.post(ANKI_CONNECT_URL, json=create_payload).json()
            if create_response.get("error"):
                print("Error creating deck in Anki:", create_response["error"])
            else:
                print(f"Deck '{deck_name}' has been created successfully.")


def import_to_anki(json_file_path):
    """
    Reads the specified JSON (exported from Mochi Cards),
    and imports the data into Anki via AnkiConnect.
    Each card's 'deck-name' becomes the Anki deck name.
    'name' is Front, 'content' is Back, as a basic example.
    """
    # モデルがなければ作成
    ensure_basic_model()

    with open(json_file_path, "r", encoding="utf-8") as f:
        mochi_cards = json.load(f)

    # まずは必要なデッキ名を全取得
    deck_names_needed = set(card.get("deck-name", "Mochi Imported") for card in mochi_cards)
    # デッキがなければ作成
    ensure_decks_exist(deck_names_needed)

    # Ankiに追加するノート群を作成
    notes_for_anki = []
    for card in mochi_cards:
        deck_name = card.get("deck-name", "Mochi Imported")
        front_text = card.get("name", "")
        back_text = card.get("content", "")

        note = {
            "deckName": deck_name,    # createDeck で作成済みならエラーにならない
            "modelName": DEFAULT_MODEL_NAME,
            "fields": {
                "Front": front_text,
                "Back": back_text
            },
            "tags": ["mochiImport"]
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
        if result.get("error"):
            print("AnkiConnect error:", result["error"])
        else:
            print("AnkiConnect success:", result["result"])
    except requests.exceptions.RequestException as e:
        print("Failed to send notes to Anki:", e)
