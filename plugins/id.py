from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Bot.on_message(filters.command("id") & filters.private)
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        photo_url = "https://example.com/image.jpg"  # Replace with your image URL or file_id

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Button 1", callback_data="btn1"),
                InlineKeyboardButton("Button 2", callback_data="btn2")
            ]
        ])

        await message.reply_photo(
            photo=photo_url,
            caption=f"<b>ʏᴏᴜʀ ᴜsᴇʀ ɪᴅ ɪs:</b> <code>{user_id}</code>",
            reply_markup=buttons,
            quote=True
        )
