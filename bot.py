import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from database import save_user, save_phone_number, users_collection  # Import users_collection for validation

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.from_user.first_name
    username = message.from_user.username
    chat_id = message.chat.id

    # Ensure MongoDB connection is valid before saving
    if users_collection is not None:
        if save_user(first_name, username, chat_id):
            bot.send_message(chat_id, "You have been registered successfully!")
            request_phone_number(chat_id)  # After successful registration, request phone number
        else:
            bot.send_message(chat_id, "You are already registered.")
    else:
        bot.send_message(chat_id, "Database connection error. Please try again later.")

def request_phone_number(chat_id):
    """Requests user's phone number using Telegram's contact button"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_button = KeyboardButton("📞 Share My Number", request_contact=True)
    markup.add(phone_button)
    bot.send_message(chat_id, "Click the button below to share your phone number:", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Handles the phone number received from the user"""
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    if save_phone_number(chat_id, phone_number):
        bot.send_message(chat_id, "✅ Phone number saved successfully!")
    else:
        bot.send_message(chat_id, "❌ Error saving phone number. Please try again.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
