# plugins/premium.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import LOG_CHANNEL_ID, ADMINS
from database import db
from datetime import datetime, timedelta


@Client.on_message(filters.command("buy") & filters.private)
async def buy_plan(client, message: Message):
    await message.reply_text(
        "💎 *Premium Plans Available:*\n\n"
        "📦 Weekly: ₹50 (7 days)\n"
        "📦 Monthly: ₹100 (30 days)\n\n"
        "Pay to UPI: `yourupi@paytm`\n"
        "📸 After payment, send a screenshot using /paydone\n\n"
        "Scan this QR for faster payment 👇", quote=True
    )
    await client.send_photo(message.chat.id, photo="https://your_qr_link_or_path.jpg")


@Client.on_message(filters.command("paydone") & filters.private)
async def pay_done(client, message: Message):
    if not message.photo:
        return await message.reply("📸 Please send a screenshot/photo of your payment!")

    await message.reply("✅ Payment proof submitted! We'll verify and approve you soon.")

    await client.send_photo(
        chat_id=LOG_CHANNEL_ID,
        photo=message.photo.file_id,
        caption=(
            f"💳 *New Payment Received!*\n\n"
            f"👤 User: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
            f"🆔 User ID: `{message.from_user.id}`\n\n"
            f"Reply to approve:\n`/approve {message.from_user.id} 7` or `/approve {message.from_user.id} 30`"
        ),
        parse_mode="Markdown"
    )


@Client.on_message(filters.command("approve") & filters.user(ADMINS))
async def approve_plan(client, message: Message):
    try:
        _, uid, days = message.text.split()
        uid = int(uid)
        days = int(days)
        expires = datetime.utcnow() + timedelta(days=days)

        await db.col.update_one(
            {"id": uid},
            {"$set": {
                "premium": {
                    "is_active": True,
                    "expires_on": expires.isoformat()
                }
            }},
            upsert=True
        )

        await message.reply(f"✅ Approved {uid} for {days} days. Expires on: {expires.date()}")

        try:
            await client.send_message(uid, f"🎉 Your premium is active until `{expires.date()}`.\nEnjoy forwarding 😈")
        except:
            pass

    except:
        await message.reply("❌ Usage: /approve <user_id> <days>")


@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user = await db.col.find_one({"id": message.from_user.id})
    if user and user.get("premium", {}).get("is_active", False):
        expires = datetime.fromisoformat(user["premium"]["expires_on"])
        days_left = (expires - datetime.utcnow()).days
        await message.reply_text(f"💎 Premium Status: ✅ Active\n📅 Expires in: {days_left} days")
    else:
        await message.reply_text("🔓 Premium Status: ❌ Not Active\nUse /buy to upgrade.")
