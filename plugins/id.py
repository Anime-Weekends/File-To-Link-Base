from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot  # This now works!

@Bot.on_message(filters.command("myid") & filters.private)
async def showid(client, message):
    user_id = message.chat.id
    photo_url = "https://i.ibb.co/YzFqHky/photo-2025-04-15-09-14-30-7493465832589099024.jpg"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Oᴡɴᴇʀ", url=f"https://t.me/RexySama"),
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/RexySama")
        ]
    ])

    await message.reply_photo(
        photo=photo_url,
        caption=f"<b><blockquote>Yᴏᴜʀ ᴜsᴇʀ ɪᴅ ɪs:</b> <code>{user_id}</blockquote></code>",
        reply_markup=buttons,
        quote=True
    )
