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
        # Forward file to BIN_CHANNEL
        msg = await m.forward(chat_id=BIN_CHANNEL)

        # Ensure base URL is valid
        base_url = URL.strip()
        if not base_url.startswith("http"):
            base_url = f"https://{base_url}"

        msg_hash = get_hash(msg)

        # Build links
        stream = f"{base_url}/watch/{msg.id}?hash={msg_hash}"
        download = f"{base_url}/{msg.id}?hash={msg_hash}"
        file_link = f"https://t.me/{BOT_USERNAME}?start=file_{msg.id}"
        share_link = f"https://t.me/share/url?url={file_link}"

        # URL validation helper
        def is_valid_url(url):
            return url.startswith("http://") or url.startswith("https://")

        # Fallbacks
        fallback_url = "https://t.me"
        stream = stream if is_valid_url(stream) else fallback_url
        download = download if is_valid_url(download) else fallback_url
        file_link = file_link if is_valid_url(file_link) else fallback_url
        share_link = share_link if is_valid_url(share_link) else fallback_url

        # Notify in BIN_CHANNEL
        await msg.reply_text(
            text=f"Requested by: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                 f"User ID: `{m.from_user.id}`\n"
                 f"Stream Link: {stream}",
            disable_web_page_preview=True,
            quote=True
        )

        # Inline buttons
        if file_name:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("Stream", url=stream),
                 InlineKeyboardButton("Download", url=download)],
                [InlineKeyboardButton("Get File", url=file_link),
                 InlineKeyboardButton("Share", url=share_link),
                 InlineKeyboardButton("Close", callback_data="close_data")]
            ])
            caption = script.CAPTION_TXT.format(CHANNEL, file_name, file_size, stream, download)
        else:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("Download", url=download),
                 InlineKeyboardButton("Get File", url=file_link)],
                [InlineKeyboardButton("Share", url=share_link),
                 InlineKeyboardButton("Close", callback_data="close_data")]
            ])
            caption = script.CAPTION2_TXT.format(CHANNEL, file_name, file_size, download)

        # Send message to user
        await m.reply_text(
            text=caption,
            quote=True,
            disable_web_page_preview=True,
            reply_markup=reply_markup
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
