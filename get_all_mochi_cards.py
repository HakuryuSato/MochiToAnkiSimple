"""Module for interacting with the Mochi Cards API."""

import aiohttp
import requests
from requests.auth import HTTPBasicAuth
from config import API_KEY, MOCHI_API_BASE_URL


async def fetch_cards(session, url, params):
    """
    Fetches a batch of cards from the Mochi Cards API using aiohttp.
    Raises an exception if the response status is not successful.
    """
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


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

            bookmark = data.get("bookmark")
            print("Current bookmark:", bookmark)

            # ページネーションが終了したらブレイク
            if (not bookmark) or (bookmark in seen_bookmarks):
                print("complete get_all_cards_async()")
                break
            seen_bookmarks.add(bookmark)

    return all_cards


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
