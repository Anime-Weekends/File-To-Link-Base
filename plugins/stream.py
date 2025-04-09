import asyncio
from database.users_db import db
from web.utils.file_properties import get_hash
from pyrogram import Client, filters
from info import URL, BOT_USERNAME, BIN_CHANNEL, BAN_ALERT, FSUB, CHANNEL
from utils import get_size
from Script import script, IMAGE_URL
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from plugins.avbot import is_user_joined, is_user_allowed


def escape_md(text: str) -> str:
    return (
        str(text)
        .replace("_", "\\_")
        .replace("*", "\\*")
        .replace("[", "\")
        .replace("]", "\")
        .replace("(", "\")
        .replace(")", "\")
        .replace("~", "\\~")
        .replace("`", "\\`")
        .replace(">", "\\>")
        .replace("#", "\\#")
        .replace("+", "\\+")
        .replace("-", "\\-")
        .replace("=", "\\=")
        .replace("|", "\\|")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace(".", "\\.")
        .replace("!", "\\!")
    )


@Client.on_message((filters.private) & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):
    if FSUB:
        if not await is_user_joined(c, m):
            return

    if await db.is_banned(int(m.from_user.id)):
        return await m.reply(BAN_ALERT)

    user_id = m.from_user.id

    is_allowed, remaining_time = await is_user_allowed(user_id)
    if not is_allowed:
        return await m.reply_text(
            f"*You have already uploaded 10 files\\!* Try again in *{remaining_time} seconds*\\.",
            quote=True,
            parse_mode="MarkdownV2"
        )

    file_id = m.document or m.video or m.audio
    file_name = escape_md(file_id.file_name) if file_id.file_name else "Unknown"
    file_size = escape_md(get_size(file_id.file_size))

    try:
        msg = await m.forward(chat_id=BIN_CHANNEL)
        file_hash = get_hash(msg)

        stream = f"{URL}watch/{msg.id}?hash={file_hash}"
        download = f"{URL}{msg.id}?hash={file_hash}"
        file_link = f"https://t.me/{BOT_USERNAME}?start=file_{msg.id}"
        share_link = f"https://t.me/share/url?url={file_link}"

        await msg.reply_text(
            text=(
                f"> Requested by: [{escape_md(m.from_user.first_name)}](tg://user?id={m.from_user.id})\n"
                f"> User ID: `{m.from_user.id}`\n"
                f"> [Stream Link]({stream})"
            ),
            disable_web_page_preview=True,
            quote=True,
            parse_mode="MarkdownV2"
        )

        buttons = [
            [
                InlineKeyboardButton("Stream", url=stream),
                InlineKeyboardButton("Download", url=download)
            ],
            [
                InlineKeyboardButton("Get File", url=file_link),
                InlineKeyboardButton("Share", url=share_link),
                InlineKeyboardButton("Close", callback_data="close_data")
            ]
        ]

        await m.reply_photo(
            photo=IMAGE_URL,
            caption=script.CAPTION_TXT.format(
                escape_md(CHANNEL),
                file_name,
                file_size,
                stream,
                download
            ),
            parse_mode="MarkdownV2",
            quote=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except FloodWait as e:
        print(f"Sleeping for {e.value}s due to FloodWait")
        await asyncio.sleep(e.value)
        await c.send_message(
            chat_id=BIN_CHANNEL,
            text=(
                f"FloodWait triggered: {e.value} seconds\n"
                f"User: [{escape_md(m.from_user.first_name)}](tg://user?id={m.from_user.id})\n"
                f"User ID: `{m.from_user.id}`"
            ),
            disable_web_page_preview=True,
            parse_mode="MarkdownV2"
        )
