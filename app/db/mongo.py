from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongodb_uri)
db = client["visamitra"]

users_col = db["users"]
trackers_col = db["trackers"]
