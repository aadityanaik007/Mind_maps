from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
host = os.getenv("MONGO_HOST", "localhost")
port = os.getenv("MONGO_PORT", "27017")
db_name = os.getenv("MONGO_DB_NAME", "financial_data")

MONGO_URI = f"mongodb://{user}:{password}@{host}:{port}"
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[db_name]
