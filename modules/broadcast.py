from pyrogram.errors import *
from database.users_db import db
from pyrogram import Client, filters
from info import ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import datetime
import time
import random

# Global flag for canceling broadcast
broadcast_cancel = {}

BROADCAST_IMG = "https://i.ibb.co/b5PwhJxm/photo-2025-04-06-20-48-47-7490897815808245776.jpg"
URL_BTN = "https://t.me/RexySama"

async def broadcast_messages(user_id, message, forward=False, pin=False, delete_after=None):
    try:
        if forward:
            sent = await message.forward(chat_id=user_id)
        else:
            sent = await message.copy(chat_id=user_id)
        if pin:
            await sent.pin(disable_notification=True)
        if delete_after:
            await asyncio.sleep(delete_after)
            await sent.delete()
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, forward, pin, delete_after)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        await db.delete_user(int(user_id))
        return False, "Invalid"
    except Exception:
        return False, "Error"

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def start_broadcast(bot, message):
    global broadcast_cancel
    broadcast_id = random.randint(10000, 99999)
    broadcast_cancel[broadcast_id] = False

    b_msg = message.reply_to_message
    users = await db.get_all_users()
    total_users = await db.total_users_count()
    forward = "forward" in message.command
    delete_after = 10 if "autodelete" in message.command else None
    pin = "pin" in message.command

    status_msg = await message.reply_photo(
        BROADCAST_IMG,
        caption=f"**<b>Broadcast Started</b>**\n\nTotal users: {total_users}\n\n<b>Status:</b> Processing...",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Refresh", callback_data=f"refresh_{broadcast_id}"),
             InlineKeyboardButton("Cancel", callback_data=f"cancel_{broadcast_id}")],
            [InlineKeyboardButton("Join Updates Channel", url=URL_BTN)]
        ])
    )

    done = success = blocked = deleted = failed = 0
    start_time = time.time()

    async for user in users:
        if broadcast_cancel.get(broadcast_id):
            break
        uid = user.get("id")
        if uid:
            sent, reason = await broadcast_messages(
                user_id=int(uid),
                message=b_msg,
                forward=forward,
                pin=pin,
                delete_after=delete_after
            )
            if sent:
                success += 1
            else:
                if reason == "Blocked":
                    blocked += 1
                elif reason == "Deleted":
                    deleted += 1
                else:
                    failed += 1
            done += 1

        if not done % 20:
            try:
                await status_msg.edit_caption(
                    f"**<b>Broadcast in Progress...</b>**\n\n"
                    f"Total: {total_users}\n"
                    f"Done: {done}\n"
                    f"Success: {success}\n"
                    f"Blocked: {blocked}\n"
                    f"Deleted: {deleted}\n"
                    f"Failed: {failed}",
                    reply_markup=status_msg.reply_markup
                )
            except:
                pass

    end_time = time.time()
    duration = datetime.timedelta(seconds=int(end_time - start_time))
    final_text = (
        f"**<b>Broadcast Finished</b>**\n\n"
        f"Total Users: {total_users}\n"
        f"Completed: {done}\n"
        f"Success: {success}\n"
        f"Blocked: {blocked}\n"
        f"Deleted: {deleted}\n"
        f"Failed: {failed}\n"
        f"Time Taken: {duration}"
    )

    try:
        await status_msg.edit_caption(final_text, reply_markup=None)
    except:
        pass

    del broadcast_cancel[broadcast_id]

@Client.on_callback_query(filters.regex("cancel_(.*)"))
async def cancel_broadcast_cb(bot, query):
    bc_id = int(query.data.split("_")[1])
    broadcast_cancel[bc_id] = True
    await query.answer("Broadcast cancelled.", show_alert=True)
    await query.message.edit_caption("**<b>Broadcast Cancelled.</b>**", reply_markup=None)

@Client.on_callback_query(filters.regex("refresh_(.*)"))
async def refresh_status(bot, query):
    await query.answer("Refreshing...", show_alert=False)
