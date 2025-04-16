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

@Client.on_message((filters.private) & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):
    # Force Subscribe Check
    if FSUB:
        if not await is_user_joined(c, m):
            return

    # Check if Banned
    if await db.is_banned(int(m.from_user.id)):
        return await m.reply(BAN_ALERT)

    user_id = m.from_user.id

    # Check user limit
    is_allowed, remaining_time = await is_user_allowed(user_id)
    if not is_allowed:
        await m.reply_text(
            f"🚫 You have already sent 10 files.\nPlease try again after **{remaining_time} seconds**.",
            quote=True
        )
        return

    file_id = m.document or m.video or m.audio
    file_name = file_id.file_name if file_id.file_name else "Unknown"
    file_size = get_size(file_id.file_size)

    try:
        msg = await m.forward(chat_id=BIN_CHANNEL)

        # Ensure URL is valid
        base_url = URL if URL.startswith("http") else f"https://{URL}"

        # Generate Links
        stream = f"{base_url}watch/{msg.id}?hash={get_hash(msg)}"
        download = f"{base_url}{msg.id}?hash={get_hash(msg)}"
        file_link = f"https://t.me/{BOT_USERNAME}?start=file_{msg.id}"
        share_link = f"https://t.me/share/url?url={file_link}"

        # Notify in BIN_CHANNEL
        await msg.reply_text(
            text=f"Requested by: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                 f"User ID: `{m.from_user.id}`\n"
                 f"Stream Link: {stream}",
            disable_web_page_preview=True,
            quote=True
        )

        # Send response with full or short caption
        if file_name:
            await m.reply_text(
                text=script.CAPTION_TXT.format(CHANNEL, file_name, file_size, stream, download),
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Stream", url=stream),
                     InlineKeyboardButton("Download", url=download)],
                    [InlineKeyboardButton("Get File", url=file_link),
                     InlineKeyboardButton("Share", url=share_link),
                     InlineKeyboardButton("Close", callback_data="close_data")]
                ])
            )
        else:
            await m.reply_text(
                text=script.CAPTION2_TXT.format(CHANNEL, file_name, file_size, download),
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Download", url=download),
                     InlineKeyboardButton("Get File", url=file_link)],
                    [InlineKeyboardButton("Share", url=share_link),
                     InlineKeyboardButton("Close", callback_data="close_data")]
                ])
            )

    except FloodWait as e:
        print(f"Sleeping for {e.value}s")
        await asyncio.sleep(e.value)
        await c.send_message(
            chat_id=BIN_CHANNEL,
            text=f"FloodWait of {e.value}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n"
                 f"User ID: `{m.from_user.id}`",
            disable_web_page_preview=True
        )
