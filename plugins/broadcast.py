from pyrogram.errors import *
from database.users_db import db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS
import asyncio
import datetime
import time

BROADCAST_IMAGE = "https://i.ibb.co/JzJMc7S/broadcast.jpg"  # Optional: replace with your custom banner
SUPPORT_URL = "https://t.me/AV_SUPPORT_GROUP"  # Replace with your support or repo URL
REFRESH_COMMAND = "broadcast"  # You can change the command to trigger refresh if needed

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception:
        return False, "Error"

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_handler(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    total_users = await db.total_users_count()
    start_time = time.time()

    status = await message.reply_photo(
        photo=BROADCAST_IMAGE,
        caption="**<b>🚀 Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Pʀᴏɢʀᴇss...</b>**\n\n"
                f"**Total Users:** `{total_users}`\n"
                f"**Completed:** `0`\n"
                f"**Success:** `0`\n"
                f"**Blocked:** `0`\n"
                f"**Deleted:** `0`\n"
                f"**Failed:** `0`\n\n"
                f"__Updating every 20 users__",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh Bot", callback_data="refresh_bot")],
            [InlineKeyboardButton("🌐 Support / Repo", url=SUPPORT_URL)]
        ])
    )

    done = success = blocked = deleted = failed = 0

    async for user in users:
        if 'id' in user:
            pti, reason = await broadcast_messages(int(user['id']), b_msg)
            if pti:
                success += 1
            elif reason == "Blocked":
                blocked += 1
            elif reason == "Deleted":
                deleted += 1
            else:
                failed += 1
            done += 1
        else:
            done += 1
            failed += 1

        if not done % 20:
            try:
                progress = f"[{'█' * (done * 10 // total_users)}{'░' * (10 - (done * 10 // total_users))}]"
                await status.edit_caption(
                    caption="**<b>🚀 Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Pʀᴏɢʀᴇss...</b>**\n\n"
                            f"**Total Users:** `{total_users}`\n"
                            f"**Completed:** `{done}`\n"
                            f"**Success:** `{success}`\n"
                            f"**Blocked:** `{blocked}`\n"
                            f"**Deleted:** `{deleted}`\n"
                            f"**Failed:** `{failed}`\n\n"
                            f"__Progress__:\n`{progress}`",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 Refresh Bot", callback_data="refresh_bot")],
                        [InlineKeyboardButton("🌐 Support / Repo", url=SUPPORT_URL)]
                    ])
                )
            except:
                pass

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    final_bar = f"[{'█' * 10}]"
    await status.edit_caption(
        caption="**<b>✅ Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ!</b>**\n\n"
                f"**Time Taken:** `{time_taken}`\n"
                f"**Total Users:** `{total_users}`\n"
                f"**Completed:** `{done}`\n"
                f"**Success:** `{success}`\n"
                f"**Blocked:** `{blocked}`\n"
                f"**Deleted:** `{deleted}`\n"
                f"**Failed:** `{failed}`\n\n"
                f"__Progress__:\n`{final_bar}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh Bot", callback_data="refresh_bot")],
            [InlineKeyboardButton("🌐 Support / Repo", url=SUPPORT_URL)]
        ])
    )
