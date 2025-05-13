from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import db
from datetime import datetime, timedelta
from config import Config

LOG_CHANNEL_ID = Config.LOG_CHANNEL_ID
ADMINS = Config.ADMINS


@Client.on_message(filters.command("buy") & filters.private)
async def buy_plan(client, message: Message):
    buttons = [
        [InlineKeyboardButton("💎 Weekly ₹50", callback_data="plan_week")],
        [InlineKeyboardButton("👑 Monthly ₹100", callback_data="plan_month")]
    ]
    await message.reply_text(
        "🎁 <b>Choose your premium plan:</b>\n\n"
        "💎 <b>Weekly</b>: ₹50 (7 days)\n"
        "👑 <b>Monthly</b>: ₹100 (30 days)\n\n"
        "📸 After payment, send a screenshot and use /paydone\n"
        "💳 UPI: <code>yourupi@paytm</code>\n\n"
        "Scan this QR for faster payment 👇",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )

    # Replace this with local file or File ID for QR code
    await client.send_photo(message.chat.id, photo="your_local_qr.png")


@Client.on_callback_query(filters.regex("plan_"))
async def select_plan(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    plan_type = callback_query.data

    if "week" in plan_type:
        days = 7
        plan_name = "💎 Weekly ₹50"
    else:
        days = 30
        plan_name = "👑 Monthly ₹100"

    await db.col.update_one(
        {"id": user_id},
        {"$set": {"selected_plan": {"name": plan_name, "days": days}}},
        upsert=True
    )

    await callback_query.message.edit_text(
        f"✅ You selected: <b>{plan_name}</b>\n\n"
        "📸 Now send your payment screenshot and use /paydone.",
        parse_mode="html"
    )


@Client.on_message(filters.command("paydone") & filters.private)
async def pay_done(client, message: Message):
    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "N/A"

    # Get selected plan
    user_data = await db.col.find_one({"id": user_id})
    selected_plan = user_data.get("selected_plan", {})
    plan_name = selected_plan.get("name", "Not Selected")
    plan_days = selected_plan.get("days", "N/A")

    # Get file from message, document, or reply
    file = None
    if message.photo:
        file = message.photo.file_id
    elif message.document and message.document.mime_type.startswith("image/"):
        file = message.document.file_id
    elif message.reply_to_message:
        reply = message.reply_to_message
        if reply.photo:
            file = reply.photo.file_id
        elif reply.document and reply.document.mime_type.startswith("image/"):
            file = reply.document.file_id

    if not file:
        return await message.reply("📸 Please send or reply to a screenshot and use /paydone again.")

    await message.reply("✅ Payment proof submitted!\nWe'll verify and activate your premium shortly.")

    # Send to log channel
    await client.send_photo(
        chat_id=LOG_CHANNEL_ID,
        photo=file,
        caption=(
            f"<b>💳 New Payment Proof Submitted!</b>\n\n"
            f"<b>👤 User:</b> <a href='tg://user?id={user_id}'>{user.first_name}</a>\n"
            f"<b>🆔 ID:</b> <code>{user_id}</code>\n"
            f"<b>🔗 Username:</b> {username}\n"
            f"<b>💰 Plan:</b> {plan_name} ({plan_days} days)\n\n"
            f"🛠️ Approve with:\n"
            f"<code>/approve {user_id} {plan_days}</code>"
        ),
        parse_mode="HTML"
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
                },
                "selected_plan": None  # clear selected plan
            }},
            upsert=True
        )

        await message.reply(f"✅ Approved <code>{uid}</code> for {days} days. Expires: <b>{expires.date()}</b>", parse_mode="html")

        try:
            await client.send_message(
                uid,
                f"🎉 <b>Your premium is now active!</b>\n"
                f"✅ Valid for <b>{days}</b> days.\n"
                f"📅 Expires on: <code>{expires.date()}</code>",
                parse_mode="html"
            )
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
