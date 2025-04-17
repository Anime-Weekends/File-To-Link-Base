import asyncio
from web.utils.file_properties import get_hash
from pyrogram import Client, filters, enums
from info import BIN_CHANNEL, BAN_CHNL, BANNED_CHANNELS, URL, CHANNEL, BOT_USERNAME
from Script import script
from database.users_db import db
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Dont Remove My Credit @AV_BOTz_UPDATE 
# This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP

@Client.on_message(filters.channel & (filters.document | filters.video) & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot: Client, broadcast: Message):
    try:
        if int(broadcast.chat.id) in BAN_CHNL:
            print("Channel is banned. Skipping.")
            return

        ban_chk = await db.is_banned(int(broadcast.chat.id))
        if int(broadcast.chat.id) in BANNED_CHANNELS or ban_chk is True:
            await bot.leave_chat(broadcast.chat.id)
            return

        file = broadcast.document or broadcast.video
        file_name = file.file_name if file else "Unknown File"

        # Forward to BIN_CHANNEL
        msg = await broadcast.forward(chat_id=BIN_CHANNEL)

        # Safe base URL
        base_url = URL if URL.startswith("http") else f"https://{URL}"
        hash_val = get_hash(msg)

        stream = f"{base_url}watch/{msg.id}?hash={hash_val}"
        download = f"{base_url}{msg.id}?hash={hash_val}"
        file_link = f"https://t.me/{BOT_USERNAME}?start=file_{msg.id}"

        # Debug print (optional)
        print(f"Stream: {stream}, Download: {download}, File Link: {file_link}")

        await msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**CHANNEL ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream}",
            quote=True
        )

        # Caption and Buttons
        new_caption = f"<i><a href='{CHANNEL}'>{file_name}</a></i>"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴛʀᴇᴀᴍ", url=stream),
             InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ", url=download)],
            [InlineKeyboardButton('Gᴇᴛ ғɪʟᴇ', url=file_link)]
        ])

        await bot.edit_message_caption(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            caption=new_caption,
            reply_markup=buttons,
            parse_mode=enums.ParseMode.HTML
        )

    except asyncio.exceptions.TimeoutError:
        print("Timeout Error, retrying in 5s...")
        await asyncio.sleep(5)
        await channel_receive_handler(bot, broadcast)

    except FloodWait as w:
        print(f"FloodWait: Sleeping for {w.value}s")
        await asyncio.sleep(w.value)

    except Exception as e:
        await bot.send_message(
            chat_id=BIN_CHANNEL,
            text=f"❌ **Error in stream2.py:** `{str(e)}`",
            disable_web_page_preview=True
        )
        print(f"❌ Error: {e}")
