import os
import sys
import json
import re
from collections import defaultdict


def format_text(text: str) -> str:
    """
    テキストをフォーマットする:
    - 改行を <br> に変換
    - `,` を半角スペースに置換
    - `![...](...)` を削除
    """
    text = text.strip()
    text = text.replace("\n", "<br>")
    text = text.replace(",", " ")
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)  # `![...]` を削除
    return text.strip()


def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", filename)


def export_deck_csv(json_file_path: str) -> None:
    with open(json_file_path, "r", encoding="utf-8") as f:
        mochi_cards = json.load(f)

    print(f"[DEBUG] Loaded {len(mochi_cards)} cards from '{json_file_path}'.")
    sys.stdout.flush()

    deck_cards = defaultdict(list)
    skipped_count = 0

    for index, card in enumerate(mochi_cards):
        content_value = card.get("content", "") or card.get("fields", {}).get(
            "name", {}
        ).get("value", "")

        if not content_value:
            skipped_count += 1
            continue

        front_text, back_text = content_value.split("\n---\n")

        # format
        front_text = format_text(front_text)
        back_text = format_text(back_text)

        if not front_text or not back_text:
            skipped_count += 1
            print(
                f"[INFO] Skipping invalid card at index {index}: Front='{front_text}', Back='{back_text}'"
            )
            continue

        deck_name = card.get("deck-name", "other")
        deck_cards[deck_name].append((front_text, back_text))

    os.makedirs("output/deck", exist_ok=True)

    for deck_name, cards in deck_cards.items():
        safe_deck_name = sanitize_filename(deck_name)
        output_path = os.path.join("output", "deck", f"{safe_deck_name}.csv")

        try:
            with open(output_path, "w", encoding="utf-8", newline="") as out:
                out.write('"Front","Back"\n')
                for front_text, back_text in cards:
                    out.write(f'"{front_text}","{back_text}"\n')
        except Exception as e:
            print(f"[ERROR] Failed to write deck '{deck_name}': {e}")
            continue

        print(f"[DEBUG] Finished writing deck '{deck_name}'")

    print(f"[INFO] Skipped {skipped_count} invalid cards.")
