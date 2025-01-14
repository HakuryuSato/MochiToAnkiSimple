import aiohttp
from .auth import get_aiohttp_auth
from .config import MOCHI_API_BASE_URL
from .api import async_get

async def get_all_cards_async():
    """Get all cards asynchronously."""
    url = f"{MOCHI_API_BASE_URL}/cards"
    all_cards = []
    limit = 100
    bookmark = None
    seen_bookmarks = set()

    async with aiohttp.ClientSession(auth=get_aiohttp_auth()) as session:
        while True:
            params = {"limit": limit}
            if bookmark:
                params["bookmark"] = bookmark

            data = await async_get(session, url, params=params)
            cards = data.get("docs", [])
            all_cards.extend(cards)

            bookmark = data.get("bookmark")
            print(bookmark)

            if not bookmark or bookmark in seen_bookmarks:
                print("complete get_all_cards_async()")
                break

            seen_bookmarks.add(bookmark)

    return all_cards

def get_cards_by_deck(deck_id, all_cards):
    """Get cards by deck ID."""
    all_cards_copy = all_cards[:]
    return [card for card in all_cards_copy if card.get("deck-id") == deck_id]
