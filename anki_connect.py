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
    Imports cards from a JSON file into Anki, using the "Basic" model.
    """
    MODEL_NAME = "Basic"

    with open(json_file_path, "r", encoding="utf-8") as f:
        mochi_cards = json.load(f)

        notes = []
        for card in mochi_cards:
            front_text = card.get("name", "").split("\n---\n")[
                0
            ]  # 安全に最初の要素を取得
            back_parts = card.get("content", "").split("\n---\n")  # 分割してリスト取得
            back_text = (
                back_parts[1] if len(back_parts) > 1 else "(No content)"
            )  # 安全に2番目を取得

            notes.append(
                {
                    "deckName": card.get("deck-name", "Default"),
                    "modelName": MODEL_NAME,
                    "fields": {"Front": front_text, "Back": back_text},
                    "tags": ["mochiImport"],
                }
            )

    can_add_payload = {
        "action": "canAddNotes",
        "version": 6,
        "params": {"notes": notes},
    }
    can_add_result = (
        requests.post(ANKI_CONNECT_URL, json=can_add_payload).json().get("result", [])
    )
    filtered_notes = [note for note, can_add in zip(notes, can_add_result) if can_add]

    if filtered_notes:
        add_payload = {
            "action": "addNotes",
            "version": 6,
            "params": {"notes": filtered_notes},
        }
        requests.post(ANKI_CONNECT_URL, json=add_payload)
