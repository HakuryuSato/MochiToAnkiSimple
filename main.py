import asyncio

from mochi_to_anki_simple.get_decks import get_deck_list
from mochi_to_anki_simple.get_all_cards import get_all_cards_async, get_cards_by_deck

def main():
    """Main entry point."""
    try:
        # Get the deck list
        print("Retrieving deck list...")
        decks = get_deck_list()

        if not decks:
            print("No decks found.")
            return

        # Get all cards asynchronously
        all_cards = asyncio.run(get_all_cards_async())

        # Display deck list
        print("Deck list:")
        for idx, deck in enumerate(decks):
            print(f"{idx + 1}: {deck['name']} (ID: {deck['id']})")

        # Retrieve and display cards for each deck
        for deck in decks:
            print(f"\nRetrieving cards from deck '{deck['name']}'...")
            cards = get_cards_by_deck(deck["id"], all_cards)

            if not cards:
                print(f"Deck '{deck['name']}' has no cards. Moving to the next deck.")
                continue

            for card in cards:
                
                print(card)

    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    main()
