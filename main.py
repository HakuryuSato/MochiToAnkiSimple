"""Main module for the Mochi to Anki converter."""

import asyncio
import requests
from get_all_mochi_cards import get_deck_list, get_all_cards_async
from export_mochi_cards_json import create_json_file, write_cards_to_json
from export_formatted_cards_csv import export_deck_csv
from import_to_anki import import_to_anki


def main():
    """Main function to orchestrate the Mochi to Anki conversion process."""
    try:
        print("Step 1: Retrieving deck list from Mochi...")
        decks = get_deck_list()
        if not decks:
            print("No decks found in Mochi. Exiting process.")
            return

        print("Step 2: Retrieving card list from Mochi...")
        all_cards = asyncio.run(get_all_cards_async())
        if not all_cards:
            print("No cards found in Mochi. Exiting process.")
            return

        print("Step 3: Writing cards to JSON file...")
        json_file_name = create_json_file()
        write_cards_to_json(json_file_name, decks, all_cards)

        print("Step 4: Exporting formatted card to CSV...")
        json_file_name = "output/mochi_cards_full_data_202501221521.json"
        export_deck_csv(json_file_name)

        print("Step 5: Importing decks into Anki...")
        deck_directory = "output/deck"
        import_to_anki(deck_directory)

        print("Process completed successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error: An issue occurred while fetching data from Mochi. Details: {e}")


if __name__ == "__main__":
    main()
