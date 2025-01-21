import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import csv
import json
import datetime

# ---------------------------------------------------------
# Environment loading and global settings
# ---------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("MOCHI_API_KEY")

if not API_KEY:
    raise ValueError("API key is not set. Please check your .env file.")

MOCHI_API_BASE_URL = "https://app.mochi.cards/api"


# ---------------------------------------------------------
# Async function to fetch card data from the API
# ---------------------------------------------------------
async def fetch_cards(session, url, params):
    """
    Fetches a batch of cards from the Mochi Cards API using aiohttp.
    Raises an exception if the response status is not successful.
    """
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


# ---------------------------------------------------------
# Async function to retrieve all cards
# ---------------------------------------------------------
async def get_all_cards_async():
    """
    Retrieves all cards from the Mochi Cards API by following bookmark pagination.
    Returns a list of card dictionaries.
    """
    url = f"{MOCHI_API_BASE_URL}/cards"
    all_cards = []
    limit = 100
    bookmark = None
    seen_bookmarks = set()

    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(API_KEY, "")) as session:
        while True:
            params = {"limit": limit}
            if bookmark:
                params["bookmark"] = bookmark

            data = await fetch_cards(session, url, params)
            cards = data.get("docs", [])
            all_cards.extend(cards)

            # Print bookmark for debugging; remove or comment out if not needed
            bookmark = data.get("bookmark")
            print(bookmark)

            # If there's no bookmark or we've seen it before, break the loop
            if (not bookmark) or (bookmark in seen_bookmarks):
                print("complete get_all_cards_async()")
                break
            seen_bookmarks.add(bookmark)

    return all_cards


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------
def get_deck_list():
    """
    Retrieves a list of decks from the Mochi Cards API.
    Returns a list of deck dictionaries.
    """
    url = f"{MOCHI_API_BASE_URL}/decks"
    auth = HTTPBasicAuth(API_KEY, "")
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    data = response.json()
    return data.get("docs", [])


def get_cards_by_deck(deck_id, all_cards):
    """
    Filters a list of cards by a given deck ID.
    Returns only the cards belonging to that deck.
    """
    return [card for card in all_cards if card.get("deck-id") == deck_id]


def gather_all_fieldnames(all_cards):
    """
    Gathers all unique keys from the entire list of cards.
    Returns a sorted list of unique field names.
    """
    fieldnames_set = set()
    for card in all_cards:
        fieldnames_set.update(card.keys())
    return sorted(list(fieldnames_set))


def create_csv_filename(prefix="mochi_cards_full_data"):
    """
    Creates a CSV filename with the current date-time appended.
    """
    now_str = datetime.datetime.now().strftime('%Y%m%d%H%M')
    return f"{prefix}_{now_str}.csv"


def write_cards_to_csv(file_name, decks, all_cards, fieldnames):
    """
    Writes card data to a CSV file given the file name, 
    a list of decks, all cards, and the fieldnames (column headers).
    """
    with open(file_name, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for deck in decks:
            print(f"\nRetrieving cards from deck '{deck['name']}'...")
            cards_in_deck = get_cards_by_deck(deck["id"], all_cards)

            if not cards_in_deck:
                print(f"Deck '{deck['name']}' has no cards. Moving to the next deck.")
                continue

            for card in cards_in_deck:
                # Prepare a row dictionary that includes every field from fieldnames
                row = {}
                for field in fieldnames:
                    value = card.get(field, "")
                    # If the value is nested (dict or list), convert it to JSON string
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, ensure_ascii=False)
                    row[field] = value

                writer.writerow(row)
    print(f"\nCSV file '{file_name}' has been created successfully.")


# ---------------------------------------------------------
# Main function
# ---------------------------------------------------------
def main():
    try:
        print("Retrieving deck list...")
        decks = get_deck_list()

        if not decks:
            print("No decks found.")
            return

        # Retrieve all cards asynchronously
        all_cards = asyncio.run(get_all_cards_async())

        if not all_cards:
            print("No cards found at all.")
            return

        # Gather all unique fieldnames from all cards
        fieldnames = gather_all_fieldnames(all_cards)

        # Create a CSV filename
        filename = create_csv_filename()

        # Print the deck list for reference
        print("\nDeck list:")
        for idx, deck in enumerate(decks):
            print(f"{idx + 1}: {deck['name']} (ID: {deck['id']})")

        # Write cards to CSV
        write_cards_to_csv(filename, decks, all_cards, fieldnames)

    except requests.exceptions.RequestException as e:
        print(f"An error has occurred: {e}")


if __name__ == "__main__":
    main()
