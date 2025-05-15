import os
from dotenv import load_dotenv

def load_config():
    """Load environment variables and return configuration."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in .env")
    return {
        "api_key": api_key,
        "data_dir": "data",
        "collection_name": "cosing_ingredients"
    }