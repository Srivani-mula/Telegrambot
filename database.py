from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from datetime import datetime

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Collections
    users_collection = db[COLLECTION_NAME]  # Users collection
    chat_collection = db["chat_history"]    # Chat history collection

    # Check if connection is successful
    if db.command("ping"):
        print("✅ Successfully connected to MongoDB!")

except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    users_collection = None
    chat_collection = None


def save_user(first_name, username, chat_id):
    """Save user data to MongoDB if not already registered"""
    if users_collection is None:
        print("❌ MongoDB connection failed. Cannot save user.")
        return False

    try:
        if users_collection.find_one({"chat_id": chat_id}) is None:
            user_data = {
                "first_name": first_name,
                "username": username,
                "chat_id": chat_id
            }
            users_collection.insert_one(user_data)
            print(f"✅ User {first_name} ({username}) registered successfully.")
            return True  # New user registered
        else:
            print(f"ℹ️ User {first_name} ({username}) is already registered.")
    except Exception as e:
        print(f"❌ Error saving user: {e}")
    
    return False  # User already exists or error occurred


def save_phone_number(chat_id, phone_number):
    """Update user's phone number if the user exists"""
    if users_collection is None:
        print("❌ MongoDB connection failed. Cannot save phone number.")
        return False

    try:
        result = users_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"phone_number": phone_number}}
        )
        if result.modified_count > 0:
            print(f"✅ Phone number updated for user with chat_id {chat_id}.")
            return True  # Successfully updated
        else:
            print(f"ℹ️ No update made. User with chat_id {chat_id} may not exist.")
    except Exception as e:
        print(f"❌ Error updating phone number: {e}")
    
    return False  # Update failed


def store_chat_history(chat_id, user_input, bot_response):
    """Store user chat history separately in a chat history collection"""
    if chat_collection is None:
        print("❌ MongoDB connection failed. Cannot save chat history.")
        return False

    try:
        chat_history = {
            "chat_id": chat_id,
            "user_input": user_input,
            "bot_response": bot_response,
            "timestamp": datetime.now()
        }
        chat_collection.insert_one(chat_history)
        print(f"✅ Chat history saved for user with chat_id {chat_id}.")
        return True
    except Exception as e:
        print(f"❌ Error saving chat history: {e}")
    
    return False  # Failed to save chat history



def store_file_metadata(chat_id, file_type, file_name, analysis):
    """Store metadata of received files in MongoDB"""
    if users_collection is None:
        print("❌ MongoDB connection failed. Cannot store file metadata.")
        return False

    try:
        file_metadata = {
            "chat_id": chat_id,
            "file_type": file_type,
            "file_name": file_name,
            "analysis": analysis,
            "timestamp": datetime.now()
        }
        users_collection.insert_one(file_metadata)
        print(f"✅ File metadata stored successfully for chat_id {chat_id}.")
        return True
    except Exception as e:
        print(f"❌ Error storing file metadata: {e}")
        return False

