import asyncio
from datetime import datetime, timedelta
from pyrogram import Client
from config import Config
from database import db

LOG_CHANNEL = Config.LOG_CHANNEL_ID

async def check_premium_expiry(app: Client):
    while True:
        try:
            async for user in db.col.find({"premium.is_active": True}):
                user_id = user["id"]
                premium = user["premium"]
                expires_on = datetime.fromisoformat(premium["expires_on"])
                now = datetime.utcnow()
                time_left = expires_on - now

                # Notify 1 day before
                if timedelta(days=1) >= time_left > timedelta(hours=11, minutes=59):
                    try:
                        await app.send_message(
                            user_id,
                            f"⚠️ Reminder: Your premium will expire in 1 day.\n"
                            f"To extend, use /buy"
                        )
                    except: pass

                # Notify 12 hours before
                if timedelta(hours=12) >= time_left > timedelta(hours=11):
                    try:
                        await app.send_message(
                            user_id,
                            f"⚠️ Your premium will expire in 12 hours!\n"
                            f"Renew with /buy to avoid interruption."
                        )
                    except: pass

                # Expired
                if time_left.total_seconds() <= 0:
                    await db.col.update_one(
                        {"id": user_id},
                        {"$unset": {"premium": ""}}
                    )
                    try:
                        await app.send_message(
                            user_id,
                            "⛔ Your premium has expired.\nUse /buy to renew anytime!"
                        )
                    except: pass
                    try:
                        await app.send_message(
                            LOG_CHANNEL,
                            f"🔔 Premium expired for: `{user_id}`"
                        )
                    except: pass

        except Exception as e:
            print(f"[Premium Checker Error] {e}")

        await asyncio.sleep(3600)  # 🔁 Check every hour
