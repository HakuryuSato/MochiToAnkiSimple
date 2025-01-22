"""Anki Connect importer module."""

import os
import requests


def create_model_if_not_exists(model_name: str) -> bool:
    payload_check = {"action": "modelNames", "version": 6}
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload_check).json()
        if response.get("result") and model_name in response["result"]:
            return True
    except Exception as e:
        print(f"[ERROR] Failed to fetch model names: {e}")
        return False

    payload_create = {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": model_name,
            "inOrderFields": ["Front", "Back"],
            "cardTemplates": [
                {
                    "Name": "Card 1",
                    "Front": "{{Front}}",
                    "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}"
                }
            ]
        }
    }
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload_create).json()
        if response.get("error"):
            print(f"[ERROR] Failed to create model '{model_name}': {response['error']}")
            return False
        print(f"[INFO] Model '{model_name}' created successfully.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create model '{model_name}': {e}")
        return False


def create_deck_if_not_exists(deck_name: str) -> bool:
    payload_check = {"action": "deckNames", "version": 6}
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload_check).json()
        if response.get("result") and deck_name in response["result"]:
            return True
    except Exception as e:
        print(f"[ERROR] Failed to fetch deck names: {e}")
        return False

    payload_create = {
        "action": "createDeck",
        "version": 6,
        "params": {"deck": deck_name}
    }
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload_create).json()
        if response.get("error"):
            print(f"[ERROR] Failed to create deck '{deck_name}': {response['error']}")
            return False
        print(f"[INFO] Deck '{deck_name}' created successfully.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create deck '{deck_name}': {e}")
        return False


def note_exists(front: str, model_name: str) -> bool:
    """
    指定された Front フィールドのノートが既に存在するかを確認する。
    """
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'"Front:{front}"'
        }
    }
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload).json()
        if response.get("result") and len(response["result"]) > 0:
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Failed to check for duplicate note: {e}")
        return False


def import_with_anki_connect(deck_directory: str, model_name: str = "mochi_cards") -> None:
    if not create_model_if_not_exists(model_name):
        print(f"[ERROR] Cannot proceed without model '{model_name}'.")
        return

    if not os.path.exists(deck_directory):
        print(f"[ERROR] Directory not found: {deck_directory}")
        return

    for file_name in os.listdir(deck_directory):
        if not file_name.endswith(".tsv"):
            continue

        deck_name = os.path.splitext(file_name)[0]
        if not create_deck_if_not_exists(deck_name):
            print(f"[ERROR] Cannot proceed without deck '{deck_name}'.")
            continue

        file_path = os.path.join(deck_directory, file_name)

        notes = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("\t")
                if len(parts) < 2:
                    continue
                front, back = parts[0], parts[1]

                # 重複確認
                if note_exists(front, model_name):
                    print(f"[INFO] Skipping duplicate note: {front}")
                    continue

                note = {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": {
                        "Front": front,
                        "Back":  back
                    },
                    "tags": []
                }
                notes.append(note)

        if not notes:
            print(f"[INFO] No valid notes found in {file_name}, skipping.")
            continue

        payload = {
            "action": "addNotes",
            "version": 6,
            "params": {
                "notes": notes
            }
        }

        try:
            response = requests.post("http://127.0.0.1:8765", json=payload).json()
            if response.get("error"):
                print(f"[ERROR] Failed to import '{file_name}' into deck '{deck_name}': {response['error']}")
            else:
                print(f"[INFO] Imported {len(notes)} notes into deck '{deck_name}'.")
        except Exception as e:
            print(f"[ERROR] Failed to import '{file_name}' into deck '{deck_name}': {e}")
