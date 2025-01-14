import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get the API key
MOCHI_API_KEY = os.getenv("MOCHI_API_KEY")

if not MOCHI_API_KEY:
    raise ValueError("API key is not set. Please check your .env file.")

# Define the base URL for Mochi API
MOCHI_API_BASE_URL = "https://app.mochi.cards/api"
