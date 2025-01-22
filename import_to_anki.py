import os
import requests

def import_with_anki_connect(deck_directory: str, model_name: str = "mochi_cards") -> None:
    if not os.path.exists(deck_directory):
        print(f"[ERROR] Directory not found: {deck_directory}")
        return

    for file_name in os.listdir(deck_directory):
        if not file_name.endswith(".csv"):
            continue

        deck_name = os.path.splitext(file_name)[0]
        file_path = os.path.join(deck_directory, file_name)

        notes = []
        with open(file_path, "r", encoding="utf-8") as f:
            next(f)  # Skip header
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
                    "tags": []
                }
                notes.append(note)

        if not notes:
            print(f"[INFO] No valid notes found in {file_name}, skipping.")
            continue

        # バッチ処理: 20件ずつインポート
        for i in range(0, len(notes), 20):
            batch = notes[i:i+20]
            payload = {
                "action": "addNotes",
                "version": 6,
                "params": {"notes": batch}
            }
            try:
                response = requests.post("http://127.0.0.1:8765", json=payload).json()
                if response.get("error"):
                    print(f"[ERROR] Failed to import batch in deck '{deck_name}': {response['error']}")
                else:
                    print(f"[INFO] Imported {len(batch)} notes into deck '{deck_name}'.")
            except Exception as e:
                print(f"[ERROR] Failed to import batch in deck '{deck_name}': {e}")
