from pymongo import MongoClient
import os

client = None

def get_db():
    return client.get_database(os.getenv("DATABASE_NAME"))

def init_db():
    global client
    mongodb_url = os.getenv("MONGODB_URI")
    client = MongoClient(mongodb_url)