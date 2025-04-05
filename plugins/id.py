from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Bot.on_message(filters.command("id") & filters.private)
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        photo_url = "https://i.ibb.co/q3tWtLCv/photo-2025-04-05-08-59-25-7489751171209363460.jpg"  # Replace with your image URL or file_id

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Button 1", url=f"https://t.me/{OWNER_USERNAME}"),
                InlineKeyboardButton("Button 2", url=f"https://t.me/{OWNER_USERNAME}")
            ]
        ])

        await message.reply_photo(
            photo=photo_url,
            caption=f"<b>ʏᴏᴜʀ ᴜsᴇʀ ɪᴅ ɪs:</b> <code>{user_id}</code>",
            reply_markup=buttons,
            quote=True
        )
