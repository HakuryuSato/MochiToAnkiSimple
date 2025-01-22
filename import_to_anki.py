import os
import requests

def import_to_anki(deck_directory: str) -> None:
    model_name = "mochi_cards"
    if not create_model_if_not_exists(model_name):
        print(f"[ERROR] Cannot proceed without model '{model_name}'.")
        return
    if not os.path.exists(deck_directory):
        print(f"[ERROR] Directory not found: {deck_directory}")
        return
    all_notes = open_deck_csv_files(deck_directory, model_name)
    for deck_name, notes in all_notes.items():
        BATCH_SIZE = 50
        for i in range(0, len(notes), BATCH_SIZE):
            batch = notes[i : i + BATCH_SIZE]
            handle_import(batch, deck_name, batch_start=i)

def open_deck_csv_files(deck_directory, model_name):
    all_notes = {}
    for file_name in os.listdir(deck_directory):
        if not file_name.endswith(".csv"):
            continue
        deck_name = os.path.splitext(file_name)[0]
        if not create_deck_if_not_exists(deck_name):
            print(f"[ERROR] Cannot proceed without deck '{deck_name}'.")
            continue
        file_path = os.path.join(deck_directory, file_name)
        notes = []
        with open(file_path, "r", encoding="utf-8") as f:
            next(f)
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('","')
                if len(parts) < 2:
                    continue
                front = parts[0].strip('"')
                back = parts[1].strip('"')
                note = {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": {"Front": front, "Back": back},
                    "tags": [],
                }
                notes.append(note)
        if notes:
            all_notes[deck_name] = notes
        else:
            print(f"[INFO] No valid notes found in {file_name}, skipping.")
    return all_notes

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
                    "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
                }
            ],
        },
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
        "params": {"deck": deck_name},
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

def handle_import(items, deck_name, batch_start, is_batch=True):
    payload = create_payload("addNotes", 6, items)
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload).json()
        if response.get("error"):
            if is_batch:
                print(f"[ERROR] Failed to import batch ({batch_start + 1} to {batch_start + len(items)}) in deck '{deck_name}': {response['error']}")
                for item in items:
                    handle_import([item], deck_name, batch_start=0, is_batch=False)
            else:
                print(f"[ERROR] Failed to import note: {items[0]['fields']['Front']} - {response['error']}")
        else:
            if is_batch:
                print(f"[INFO] Successfully imported {len(items)} notes (batch {batch_start + 1} to {batch_start + len(items)}) into deck '{deck_name}'.")
            else:
                print(f"[INFO] Successfully imported note: {items[0]['fields']['Front']}")
    except Exception as e:
        if is_batch:
            print(f"[ERROR] Failed to import batch ({batch_start + 1} to {batch_start + len(items)}) in deck '{deck_name}': {e}")
        else:
            print(f"[ERROR] Failed to import note: {items[0]['fields']['Front']} - {e}")

def create_payload(action, version, notes):
    return {
        "action": action,
        "version": version,
        "params": {"notes": notes},
    }
