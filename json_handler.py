"""Module for handling JSON file operations."""

import json
import datetime


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
        json.dump(all_cards, json_file, ensure_ascii=False, indent=2)

    print(f"\nJSON file '{file_name}' has been created successfully.")
