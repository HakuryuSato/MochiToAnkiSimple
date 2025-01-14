from requests.auth import HTTPBasicAuth
from aiohttp import BasicAuth
from .config import MOCHI_API_KEY

def get_requests_auth():
    """Return Requests BasicAuth."""
    return HTTPBasicAuth(MOCHI_API_KEY, "")

def get_aiohttp_auth():
    """Return Aiohttp BasicAuth."""
    return BasicAuth(MOCHI_API_KEY, "")
