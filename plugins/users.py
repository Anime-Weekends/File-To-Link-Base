import sys
import os
import asyncio
from pyrogram.errors import *
from database.users_db import db
from pyrogram import Client, filters
from info import ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.private & filters.command("users") & filters.user(ADMINS))
async def users(bot, update):
    total_users = await db.total_users_count()
    text = "Bot Status\n"
    text += f"\nTotal Users: {total_users}"

    # Inline button
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Close", callback_data="close")]
    ])

    # Image URL or local path
    img_url = "https://i.ibb.co/YzFqHky/photo-2025-04-15-09-14-30-7493465832589099024.jpg"  # Replace with actual image URL or local path

    await update.reply_photo(
        photo=img_url,
        caption=text,
        reply_markup=buttons
    )

# Callback to handle the "Close" button
@Client.on_callback_query(filters.regex("close"))
async def close_button(bot, query):
    await query.message.delete()


@Client.on_message(filters.private & filters.command(['restart']) & filters.user(ADMINS))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying To Restarting.....</i>",
        quote=True
    )
    await asyncio.sleep(2)
    await msg.edit("<i>Server Restarted Successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)
