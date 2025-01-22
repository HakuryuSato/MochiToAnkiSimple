"""Main module for the Mochi to Anki converter."""

import asyncio
import requests
from get_all_mochi_cards import get_deck_list, get_all_cards_async
from export_json import create_json_filename, write_cards_to_json
from export_deck_csv import export_deck_csv
from import_to_anki import import_with_anki_connect


def main():
    """Main function to orchestrate the Mochi to Anki conversion process."""
    try:
        # print("Retrieving deck list from Mochi...")
        # decks = get_deck_list()

        # if not decks:
        #     print("No decks found in Mochi.")
        #     return

        # # Retrieve all cards asynchronously
        # print("Retrieving card list from Mochi...")
        # all_cards = asyncio.run(get_all_cards_async())
        # if not all_cards:
        #     print("No cards found at all.")
        #     return

        # # JSONファイル名を作成して書き出し
        # json_file_name = create_json_filename()
        # write_cards_to_json(json_file_name, decks, all_cards)

        json_file_name = "output/mochi_cards_full_data_202501212349.json"
        export_deck_csv(json_file_name)

        deck_directory = "output/deck"
        import_with_anki_connect(deck_directory, model_name="mochi_cards")

    except requests.exceptions.RequestException as e:
        print(f"An error has occurred while fetching from Mochi: {e}")


if __name__ == "__main__":
    main()
