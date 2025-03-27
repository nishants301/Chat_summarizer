import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def get_db():
    try:
        client = MongoClient(MONGO_DB_URI,)
        db = client[DB_NAME]
        chat_data = db[COLLECTION_NAME]
        return chat_data
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
