from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import db
from datetime import datetime, timedelta
from config import Config
from plugins.start import Script, main_buttons

LOG_CHANNEL_ID = Config.LOG_CHANNEL_ID
ADMINS = Config.ADMINS

# 🔹 Reusable: Plan buttons
async def send_plan_options(client, message):
    buttons = [
        [
            InlineKeyboardButton("🕐 1 Day ₹15", callback_data="plan_day"),
            InlineKeyboardButton("💎 Weekly ₹50", callback_data="plan_week")
        ],
        [InlineKeyboardButton("👑 Monthly ₹100", callback_data="plan_month")],
        [InlineKeyboardButton("🏠 Home", callback_data="start")]
    ]
    await message.reply_text(
        "💰 <b>Select a Premium Plan:</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )


@Client.on_message(filters.command("buy") & filters.private)
async def buy_plan(client, message: Message):
    await send_plan_options(client, message)


@Client.on_callback_query(filters.regex("buy_again"))
async def change_plan(client, callback_query: CallbackQuery):
    await send_plan_options(client, callback_query.message)
    await callback_query.message.delete()


@Client.on_callback_query(filters.regex("plan_"))
async def select_plan(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    plan_type = callback_query.data

    if "day" in plan_type:
        days = 1
        plan_name = "🕐 1 Day ₹15"
        qr_image_path = "images/1day.jpg"
    elif "week" in plan_type:
        days = 7
        plan_name = "💎 Weekly ₹50"
        qr_image_path = "images/1week.jpg"
    else:
        days = 30
        plan_name = "👑 Monthly ₹100"
        qr_image_path = "images/1month.jpg"

    await db.col.update_one(
        {"id": user_id},
        {"$set": {
            "selected_plan": {"name": plan_name, "days": days},
            "awaiting_screenshot": True
        }},
        upsert=True
    )

    buttons = [
        [InlineKeyboardButton("✅ I Paid", callback_data="i_paid")],
        [InlineKeyboardButton("🔁 Change Plan", callback_data="buy_again")],
        [InlineKeyboardButton("🏠 Home", callback_data="start")]
    ]

    await callback_query.message.reply_photo(
        photo=qr_image_path,
        caption=(
            f"✅ <b>You selected:</b> <code>{plan_name}</code>\n\n"
            f"💳 <b>Pay to UPI:</b> <code>yourupi@paytm</code>\n"
            f"📸 After payment, send screenshot below 👇"
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )
    await callback_query.message.delete()


@Client.on_callback_query(filters.regex("i_paid"))
async def i_paid_clicked(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    await callback_query.message.edit_text(
        "📸 Now send your payment screenshot (photo or image doc).\n"
        "We will verify and approve your plan manually.",
        parse_mode="HTML"
    )

    await db.col.update_one(
        {"id": user_id},
        {"$set": {"awaiting_screenshot": True}}
    )


@Client.on_message(filters.private & (filters.photo | filters.document))
async def handle_payment_screenshot(client, message: Message):
    user_id = message.from_user.id
    user_data = await db.col.find_one({"id": user_id})

    if not user_data or not user_data.get("awaiting_screenshot"):
        return

    file = None
    if message.photo:
        file = message.photo.file_id
    elif message.document and message.document.mime_type.startswith("image/"):
        file = message.document.file_id

    if not file:
        return await message.reply("❌ Please send a valid image (photo or document).")

    plan_name = user_data.get("selected_plan", {}).get("name", "Not Selected")
    plan_days = user_data.get("selected_plan", {}).get("days", "N/A")
    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"

    await client.send_photo(
        chat_id=LOG_CHANNEL_ID,
        photo=file,
        caption=(
            f"<b>💳 New Payment Proof Submitted!</b>\n\n"
            f"<b>👤 User:</b> <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>\n"
            f"<b>🆔 ID:</b> <code>{user_id}</code>\n"
            f"<b>🔗 Username:</b> {username}\n"
            f"<b>💰 Plan:</b> {plan_name} ({plan_days} days)\n\n"
            f"🛠️ Approve with:\n"
            f"<code>/approve {user_id} {plan_days}</code>"
        ),
        parse_mode="HTML"
    )

    await db.col.update_one(
        {"id": user_id},
        {"$unset": {"awaiting_screenshot": ""}}
    )
    await message.reply("✅ Payment proof received!\nWe'll verify and activate your premium shortly.")


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
                "selected_plan": None
            }},
            upsert=True
        )

        await message.reply(
            f"✅ Approved <code>{uid}</code> for {days} days.\n📅 Expires on: <b>{expires.date()}</b>",
            parse_mode="HTML"
        )

        try:
            await client.send_message(
                uid,
                f"🎉 <b>Your premium is now active!</b>\n"
                f"✅ Valid for <b>{days}</b> days.\n"
                f"📅 Expires on: <code>{expires.date()}</code>",
                parse_mode="HTML"
            )
        except:
            pass

    except:
        await message.reply("❌ Usage: /approve <user_id> <days>")


@Client.on_message(filters.command("revoke") & filters.user(ADMINS))
async def revoke_plan(client, message: Message):
    try:
        _, uid = message.text.split()
        uid = int(uid)

        await db.col.update_one(
            {"id": uid},
            {"$unset": {"premium": "", "selected_plan": ""}}
        )

        await message.reply(f"🗑️ Premium access revoked for user <code>{uid}</code>.", parse_mode="HTML")

        try:
            await client.send_message(uid, "⚠️ Your premium plan has been revoked by admin.")
        except:
            pass

    except:
        await message.reply("❌ Usage: /revoke <user_id>")


@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user = await db.col.find_one({"id": message.from_user.id})
    if user and user.get("premium", {}).get("is_active", False):
        expires = datetime.fromisoformat(user["premium"]["expires_on"])
        days_left = (expires - datetime.utcnow()).days
        await message.reply_text(
            f"💎 Premium Status: ✅ Active\n📅 Expires in: {days_left} days",
            parse_mode="HTML"
        )
    else:
        await message.reply_text(
            "🔓 Premium Status: ❌ Not Active\nUse /buy to upgrade.",
            parse_mode="HTML"
        )


@Client.on_callback_query(filters.regex("start"))
async def go_home(client, callback_query: CallbackQuery):
    user = callback_query.from_user
    await callback_query.message.edit_text(
        text=Script.START_TXT.format(user.mention),
        reply_markup=InlineKeyboardMarkup(main_buttons),
        parse_mode="HTML"
    )
