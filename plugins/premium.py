# plugins/premium.py

from pyrogram import Client, filters
from pyrogram.types import Message
from database import db
from datetime import datetime, timedelta
from config import Config
LOG_CHANNEL_ID = Config.LOG_CHANNEL_ID
ADMINS = Config.ADMINS


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
async def pay_done(client, message):
    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "N/A"

    file = None

    # 🧠 Get image from message, document, or reply
    if message.photo:
        file = message.photo.file_id
    elif message.document and message.document.mime_type.startswith("image/"):
        file = message.document.file_id
    elif message.reply_to_message:
        if message.reply_to_message.photo:
            file = message.reply_to_message.photo.file_id
        elif message.reply_to_message.document and message.reply_to_message.document.mime_type.startswith("image/"):
            file = message.reply_to_message.document.file_id

    # ❌ If no image found
    if not file:
        return await message.reply(
            "📸 Please send your payment screenshot image (as photo or document), or reply to an image and use /paydone.",
            quote=True
        )

    await message.reply("✅ Your payment proof has been submitted!\nWe'll verify and activate your premium shortly.")

    # 🧾 Optional plan detection (if mentioned in caption)
    plan = "Unknown"
    if message.caption:
        if "week" in message.caption.lower():
            plan = "Weekly ₹50"
        elif "month" in message.caption.lower():
            plan = "Monthly ₹100"

    # 🔥 Send to LOG_CHANNEL
    await client.send_photo(
        chat_id=Config.LOG_CHANNEL_ID,
        photo=file,
        caption=(
            f"<b>💳 New Payment Proof Submitted!</b>\n\n"
            f"<b>👤 User:</b> <a href='tg://user?id={user_id}'>{user.first_name}</a>\n"
            f"<b>🆔 ID:</b> <code>{user_id}</code>\n"
            f"<b>🔗 Username:</b> {username}\n"
            f"<b>💰 Plan:</b> {plan}\n\n"
            f"🛠️ Reply with:\n"
            f"<code>/approve {user_id} 7</code> or <code>/approve {user_id} 30</code>"
        ),
        parse_mode="html"
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
