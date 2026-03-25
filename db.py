from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

alerts_collection = db["alerts"]
trades_collection = db["trades"]
