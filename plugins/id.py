from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot  # This now works!

@Bot.on_message(filters.command("id") & filters.private)
async def showid(client, message):
    user_id = message.chat.id
    photo_url = "https://i.ibb.co/d0Xg3xMB/photo-2025-04-06-10-07-03-7490139616641548308.jpg"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Button 1", url=f"https://t.me/RexySama"),
            InlineKeyboardButton("Button 2", url=f"https://t.me/RexySama")
        ]
    ])

    await message.reply_photo(
        photo=photo_url,
        caption=f"<b><blockquote>Your User ID is:</b> <code>{user_id}</blockquote></code>",
        reply_markup=buttons,
        quote=True
    )
