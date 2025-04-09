from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from database.users_db import db
from info import ADMINS
import asyncio, datetime, time

# Global cancel flag
cancel_flag = {}

async def send_broadcast(user_id, message, forward=False, pin=False, auto_delete=None):
    try:
        if forward:
            sent = await message.forward(chat_id=user_id)
        else:
            sent = await message.copy(chat_id=user_id)

        if pin:
            try:
                await message._client.pin_chat_message(user_id, sent.id, disable_notification=True)
            except:
                pass
        if auto_delete:
            await asyncio.sleep(auto_delete)
            try:
                await message._client.delete_messages(user_id, sent.id)
            except:
                pass
        return True, "Success"

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_broadcast(user_id, message, forward, pin, auto_delete)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        await db.delete_user(user_id)
        return False, "Invalid"
    except:
        return False, "Failed"

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_handler(client, message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply("**<blockquote>Reply to a message to broadcast it.</blockquote>**")

    buttons = [
        [
            InlineKeyboardButton("➕ Normal", callback_data="bcast:normal"),
            InlineKeyboardButton("🔁 Forward", callback_data="bcast:forward")
        ],
        [
            InlineKeyboardButton("📌 With Pin", callback_data="bcast:pin"),
            InlineKeyboardButton("⏱ Auto-Delete", callback_data="bcast:delete")
        ],
        [
            InlineKeyboardButton("♻ Refresh", callback_data="bcast:refresh"),
            InlineKeyboardButton("✖ Cancel", callback_data="bcast:cancel")
        ]
    ]

    await message.reply_photo(
        photo="https://i.ibb.co/ynjcqYdZ/photo-2025-04-06-20-48-47-7490304985767346192.jpg",
        caption="**<blockquote>Choose your broadcast mode:</blockquote>**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r"bcast:(.*)"))
async def broadcast_callback(client, query):
    action = query.data.split(":")[1]
    user_id = query.from_user.id
    reply = query.message.reply_to_message

    if not reply:
        return await query.answer("Reply message missing.", show_alert=True)

    if action == "cancel":
        cancel_flag[user_id] = True
        return await query.edit_message_caption("**<blockquote>Broadcast Cancelled.</blockquote>**")

    if action == "refresh":
        return await query.answer("UI refreshed!")

    forward = (action == "forward")
    pin = (action == "pin")
    auto_delete = 10 if action == "delete" else None

    cancel_flag[user_id] = False

    users = await db.get_all_users()
    total = await db.total_users_count()
    success = failed = invalid = done = 0
    start = time.time()

    status = await query.edit_message_caption(
        f"**<blockquote>Broadcast started...\n\nTotal: {total}\nDone: {done}\nSuccess: {success}\nInvalid: {invalid}\nFailed: {failed}</blockquote>**"
    )

    async for user in users:
        if cancel_flag.get(user_id):
            await query.message.edit_caption("**<blockquote>Broadcast Cancelled.</blockquote>**")
            return

        uid = int(user.get("id"))
        ok, reason = await send_broadcast(uid, reply, forward=forward, pin=pin, auto_delete=auto_delete)
        done += 1
        if ok:
            success += 1
        else:
            if reason == "Invalid":
                invalid += 1
            else:
                failed += 1

        if done % 20 == 0 or done == total:
            try:
                await status.edit_caption(
                    f"**<blockquote>Broadcasting...\n\nTotal: {total}\nDone: {done}\nSuccess: {success}\nInvalid: {invalid}\nFailed: {failed}</blockquote>**",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("✖ Cancel", callback_data="bcast:cancel")
                    ]])
                )
            except: pass

    duration = str(datetime.timedelta(seconds=int(time.time() - start)))
    await status.edit_caption(
        f"**<blockquote>Broadcast Completed in {duration}.\n\nTotal: {total}\nSuccess: {success}\nInvalid: {invalid}\nFailed: {failed}</blockquote>**"
    )
