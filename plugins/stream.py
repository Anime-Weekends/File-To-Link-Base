import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from web.utils.file_properties import get_hash
from info import URL, BOT_USERNAME, BIN_CHANNEL, BAN_ALERT, FSUB, CHANNEL
from utils import get_size
from Script import script
from plugins.avbot import is_user_joined, is_user_allowed

# Credit: @AV_BOTz_UPDATE | Repo by @BOT_OWNER26

@Client.on_message((filters.private) & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):
    # Force Subscribe Check
    if FSUB:
        if not await is_user_joined(c, m):
            return

    # Check if Banned
    ban_chk = await db.is_banned(int(m.from_user.id))
    if ban_chk:
        return await m.reply(BAN_ALERT)

    user_id = m.from_user.id

    # Check if User is Allowed
    is_allowed, remaining_time = await is_user_allowed(user_id)
    if not is_allowed:
        await m.reply_text(
            f"🚫 **आप 10 फाइल पहले ही भेज चुके हैं!**\nकृपया **{remaining_time} सेकंड** बाद फिर से प्रयास करें।",
            quote=True
        )
        return

    file_id = m.document or m.video or m.audio
    file_name = file_id.file_name if file_id.file_name else "Unknown"
    file_size = get_size(file_id.file_size)

    try:
        msg = await m.forward(chat_id=BIN_CHANNEL)

        # Generate Links
        file_hash = get_hash(msg)
        stream = f"{URL}watch/{msg.id}?hash={file_hash}"
        download = f"{URL}{msg.id}?hash={file_hash}"
        file_link = f"https://t.me/{BOT_USERNAME}?start=file_{msg.id}"
        share_link = f"https://t.me/share/url?url={file_link}"

        # Notify in BIN_CHANNEL
        await msg.reply_text(
            text=f"Requested By: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                 f"User ID: `{m.from_user.id}`\n"
                 f"Stream Link: {stream}",
            disable_web_page_preview=True,
            quote=True
        )

        # Prepare Inline Keyboard
        buttons = [
            [InlineKeyboardButton("Stream", url=stream), InlineKeyboardButton("Download", url=download)],
            [InlineKeyboardButton("Get File", url=file_link), InlineKeyboardButton("Share", url=share_link)],
            [InlineKeyboardButton("Close", callback_data="close_data")]
        ]

        # Send Response
        await m.reply_text(
            text=script.CAPTION_TXT.format(CHANNEL, file_name, file_size, stream, download),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except FloodWait as e:
        print(f"Sleeping for {e.value}s")
        await asyncio.sleep(e.value)
        await c.send_message(
            chat_id=BIN_CHANNEL,
            text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {e.value}s from "
                 f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n"
                 f"**User ID:** `{m.from_user.id}`",
            disable_web_page_preview=True
        )
