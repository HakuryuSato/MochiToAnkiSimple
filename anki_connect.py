import os
import sys
import json
import re
from collections import defaultdict

def replace_newlines_with_br(text: str) -> str:
    return text.replace("\n", "<br>")

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def export_to_anki_tsv(json_file_path: str) -> None:
    with open(json_file_path, "r", encoding="utf-8") as f:
        mochi_cards = json.load(f)

    print(f"[DEBUG] Loaded {len(mochi_cards)} cards from '{json_file_path}'.")
    sys.stdout.flush()

    deck_cards = defaultdict(list)
    skipped_count = 0

    for index, card in enumerate(mochi_cards):
        content_value = card.get("content", "")
        if not content_value:
            skipped_count += 1
            continue
        parts = content_value.split("\n---\n")
        front_text = parts[0] if len(parts) > 0 else "(No content)"
        back_text = parts[1] if len(parts) > 1 else "(No content)"
        front_text = replace_newlines_with_br(front_text)
        back_text = replace_newlines_with_br(back_text)
        deck_name = card.get("deck-name", "other")
        deck_cards[deck_name].append((front_text, back_text))

        if (index + 1) % 1000 == 0:
            print(f"[DEBUG] Processed {index+1} cards so far...")
            sys.stdout.flush()

    print(f"[DEBUG] Total skipped cards (empty content): {skipped_count}")
    sys.stdout.flush()

    os.makedirs("output/deck", exist_ok=True)

    print(f"[DEBUG] Writing decks to 'output/deck'...")
    sys.stdout.flush()

    for deck_name, cards in deck_cards.items():
        safe_deck_name = sanitize_filename(deck_name)
        output_path = os.path.join("output", "deck", f"{safe_deck_name}.tsv")

        print(f"[DEBUG] Start writing deck '{deck_name}' ({len(cards)} cards) to '{output_path}'")
        sys.stdout.flush()

        try:
            with open(output_path, "w", encoding="utf-8") as out:
                for front_text, back_text in cards:
                    out.write(f"{front_text}\t{back_text}\n")
        except Exception as e:
            print(f"[ERROR] Failed to write deck '{deck_name}': {e}")
            sys.stdout.flush()
            continue

        print(f"[DEBUG] Finished writing deck '{deck_name}'")
        sys.stdout.flush()

    print("[DEBUG] All decks processed successfully.")
    sys.stdout.flush()

if __name__ == "__main__":
    # テスト用の例: export_to_anki_tsv("mochi_cards.json")
    pass
