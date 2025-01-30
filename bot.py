import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from database import save_user, save_phone_number, store_chat_history, users_collection, store_file_metadata
from gemini import get_gemini_response, analyze_image_or_file, perform_web_search
import requests

bot = telebot.TeleBot(TOKEN)

# ✅ Start Command Handler
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from database import save_user, save_phone_number, store_chat_history, users_collection
from gemini import get_gemini_response, analyze_image_or_file, perform_web_search

bot = telebot.TeleBot(TOKEN)

# ✅ Handle Media (Photos & Documents)
@bot.message_handler(content_types=['photo', 'document'])
def handle_media(message):
    chat_id = message.chat.id
    file_id = None

    # Determine the file type and fetch file ID
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id  # Highest resolution photo
    elif message.content_type == 'document':
        file_id = message.document.file_id

    if file_id:
        # Get file info from Telegram
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        print(f"📂 File Path: {file_path}")  # Debugging - Print the file path

        # Telegram file URL format
        file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
        print(f"🔗 File URL: {file_url}")  # Debugging - Print the direct URL

        bot.send_message(chat_id, f"File received! \nFile Path: `{file_path}`", parse_mode="Markdown")

        # Download the file and analyze it
        download_and_analyze(file_url, chat_id)
    else:
        bot.send_message(chat_id, "⚠️ Could not retrieve file ID.")

def download_and_analyze(file_url, chat_id):
    """Download the file from Telegram and analyze it"""
    local_filename = file_url.split("/")[-1]  # Extract file name

    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(local_filename, "wb") as f:
                f.write(response.content)
            print(f"✅ File saved locally: {local_filename}")

            # Analyze the file using Gemini
            analysis = analyze_image_or_file(local_filename)
            bot.send_message(chat_id, f"📊 Analysis Result:\n{analysis}")
        else:
            bot.send_message(chat_id, "❌ Error downloading file from Telegram.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Download error: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    if users_collection is None:
        bot.send_message(chat_id, "❌ Database connection error. Please try again later.")
        return

    if save_user(first_name, username, chat_id):
        bot.send_message(chat_id, "✅ You have been registered successfully!")
        request_phone_number(chat_id)
    else:
        bot.send_message(chat_id, "ℹ️ You are already registered.")

# ✅ Handle Text Messages (Gemini AI Chat)
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    user_input = message.text

    try:
        bot_response = get_gemini_response(user_input)
        store_chat_history(chat_id, user_input, bot_response)
        bot.send_message(chat_id, bot_response)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error generating response: {str(e)}")

# ✅ Web Search Command
@bot.message_handler(commands=['websearch'])
def web_search(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔍 Please enter your search query:")

    def search_query(message):
        query = message.text.strip()  # Ensure clean input
        if query:
            results = perform_web_search(query)
            bot.send_message(chat_id, f"🌐 Here are the search results:\n\n{results}", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "⚠️ Invalid search query. Please try again.")

    bot.register_next_step_handler(message, search_query)  # Wait for user input


# ✅ Request Phone Number
def request_phone_number(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_button = KeyboardButton("📞 Share My Number", request_contact=True)
    markup.add(phone_button)
    bot.send_message(chat_id, "📲 Click the button below to share your phone number:", reply_markup=markup)

# ✅ Handle Contact Sharing
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    if save_phone_number(chat_id, phone_number):
        bot.send_message(chat_id, "✅ Phone number saved successfully!")
    else:
        bot.send_message(chat_id, "❌ Error saving phone number. Please try again.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
