import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import aiohttp
import asyncio

# Get the API key
load_dotenv()
API_KEY = os.getenv("MOCHI_API_KEY")

if not API_KEY:
    raise ValueError("API key is not set. Please check your .env file.")

MOCHI_API_BASE_URL = "https://app.mochi.cards/api"

auth = HTTPBasicAuth(API_KEY, "")


# Function to send get card request(limit:~100)
async def fetch_cards(session, url, params):
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


# Function to get all cards
async def get_all_cards_async():
    url = f"{MOCHI_API_BASE_URL}/cards"
    all_cards = []
    limit = 100
    bookmark = None
    seen_bookmarks = set()

    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(API_KEY, "")) as session:
        while True:
            params = (
                {"limit": limit, "bookmark": bookmark} if bookmark else {"limit": limit}
            )
            data = await fetch_cards(session, url, params)
            cards = data.get("docs", [])
            all_cards.extend(cards)
            bookmark = data.get("bookmark")
            print(bookmark)

            if (not bookmark) or (bookmark in seen_bookmarks):
                print("complete get_all_cards_async()")
                break

            bookmark = data.get("bookmark")
            seen_bookmarks.add(bookmark)

    return all_cards


# Function to filter cards by deck ID
def get_cards_by_deck(deck_id, all_cards):
    all_cards_copy = all_cards[:]
    return [card for card in all_cards_copy if card.get("deck-id") == deck_id]


# Function to get the deck list
def get_deck_list():
    url = f"{MOCHI_API_BASE_URL}/decks"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    data = response.json()
    return data.get("docs", [])


def main():
    try:
        # Get the deck list
        print("Retrieving deck list...")
        decks = get_deck_list()

        if not decks:
            print("No decks found.")
            return

        # Get all cards
        all_cards = asyncio.run(get_all_cards_async())

        # Display deck list
        print("Deck list:")
        for idx, deck in enumerate(decks):
            print(f"{idx + 1}: {deck['name']} (ID: {deck['id']})")

        for deck in decks:
            print(f"\nRetrieving cards from deck '{deck['name']}'...")
            cards = get_cards_by_deck(deck["id"], all_cards)

            if not cards:
                print(f"Deck '{deck['name']}' has no cards. Moving to the next deck.")
                continue

            for card in cards:
                
                print(card)

    except requests.exceptions.RequestException as e:
        print(f"An error has occurred: {e}")


if __name__ == "__main__":
    main()
