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
        # 1. まず content を取得
        content_value = card.get("content", "")

        # 2. content が空なら fields.name.value を使う
        if not content_value:
            fallback = card.get("fields", {}).get("name", {}).get("value", "")
            content_value = fallback

        # 3. それでも空ならスキップ
        if not content_value:
            skipped_count += 1
            continue

        # 4. 改行で Front/Back に分割
        parts = content_value.split("\n---\n")
        front_text = parts[0] if len(parts) > 0 else "(No content)"
        back_text  = parts[1] if len(parts) > 1 else "(No content)"

        # 5. 改行を <br> に変換
        front_text = replace_newlines_with_br(front_text)
        back_text  = replace_newlines_with_br(back_text)

        # 6. デッキ名を取得 (なければ "other")
        deck_name = card.get("deck-name", "other")

        deck_cards[deck_name].append((front_text, back_text))


    os.makedirs("output/deck", exist_ok=True)

    for deck_name, cards in deck_cards.items():
        safe_deck_name = sanitize_filename(deck_name)
        output_path = os.path.join("output", "deck", f"{safe_deck_name}.tsv")

        try:
            with open(output_path, "w", encoding="utf-8") as out:
                for front_text, back_text in cards:
                    out.write(f"{front_text}\t{back_text}\n")
        except Exception as e:
            print(f"[ERROR] Failed to write deck '{deck_name}': {e}")
            continue

        print(f"[DEBUG] Finished writing deck '{deck_name}'")


if __name__ == "__main__":
    pass
