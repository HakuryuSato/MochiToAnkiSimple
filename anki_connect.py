"""
Module for interacting with AnkiConnect.
"""

import json
import requests
from config import ANKI_CONNECT_URL


def ensure_decks_exist(deck_names: set):
    """
    Ensures specified decks exist in Anki, creating them if necessary.
    """
    payload = {"action": "deckNames", "version": 6}
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    existing_decks = set(response.get("result", []))
    for deck_name in deck_names - existing_decks:
        create_payload = {
            "action": "createDeck",
            "version": 6,
            "params": {"deck": deck_name},
        }
        requests.post(ANKI_CONNECT_URL, json=create_payload)


def import_to_anki(json_file_path):
    """
    Imports cards from a JSON file into Anki, skipping if the card already
    exists or if adding fails. Uses the Basic model by default.
    """
    MODEL_NAME = "Basic"

    with open(json_file_path, "r", encoding="utf-8") as f:
        mochi_cards = json.load(f)

    notes = []
    for card in mochi_cards:

        content = card.get("content", "")
        parts = content.split("\n---\n")

        front_text = parts[0] if len(parts) > 0 else "(No content)"
        back_text = parts[1] if len(parts) > 1 else "(No content)"
        
        notes.append(
            {
                "deckName": card.get("deck-name", "Default"),
                "modelName": MODEL_NAME,
                "fields": {
                    "Front": front_text,
                    "Back": back_text
                },
                "tags": ["mochiImport"],
            }
        )

    # 1. 追加可能かどうかを一括チェック
    can_add_payload = {
        "action": "canAddNotes",
        "version": 6,
        "params": {"notes": notes},
    }
    response = requests.post(ANKI_CONNECT_URL, json=can_add_payload).json()
    can_add_result = response.get("result", [])

    # 2. 追加可能なものだけをフィルタリング
    filtered_notes = [
        note for note, can_add in zip(notes, can_add_result) if can_add
    ]

    # 3. フィルタリング後のノートを Anki に追加
    if filtered_notes:
        add_payload = {
            "action": "addNotes",
            "version": 6,
            "params": {"notes": filtered_notes},
        }
        requests.post(ANKI_CONNECT_URL, json=add_payload)
