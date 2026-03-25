import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV','production')
    FLASK_PORT = int(os.getenv('FLASK_PORT',5000))
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB = os.getenv('MONGO_DB')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
