"""Configuration settings for the Mochi to Anki converter."""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("MOCHI_API_KEY")
if not API_KEY:
    raise ValueError("API key is not set. Please check your .env file.")

# Mochi API settings
MOCHI_API_BASE_URL = "https://app.mochi.cards/api"

# AnkiConnect settings
ANKI_CONNECT_URL = "http://localhost:8765"
DEFAULT_MODEL_NAME = "Basic"
