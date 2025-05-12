# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import sys 
import math
import time, re
import asyncio 
import logging
import random
from .utils import STS
from database import Db, db
from .test import CLIENT, get_client, iter_messages
from config import Config, temp
from script import Script
from pyrogram import Client, filters 
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from .db import connect_user_db
from datetime import datetime
from pyrogram.types import Message
import html
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

CLIENT = CLIENT()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
TEXT = Script.TEXT


def clean_caption(text):
    if not text:
        return text

    # Remove markdown-style links [text](url)
    text = re.sub(r'\[.*?\]\(https?://\S+\)', '', text)

    # Remove HTML-style links <a href="url">text</a>
    text = re.sub(r'<a\s+href="https?://\S+">.*?<\/a>', '', text)

    # Remove raw URLs
    text = re.sub(r'https?://\S+', '', text)

    # 🔥 Replace @mentions like @username with @PFP_HUB
    text = re.sub(r'@[\w_]+', '@PFP_HUB', text)

    return text



# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ

# List of sticker file_ids
stickers = [
    "CAACAgUAAxkBAAKdy2gAAcf9KlVk_1njqKakcNHaG7EtOAACRBIAAmA8mVZNGBPG926hPx4E",
    "CAACAgUAAxkBAAKdz2gAAcgE4TO5QkE8RBHBTPLv7vMd-gAC5RoAAkLJmVaq8bSrh4WROB4E",
    "CAACAgUAAxkBAAKd02gAAcgZI1Sb7gs6TtcfATNpKNf_DAACjhUAAluZkVblEQPllMNpDR4E",
    "CAACAgUAAxkBAAKd12gAAcgoF2NiJ4nhNX1EZ2NsYAnNzAACxBMAAt6RQFe8JuZz4R3_ux4E",
    "CAACAgUAAxkBAAKd22gAAchXSZyHvSaeVlq4CcMGqL83OgAC5RYAAjYm4VXc6YhNFogSnR4E",
    "CAACAgUAAxkBAAKd4GgAAciWWCjGlazrYHMVXH02xzNXcAACUxEAAhMa4VVI7deFYNC4Th4E",
    "CAACAgUAAxkBAAKd5GgAAcir1EfGQvmUH4_zXPgbL0edhQACexMAAtM34FUY7V72MgAByGgeBA",
    "CAACAgUAAxkBAAKd6GgAAci0juti9vuDYhAhc8fWR7shjgACsxMAAkfQ6FU5u4F1et95oR4E",
    "CAACAgUAAxkBAAKd8GgAAcjfwpi3K6fyNDknlbFacksaXQACthMAAown4FVJ6mif9n7fGB4E",
    "CAACAgUAAxkBAAKd7GgAAcjLjwVBsAq5U0idYGtXWniz0wACfhUAAkaJ4FWEbGwb66jiFh4E",
    "CAACAgUAAxkBAAKd9GgAAcjoNFzvijbzEhx37Hj24AcYUQACmRMAAsuu4FWDORc0ZFLe6h4E",
    "CAACAgUAAxkBAAKd-GgAAclduuEUSKd7q7s_9azR-QFHVAAC8hcAAmqoCVT9fir12Ia5Qh4E"
]


