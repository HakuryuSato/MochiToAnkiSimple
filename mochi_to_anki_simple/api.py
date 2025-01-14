import requests

# Synchronous GET
def sync_get(url, auth, params=None):
    """Make a synchronous GET request."""
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    return response.json()

# Asynchronous GET
async def async_get(session, url, params=None):
    """Make an asynchronous GET request."""
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()
