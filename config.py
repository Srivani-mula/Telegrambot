from urllib.parse import quote_plus

# Raw credentials (Replace with actual values)
USERNAME = "Srivani1510"
PASSWORD = "15102005_SV"

# Encode credentials
ENCODED_USERNAME = quote_plus(USERNAME)
ENCODED_PASSWORD = quote_plus(PASSWORD)

# Construct the MongoDB connection string safely
MONGO_URI = f"mongodb+srv://{ENCODED_USERNAME}:{ENCODED_PASSWORD}@telegrambot.wztuk.mongodb.net/?retryWrites=true&w=majority&appName=TelegramBot"

# Database details
DB_NAME = "Srivani1510"
COLLECTION_NAME = "users"

TOKEN = "7827823463:AAECOWdTwVQGxBFtPHwFoSlTHG_EvxYqoNU"
