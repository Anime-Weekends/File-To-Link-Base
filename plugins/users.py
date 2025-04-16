import sys
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import ADMINS
from datetime import datetime

# Record bot start time
START_TIME = datetime.now()
BOT_VERSION = "v1.2.3"

def get_uptime():
    uptime = datetime.now() - START_TIME
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m"

# Command to show total users with image and close button
@Client.on_message(filters.private & filters.command("users") & filters.user(ADMINS))
async def users(bot, message):
    total_users = await db.total_users_count()
    active_users = await db.active_users_count()  # Updated to use new method
    banned_users = await db.banned_users_count()
    uptime = get_uptime()

    text = "<b><blockquote>𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦</blockquote></b>\n"
    text += f"<blockquote>\nTotal Users: {total_users}</blockquote>"
    text += f"<blockquote>\nActive Users: {active_users}</blockquote>"
    text += f"<blockquote>\nBanned Users: {banned_users}</blockquote>"
    text += f"<blockquote>\nVersion: {BOT_VERSION}</blockquote>"
    text += f"<blockquote>\nUptime: {uptime}</blockquote>"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Close", callback_data="close")]
    ])

    img_url = "https://i.ibb.co/YzFqHky/photo-2025-04-15-09-14-30-7493465832589099024.jpg"

    await message.reply_photo(
        photo=img_url,
        caption=text,
        reply_markup=buttons,
        message_effect_id=5104841245755180586 #
    )

# Callback to handle "Close" button
@Client.on_callback_query(filters.regex("close"))
async def close_button(bot, query):
    await query.answer("Closed")
    await query.message.delete()

# Restart command for admins
@Client.on_message(filters.private & filters.command("restart") & filters.user(ADMINS))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying to restart...</i>",
        quote=True
    )
    await asyncio.sleep(2)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)