@Client.on_callback_query(filters.regex(r'^start_public'))
async def pub_(bot, message):
    user = message.from_user.id
    temp.CANCEL[user] = False
    frwd_id = message.data.split("_")[2]
    if temp.lock.get(user) and str(temp.lock.get(user))=="True":
      return await message.answer("please wait until previous task complete", show_alert=True)
    sts = STS(frwd_id)
    if not sts.verify():
      await message.answer("your are clicking on my old button", show_alert=True)
      return await message.message.delete()
    i = sts.get(full=True)
    if i.TO in temp.IS_FRWD_CHAT:
      return await message.answer("In Target chat a task is progressing. please wait until task complete", show_alert=True)
    m = await msg_edit(message.message, "🌚 Verifying Your Data's, Be Patience.")
    _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
    filter = datas['filters']
    max_size = datas['max_size']
    min_size = datas['min_size']
    keyword = datas['keywords']
    exten = datas['extensions']
    keywords = ""
    extensions = ""
    if keyword:
        for key in keyword:
            keywords += f"{key}|"
        keywords  = keywords.rstrip("|")
    else:
        keywords = None
    if exten:
        for ext in exten:
            extensions += f"{ext}|"
        extensions = extensions.rstrip("|")
    else:
        extensions = None
    if not _bot:
      return await msg_edit(m, "You didn't added any bot. Please add a bot using /settings !", wait=True)
    if _bot['is_bot'] == True:
        data = _bot['token']
    else:
        data = _bot['session']
    try:
      il = True if _bot['is_bot'] == True else False
      client = await get_client(data, is_bot=il)
      await client.start()
    except Exception as e:  
      return await m.edit(e)
    await msg_edit(m, "<b>Pirate Working...💀</b>")
    try: 
       await client.get_messages(sts.get("FROM"), sts.get("limit"))
    except:
       await msg_edit(m, f"**Source chat may be a private channel / group. Use userbot (user must be member over there) or  if Make Your [Bot](t.me/{_bot['username']}) an admin over there**", retry_btn(frwd_id), True)
       return await stop(client, user)
    try:
        k = await client.send_message(
           i.TO,
           "𝐅𝐨𝐫𝐰𝐚𝐫𝐝𝐢𝐧𝐠 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 🏴‍☠\n\n<b><blockquote><a href='https://t.me/Pirates_Auto_Forward_bot?start=true'>@Pirates_Auto_Forward_bot 🦜</a></blockquote></b>"
        )
        random_sticker = random.choice(stickers)
        await client.send_sticker(i.TO, random_sticker)
       
    except:
       await msg_edit(m, f"**Please Make Your [UserBot / Bot](t.me/{_bot['username']}) Admin In Target Channel With Full Permissions**", retry_btn(frwd_id), True)
       return await stop(client, user)
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if not connected:
            await msg_edit(m, "<code>Cannot Connected Your db Errors Found Dup files Have Been Skipped after Restart</code>")
        else:
            user_have_db = True
    temp.forwardings += 1
    await db.add_frwd(user)
    await send(client, user, "<b>Fᴏʀᴡᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ🔥</b>")
    sts.add(time=True)
    sleep = 1 if _bot['is_bot'] else 10
    await msg_edit(m, "<b>Pirate Working...</b>") 
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True  # ✅ correct
    dup_files = []
    if locked:
        try:
          MSG = []
          pling=0
          await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
          async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=sts.get("skip"), filters=filter, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                   if user_have_db:
                      await user_db.drop_all()
                      await user_db.close()
                   return
                if pling %20 == 0: 
                   await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
                pling += 1
                sts.add('fetched')
                if message == "DUPLICATE":
                   sts.add('duplicate')
                   continue
                elif message == "FILTERED":
                   sts.add('filtered')
                   continue 
                elif message.empty or message.service:
                   sts.add('deleted')
                   continue
                elif message.document and await extension_filter(extensions, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await keyword_filter(keywords, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await size_filter(max_size, min_size, message.document.file_size):
                   sts.add('filtered')
                   continue 
                elif message.document and message.document.file_id in dup_files:
                   sts.add('duplicate')
                   continue
                if message.document and datas['skip_duplicate']:
                    dup_files.append(message.document.file_id)
                    if user_have_db:
                        await user_db.add_file(message.document.file_id)
                if forward_tag:
                   MSG.append(message.id)
                   notcompleted = len(MSG)
                   completed = sts.get('total') - sts.get('fetched')
                   if ( notcompleted >= 100 
                        or completed <= 100): 
                      await forward(user, client, MSG, m, sts, protect)
                      sts.add('total_files', notcompleted)
                      await asyncio.sleep(10)
                      MSG = []
                else:
                   new_caption = custom_caption(message, caption)
                   details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                   await copy(user, client, details, m, sts)
                   sts.add('total_files')
                   await asyncio.sleep(sleep) 
        except Exception as e:
            await msg_edit(m, f'<b>ERROR:</b>\n<code>{e}</code>', wait=True)
            print(e)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
        temp.IS_FRWD_CHAT.remove(sts.TO)
        await send(client, user, "<b>🎉 ғᴏʀᴡᴀᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>")
        await edit(user, m, 'ᴄᴏᴍᴘʟᴇᴛᴇᴅ', "completed", sts) 
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await stop(client, user)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def copy(user, bot, msg, m, sts):
    try:
        caption = f"{msg.get('caption') or ''}"

# Current timestamp in readable format
        
# User details
        #user_info = f"""
#🆔 User ID: `{user_id}`"""



# Final caption for log post
        log_caption = caption
        # Send to TO channel
        if msg.get("media") and msg.get("caption"):
            await bot.send_cached_media(
                chat_id=sts.get('TO'),
                file_id=msg.get("media"),
                caption=caption,
                reply_markup=msg.get('button'),
                protect_content=msg.get("protect"))
            
            # ✅ Send same to log channel
            await bot.send_cached_media(
                chat_id=-1002601855166,
                file_id=msg.get("media"),
                caption=log_caption,
                reply_markup=msg.get('button'),
                protect_content=False)
        else:
            await bot.copy_message(
                chat_id=sts.get('TO'),
                from_chat_id=sts.get('FROM'),
                message_id=msg.get("msg_id"),
                caption=caption,
                reply_markup=msg.get('button'),
                protect_content=msg.get("protect"))

            # ✅ Copy to log channel
            await bot.copy_message(
                chat_id=-1002601855166,
                from_chat_id=sts.get('FROM'),
                message_id=msg.get("msg_id"),
                caption=log_caption,
                reply_markup=msg.get('button'),
                protect_content=False)
            
    except FloodWait as e:
        await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', e.value, sts)
        await asyncio.sleep(e.value)
        await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
        await copy(user, bot, msg, m, sts)

    except Exception as e:
        print(e)
        sts.add('deleted')






# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def forward(user, bot, msg_id, m, sts, protect):
    try:
        from_chat_id = sts.get('FROM')
        to_chat_id = sts.get('TO')

        # Fetch the message
        msg = await bot.get_messages(chat_id=from_chat_id, message_ids=msg_id)

        if msg.media_group_id:
            # ✅ It's an album, fetch all messages in this album
            album = await bot.get_media_group(chat_id=from_chat_id, message_ids=msg.media_group_id)

            album_msg_ids = [m.id for m in album]  # collect all message IDs

            # ✅ Forward all album messages together
            await bot.forward_messages(
                chat_id=to_chat_id,
                from_chat_id=from_chat_id,
                message_ids=album_msg_ids,
                protect_content=protect
            )

            # ✅ Forward album also to LOG CHANNEL
            await bot.forward_messages(
                chat_id=LOG_CHANNEL_ID,
                from_chat_id=from_chat_id,
                message_ids=album_msg_ids,
                protect_content=False
            )

        else:
            # ✅ If it's normal (single) message, check and clean caption if needed
            caption = msg.caption if msg.caption else None

            link_removal_enabled = await db.is_link_removal_enabled(user)
            if link_removal_enabled and caption:
                caption = clean_caption(caption)

            # Forward manually based on message type
            if msg.photo:
                await bot.send_photo(
                    chat_id=to_chat_id,
                    photo=msg.photo.file_id,
                    caption=caption,
                    protect_content=protect,
                    reply_markup=msg.reply_markup
                )
            elif msg.video:
                await bot.send_video(
                    chat_id=to_chat_id,
                    video=msg.video.file_id,
                    caption=caption,
                    protect_content=protect,
                    reply_markup=msg.reply_markup
                )
            elif msg.document:
                await bot.send_document(
                    chat_id=to_chat_id,
                    document=msg.document.file_id,
                    caption=caption,
                    protect_content=protect,
                    reply_markup=msg.reply_markup
                )
            elif msg.text:
                await bot.send_message(
                    chat_id=to_chat_id,
                    text=caption,
                    protect_content=protect,
                    reply_markup=msg.reply_markup
                )
            else:
                await bot.forward_messages(
                    chat_id=to_chat_id,
                    from_chat_id=from_chat_id,
                    message_ids=msg_id,
                    protect_content=protect
                )

            # ✅ Forward normal single message to LOG channel too
            await bot.forward_messages(
                chat_id=LOG_CHANNEL_ID,
                from_chat_id=from_chat_id,
                message_ids=msg_id,
                protect_content=False
            )

    except FloodWait as e:
        await edit(user, m, 'Processing...', e.value, sts)
        await asyncio.sleep(e.value)
        await edit(user, m, 'Processing...', 5, sts)
        await forward(user, bot, msg_id, m, sts, protect)

    except Exception as e:
        await edit(user, m, f"Error occurred: {str(e)}", 0, sts)




# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def msg_edit(msg, text, button=None, wait=None):
    try:
        return await msg.edit(text, reply_markup=button)
    except MessageNotModified:
        pass 
    except FloodWait as e:
        if wait:
           await asyncio.sleep(e.value)
           return await msg_edit(msg, text, button, wait)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
async def send_random_sticker(i):
    random_sticker = random.choice(stickers)  # Randomly pick a sticker
    await client.send_sticker(i.TO, random_sticker)  # Send the sticker to the user

async def edit(user, msg, title, status, sts):
   i = sts.get(full=True)
   status = 'Forwarding' if status == 5 else f"sleeping {status} s" if str(status).isnumeric() else status
   percentage = "{:.0f}".format(float(i.fetched)*100/float(i.total))
   text = TEXT.format(i.fetched, i.total_files, i.duplicate, i.deleted, i.skip, i.filtered, status, percentage, title)
   await update_forward(user_id=user, last_id=None, start_time=i.start, limit=i.limit, chat_id=i.FROM, toid=i.TO, forward_id=None, msg_id=msg.id, fetched=i.fetched, deleted=i.deleted, total=i.total_files, duplicate=i.duplicate, skip=i.skip, filterd=i.filtered)
   now = time.time()
   diff = int(now - i.start)
   speed = sts.divide(i.fetched, diff)
   elapsed_time = round(diff) * 1000
   time_to_completion = round(sts.divide(i.total - i.fetched, int(speed))) * 1000
   estimated_total_time = elapsed_time + time_to_completion  
   progress = "●{0}{1}".format(
       ''.join(["●" for i in range(math.floor(int(percentage) / 4))]),
       ''.join(["○" for i in range(24 - math.floor(int(percentage) / 4))]))
   button =  [[InlineKeyboardButton(progress, f'fwrdstatus#{status}#{estimated_total_time}#{percentage}#{i.id}')]]
   estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
   estimated_total_time = estimated_total_time if estimated_total_time != '' else '0 s'
   if status in ["cancelled", "completed"]:
      button.append([InlineKeyboardButton('• 🌚 ᴄᴏᴍᴘʟᴇᴛᴇᴅ 🌝 ​•', url='https://t.me/Real_Pirates')])
      try:
          await msg.client.send_message(chat_id=i.TO, text="✅ ᴅᴏɴᴇ")
      except Exception as e:
          print(f"Failed to send done message: {e}")
   else:
      button.append([InlineKeyboardButton('🚫 ᴄᴀɴᴄᴇʟ 🚫', 'terminate_frwd')])
   await msg_edit(msg, text, InlineKeyboardMarkup(button))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def is_cancelled(client, user, msg, sts):
   if temp.CANCEL.get(user)==True:
      if sts.TO in temp.IS_FRWD_CHAT:
         temp.IS_FRWD_CHAT.remove(sts.TO)
      await edit(user, msg, 'ᴄᴀɴᴄᴇʟʟᴇᴅ', "cancelled", sts)
      await send(client, user, "<b>❌ ғᴏʀᴡᴀᴅɪɴɢ ᴄᴀɴᴄᴇʟʟᴇᴅ</b>")
      await stop(client, user)
      return True 
   return False 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def stop(client, user):
   try:
     await client.stop()
   except:
     pass 
   await db.rmve_frwd(user)
   temp.forwardings -= 1
   temp.lock[user] = False 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def send(bot, user, text):
   try:
      await bot.send_message(user, text=text)
   except:
      pass 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def custom_caption(msg, caption):
    default_caption = "<b><blockquote>🎀 @PFP_Hub 🎀</blockquote></b>"  # Your default caption if no caption exists

    if msg.media:
        if (msg.video or msg.document or msg.audio or msg.photo):
            media = getattr(msg, msg.media.value, None)
            if media:
                file_name = getattr(media, 'file_name', '')
                file_size = getattr(media, 'file_size', '')
                fcaption = getattr(msg, 'caption', '')

                if fcaption:
                    fcaption = clean_caption(fcaption.html)  # Clean original caption
                else:
                    fcaption = default_caption  # 👈 If no original caption, set default caption

                if caption:
                    formatted = caption.format(
                        filename=file_name,
                        size=get_size(file_size),
                        caption=fcaption
                    )
                    return f" {formatted}"  # Final custom formatted caption
                return f" {fcaption}"  # Just use default if no formatting template

    return default_caption  # 👈 Return default even if no media


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def get_size(size):
  units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
  size = float(size)
  i = 0
  while size >= 1024.0 and i < len(units):
     i += 1
     size /= 1024.0
  return "%.2f %s" % (size, units[i]) 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def keyword_filter(keywords, file_name):
    if keywords is None:
        return False
    if re.search(keywords, file_name):
        return False
    else:
        return True

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def extension_filter(extensions, file_name):
    if extensions is None:
        return False
    if not re.search(extensions, file_name):
        return False
    else:
        return True

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def size_filter(max_size, min_size, file_size):
    file_size = file_size / 1024 / 1024
    if max_size and min_size == 0:
        return False
    if max_size == 0:
        return file_size < min_size
    if min_size == 0:
        return file_size > max_size
    if not min_size <= file_size <= max_size:
        return True
    else:
        return False

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def media(msg):
  if msg.media:
     media = getattr(msg, msg.media.value, None)
     if media:
        return getattr(media, 'file_id', None)
  return None 

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def retry_btn(id):
    return InlineKeyboardMarkup([[InlineKeyboardButton('♻️ RETRY ♻️', f"start_public_{id}")]])

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^terminate_frwd$'))
async def terminate_frwding(bot, m):
    user_id = m.from_user.id 
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True 
    await m.answer("Forwarding cancelled !", show_alert=True)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^fwrdstatus'))
async def status_msg(bot, msg):
    _, status, est_time, percentage, frwd_id = msg.data.split("#")
    sts = STS(frwd_id)
    if not sts.verify():
       fetched, forwarded, remaining = 0
    else:
       fetched, limit, forwarded = sts.get('fetched'), sts.get('limit'), sts.get('total_files')
       remaining = limit - fetched 
    est_time = TimeFormatter(milliseconds=est_time)
    start_time = sts.get('start')
    uptime = await get_bot_uptime(start_time)
    total = sts.get('limit') - sts.get('fetched')
    time_to_comple = await complete_time(total)
    est_time = est_time if (est_time != '' or status not in ['completed', 'cancelled']) else '0 s'
    return await msg.answer(PROGRESS.format(percentage, fetched, forwarded, remaining, status, time_to_comple, uptime), show_alert=True)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(bot, update):
    await update.answer()
    await update.message.delete()

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(['stop']))
async def stop_forward(client, message):
    user_id = message.from_user.id
    sts = await message.reply('<code>Stoping...</code>')
    await asyncio.sleep(0.5)
    if not await db.is_forwad_exit(message.from_user.id):
        return await sts.edit('**No Ongoing Forwards To Cancel**')
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True
    mst = await db.get_forward_details(user_id)
    msg = await client.get_messages(user_id, mst['msg_id'])
    link = f"tg://openmessage?user_id={6648261085}&message_id={mst['msg_id']}"
    await sts.edit(f"<b>Successfully Canceled </b>", disable_web_page_preview=True)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def restart_pending_forwads(bot, user):
    user = user['user_id']
    settings = await db.get_forward_details(user)
    try:
       skiping = settings['offset']
       fetch = settings['fetched'] - settings['skip']
       temp.forwardings += 1
       forward_id = await store_vars(user)
       sts = STS(forward_id)
       if settings['chat_id'] is None:
           return await db.rmve_frwd(user)
           temp.forwardings -= 1
       if not sts.verify():
          temp.forwardings -=1
          return 
       sts.add('fetched', value=fetch)
       sts.add('duplicate', value=settings['duplicate'])
       sts.add('filtered', value=settings['filtered'])
       sts.add('deleted', value=settings['deleted'])
       sts.add('total_files', value=settings['total'])
       m = await bot.get_messages(user, settings['msg_id'])#
       _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
       i = sts.get(full=True)
       filter = datas['filters']
       max_size = datas['max_size']
       min_size = datas['min_size']
       keyword = datas['keywords']
       exten = datas['extensions']
       keywords = ""
       extensions = ""
       if keyword:
           for key in keyword:
               keywords += f"{key}|"
           keywords  = keywords.rstrip("|")
       else:
           keywords = None
       if exten:
           for ext in exten:
               extensions += f"{ext}|"
           extensions = extensions.rstrip("|")
       else:
           extensions = None
       if not _bot:
          return await msg_edit(m, "You didn't added any bot. Please add a bot using /settings !", wait=True)
       if _bot['is_bot'] == True:
          data = _bot['token']
       else:
          data = _bot['session']
       try:
          il = True if _bot['is_bot'] == True else False
          client = await get_client(data, is_bot=il)
          await client.start()
       except Exception as e:  
          return await m.edit(e)
       try:
          await msg_edit(m, "<b>Pirate Working...</b>")
       except:
          return await db.rmve_frwd(user)
       try: 
          await client.get_messages(sts.get("FROM"), sts.get("limit"))
       except:
          await msg_edit(m, f"**Source chat may be a private channel / group. Use userbot (user must be member over there) or  if Make Your [Bot](t.me/{_bot['username']}) an admin over there**", retry_btn(firwd_id), True)
          return await stop(client, user)
       try:
        # Send a test message to the target chat
          k = await client.send_message(
              i.TO,
              "𝐅𝐨𝐫𝐰𝐚𝐫𝐝𝐢𝐧𝐠 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 🏴‍☠\n\n<b><blockquote><a href='https://t.me/Pirates_Auto_Forward_bot?start=true'>@Pirates_Auto_Forward_bot 🦜</a></blockquote></b>"
          )
          random_sticker = random.choice(stickers)
          await client.send_sticker(i.TO, random_sticker)
       
          
          
       except:
          await msg_edit(m, f"**Please Make Your [UserBot / Bot](t.me/{_bot['username']}) Admin In Target Channel With Full Permissions**", retry_btn(forward_id), True)
          return await stop(client, user)
    except:
       return await db.rmve_frwd(user)
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if not connected:
            await msg_edit(m, "<code>Cannot Connected Your db Errors Found Dup files Have Been Skipped after Restart</code>")
        else:
            user_have_db = True
    try:
        start = settings['start_time']
    except KeyError:
        start = None
    sts.add(time=True, start_time=start)
    sleep = 1 if _bot['is_bot'] else 10
    #await msg_edit(m, "<code>processing...</code>") 
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True
    dup_files = []
    if user_have_db and datas['skip_duplicate']:
        old_files = await user_db.get_all_files()
        async for ofile in old_files:
            dup_files.append(ofile["file_id"])
    if locked:
        try:
          MSG = []
          pling=0
          await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
          async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=skiping, filters=filter, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                    if user_have_db:
                       await user_db.drop_all()
                       await user_db.close()
                       return
                    return
                if pling %20 == 0: 
                   await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
                pling += 1
                sts.add('fetched')
                if message == "DUPLICATE":
                   sts.add('duplicate')
                   continue
                elif message == "FILTERED":
                   sts.add('filtered')
                   continue 
                elif message.empty or message.service:
                   sts.add('deleted')
                   continue
                elif message.document and await extension_filter(extensions, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await keyword_filter(keywords, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await size_filter(max_size, min_size, message.document.file_size):
                   sts.add('filtered')
                   continue 
                elif message.document and message.document.file_id in dup_files:
                   sts.add('duplicate')
                   continue
                if message.document and datas['skip_duplicate']:
                    dup_files.append(message.document.file_id)
                    if user_have_db:
                        await user_db.add_file(message.document.file_id)
                if forward_tag:
                   MSG.append(message.id)
                   notcompleted = len(MSG)
                   completed = sts.get('total') - sts.get('fetched')
                   if ( notcompleted >= 100 
                        or completed <= 100): 
                      await forward(user, client, MSG, m, sts, protect)
                      sts.add('total_files', notcompleted)
                      await asyncio.sleep(10)
                      MSG = []
                else:
                   new_caption = custom_caption(message, caption)
                   details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                   await copy(user, client, details, m, sts)
                   sts.add('total_files')
                   await asyncio.sleep(sleep) 
        except Exception as e:
            await msg_edit(m, f'<b>ERROR:</b>\n<code>{e}</code>', wait=True)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
        temp.IS_FRWD_CHAT.remove(sts.TO)
        await send(client, user, "<b>🎉 ғᴏʀᴡᴀᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>")
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await edit(user, m, 'ᴄᴏᴍᴘʟᴇᴛᴇᴅ', "completed", sts) 
        await stop(client, user)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def store_vars(user_id):
    settings = await db.get_forward_details(user_id)
    fetch = settings['fetched']
    forward_id = f'{user_id}-{fetch}'
    print(fetch)
    STS(id=forward_id).store(settings['chat_id'], settings['toid'], settings['skip'], settings['limit'])
    return forward_id

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def restart_forwards(client):
    users = await db.get_all_frwd()
    count = await db.forwad_count()
    tasks = []
    async for user in users:
        tasks.append(restart_pending_forwads(client, user))
    random_seconds = random.randint(0, 300)
    minutes = random_seconds // 60
    seconds = random_seconds % 60
    await asyncio.gather(*tasks)
    print('Done')

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def update_forward(user_id, chat_id, start_time, toid, last_id, limit, forward_id, msg_id, fetched, total, duplicate, deleted, skip, filterd):
    details = {
        'chat_id': chat_id,
        'toid': toid,
        'forward_id': forward_id,
        'last_id': last_id,
        'limit': limit,
        'msg_id': msg_id,
        'start_time': start_time,
        'fetched': fetched,
        'offset': fetched,
        'deleted': deleted,
        'total': total,
        'duplicate': duplicate,
        'skip': skip,
        'filtered':filterd
    }
    await db.update_forward(user_id, details)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_bot_uptime(start_time):
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    uptime_string = ""
    if uptime_weeks != 0:
        uptime_string += f"{uptime_weeks % 7}w, "
    if uptime_days != 0:
        uptime_string += f"{uptime_days % 24}d, "
    if uptime_hours != 0:
        uptime_string += f"{uptime_hours % 24}h, "
    if uptime_minutes != 0:
        uptime_string += f"{uptime_minutes % 60}m, "
    uptime_string += f"{uptime_seconds % 60}s"
    return uptime_string  

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def complete_time(total_files, files_per_minute=30):
    minutes_required = total_files / files_per_minute
    seconds_required = minutes_required * 60
    weeks = seconds_required // (7 * 24 * 60 * 60)
    days = (seconds_required % (7 * 24 * 60 * 60)) // (24 * 60 * 60)
    hours = (seconds_required % (24 * 60 * 60)) // (60 * 60)
    minutes = (seconds_required % (60 * 60)) // 60
    seconds = seconds_required % 60
    time_format = ""
    if weeks > 0:
        time_format += f"{int(weeks)}w, "
    if days > 0:
        time_format += f"{int(days)}d, "
    if hours > 0:
        time_format += f"{int(hours)}h, "
    if minutes > 0:
        time_format += f"{int(minutes)}m, "
    if seconds > 0:
        time_format += f"{int(seconds)}s"
    return time_format

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01



