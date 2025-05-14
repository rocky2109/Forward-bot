from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import db
from datetime import datetime, timedelta
from config import Config
import script

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
        [InlineKeyboardButton("✅ I Paid", callback_data="paydone")],
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
        
    )
    await callback_query.message.delete()


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

    # Get file from msg or reply
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
        
    )

@Client.on_message(filters.command("approve") & filters.user(ADMINS))
async def approve_plan(client, message: Message):
    try:
        _, uid, days = message.text.split()
        uid = int(uid)
        days = int(days)
        expires = datetime.utcnow() + timedelta(days=days)

        # ✅ Update premium status
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

        # ✅ Confirm to admin
        await message.reply(
            f"✅ Approved {uid} for {days} days.\nExpires on: {expires.date()}"
        )

        # ✅ Notify user
        try:
            await client.send_message(
                uid,
                f"🎉 Your premium is now active!\n"
                f"✅ Valid for {days} days.\n"
                f"📅 Expires on: {expires.date()}"
            )
        except:
            pass

        # ✅ Optional: send confirmation to another log channel (if any)
        user = await client.get_users(uid)
        username = f"@{user.username}" if user.username else "N/A"

        await client.send_message(
            Config.PREMIUM_LOG_CHANNEL,
            f"🌟 New Premium Approved\n\n"
            f"👤 User: {user.first_name}\n"
            f"🆔 ID: {uid}\n"
            f"🔗 Username: {username}\n"
            f"💰 Plan: {days} days\n"
            f"📅 Expires: {expires.date()}"
        )

    except Exception as e:
        await message.reply(
            f"❌ Usage: /approve <user_id> <days>\nError: {e}"
        )

@Client.on_message(filters.command(["revoke", "remove"]) & filters.user(ADMINS))
async def revoke_premium(client, message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2:
        return await message.reply("❌ Usage: /revoke <user_id>")

    try:
        uid = int(parts[1])

        # Remove premium and plan info
        await db.col.update_one(
            {"id": uid},
            {"$unset": {"premium": "", "selected_plan": ""}}
        )

        await message.reply(
            f"🗑️ Premium access removed for user <code>{uid}</code>.",
            
        )

        try:
            await client.send_message(
                uid,
                "⚠️ Your premium plan has been revoked by an admin. Contact support if this is a mistake."
            )
        except:
            pass

    except Exception as e:
        await message.reply(f"❌ Failed to revoke: {e}")
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

@Client.on_message(filters.command("premiumusers") & filters.user(ADMINS))
async def list_premium_users(client, message: Message):
    users_cursor = db.col.find({
        "premium.is_active": True
    })

    msg_lines = []
    count = 0

    async for user in users_cursor:
        uid = user.get("id")
        name = user.get("name", "NoName")
        expires_str = user.get("premium", {}).get("expires_on")

        if not expires_str:
            continue

        try:
            expires = datetime.fromisoformat(expires_str)
            days_left = (expires - datetime.utcnow()).days
            status = f"{days_left} days left"
        except Exception as e:
            status = "❓ Unknown"

        msg_lines.append(f"👤 <b>{name}</b> | <code>{uid}</code>\n📅 {status} | Expires: <code>{expires.date()}</code>\n")
        count += 1

        if count >= 40:
            break  # Avoid flooding Telegram

    if not msg_lines:
        return await message.reply("❌ No active premium users found.")

    text = f"💎 <b>Active Premium Users</b> ({count}):\n\n" + "\n".join(msg_lines)
    await message.reply(text, disable_web_page_preview=True)
    
@Client.on_callback_query(filters.regex("start"))
async def go_home(client, callback_query: CallbackQuery):
    user = callback_query.from_user
    await callback_query.message.edit_text(
        text=Script.START_TXT.format(user.mention),
        reply_markup=InlineKeyboardMarkup(main_buttons),
        parse_mode="HTML"
    )
