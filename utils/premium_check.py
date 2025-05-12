# utils/premium_check.py

from database import db
from datetime import datetime

async def is_premium(user_id: int) -> bool:
    user = await db.col.find_one({"id": user_id})
    if not user:
        return False
    premium = user.get("premium", {})
    if premium.get("is_active", False):
        try:
            expires = datetime.fromisoformat(premium["expires_on"])
            return datetime.utcnow() < expires
        except:
            return False
    return False
