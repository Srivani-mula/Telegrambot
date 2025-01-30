import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# MongoDB connection details
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Encode MongoDB credentials safely
ENCODED_USERNAME = quote_plus(MONGO_USERNAME)
ENCODED_PASSWORD = quote_plus(MONGO_PASSWORD)

# MongoDB URI string
MONGO_URI = f"mongodb+srv://{ENCODED_USERNAME}:{ENCODED_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=TelegramBot"

# Telegram Bot Token (Make sure to also store this securely in .env)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Gemini API Key (Stored in .env)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')  # Store SerpAPI key the same way



