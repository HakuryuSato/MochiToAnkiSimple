from .config import MOCHI_API_BASE_URL
from .auth import get_requests_auth
from .api import sync_get

def get_deck_list():
    """Get the list of decks."""
    url = f"{MOCHI_API_BASE_URL}/decks"
    data = sync_get(url, get_requests_auth())
    return data.get("docs", [])
