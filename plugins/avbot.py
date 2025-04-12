import asyncio
import time
from typing import Union
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from Script import script
from info import (
    AUTH_PICS,
    AUTH_CHANNEL,
    ENABLE_LIMIT,
    RATE_LIMIT_TIMEOUT,
    MAX_FILES,
    BAN_ALERT,
    ADMINS,
    AUTH_CHANNELS
)

rate_limit = {}

# Function to check if user is joined in required channels
async def is_user_joined(bot, message: Message):
    user_id = message.from_user.id
    missing_channels = []

    for ch in AUTH_CHANNELS:
        if not ch:
            continue
        chat_id = int(ch) if ch.startswith("-100") else ch
        status = await check_user_in_channel(bot, chat_id, user_id)

        if status == "banned":
            await message.reply_text(
                text=BAN_ALERT.format(ADMINS),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False
        elif status is False:
            invite = await get_invite_link(bot, chat_id)
            missing_channels.append(invite.invite_link)

    if missing_channels:
        buttons = [
            [InlineKeyboardButton(f"Jᴏɪɴ Cʜᴀɴɴᴇʟ {i+1}", url=link)]
            for i, link in enumerate(missing_channels)
        ]
        if AUTH_PICS:
            ver = await message.reply_photo(
                photo=AUTH_PICS,
                caption=script.AUTH_TXT.format(message.from_user.mention),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            ver = await message.reply_text(
                text=script.AUTH_TXT.format(message.from_user.mention),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        await asyncio.sleep(30)
        try:
            await ver.delete()
            await message.delete()
        except Exception:
            pass
        return False

    return True


# Function to check user’s status in a specific channel
async def check_user_in_channel(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        elif member.status == "kicked":
            return "banned"
        else:
            return False
    except UserNotParticipant:
        return False
    except Exception:
        return False


# Rate limiter function to restrict number of file requests
async def is_user_allowed(user_id):
    current_time = time.time()

    if ENABLE_LIMIT:
        if user_id in rate_limit:
            file_count, last_time = rate_limit[user_id]
            if file_count >= MAX_FILES and (current_time - last_time) < RATE_LIMIT_TIMEOUT:
                remaining_time = int(RATE_LIMIT_TIMEOUT - (current_time - last_time))
                return False, remaining_time  # ❌ Limit Exceeded
            elif file_count >= MAX_FILES:
                rate_limit[user_id] = [1, current_time]  # ✅ Reset Limit
            else:
                rate_limit[user_id][0] += 1
        else:
            rate_limit[user_id] = [1, current_time]

    return True, 0  # ✅ Allowed

# Don’t remove credits.
# @AV_BOTz_UPDATE | Repo by @BOT_OWNER26 | Help: @AV_SUPPORT_GROUP
