import sys
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import ADMINS

# Command to show total users with image and close button
@Client.on_message(filters.private & filters.command("users") & filters.user(ADMINS))
async def users(bot, message):
    total_users = await db.total_users_count()
    text = "Bot Status\n"
    text += f"\nTotal Users: {total_users}"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Close", callback_data="close")]
    ])

    img_url = "https://i.ibb.co/YzFqHky/photo-2025-04-15-09-14-30-7493465832589099024.jpg"

    await message.reply_photo(
        photo=img_url,
        caption=text,
        reply_markup=buttons
        message_effect_id=5104841245755180586 #🔥
    )

# Callback to handle "Close" button
@Client.on_callback_query(filters.regex("close"))
async def close_button(bot, query):
    await query.answer("Close")
    await query.message.delete()

# Restart command for admins
@Client.on_message(filters.private & filters.command("restart") & filters.user(ADMINS))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying To Restarting.....</i>",
        quote=True
    )
    await asyncio.sleep(2)
    await msg.edit("<i>Server Restarted Successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)
