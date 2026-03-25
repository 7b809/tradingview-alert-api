import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = "trading"
    COLLECTION_NAME = "alerts"
    FLASK_PORT = 5000
    PAGE_SIZE = 25