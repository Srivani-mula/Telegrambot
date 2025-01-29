from pymongo import MongoClient

# Your connection string
connection_string = "mongodb+srv://srivanimula1510:G4sF3grvAlivrJ15@telegrambot.wztuk.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(connection_string)
    # List databases to check connection
    print("Databases:", client.list_database_names())
    print("Connection successful!")
except Exception as e:
    print("Error:", e)
