# plugins/giveaway.py

from pyrofork import Client, filters
from pyrofork.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
from config import MONGO_URI, ADMINS
from asyncio import sleep
from datetime import datetime
import random

# DB setup
mongo = MongoClient(MONGO_URI)
db = mongo['GiveawayDB']
collection = db['Giveaways']

@Client.on_message(filters.command("giveaway") & filters.user(ADMINS))
async def start_giveaway(client: Client, message: Message):
    args = message.text.split(None, 2)
    if len(args) < 3:
        return await message.reply_text("Usage: `/giveaway <duration_in_minutes> <title>`")

    try:
        duration = int(args[1])
        title = args[2]
    except ValueError:
        return await message.reply_text("Duration must be an integer.")

    msg = await message.reply_photo(
        photo="https://i.ibb.co/r6KWBXx/giveaway.jpg",
        caption=f">>> **🎉 New Giveaway Started!**\n\n**Prize:** `{title}`\n**Duration:** `{duration}` minutes\n\nClick below to participate!",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎁 Join Giveaway", callback_data=f"join_{message.chat.id}")]]
        )
    )

    collection.insert_one({
        "chat_id": message.chat.id,
        "message_id": msg.id,
        "title": title,
        "duration": duration,
        "start_time": datetime.utcnow(),
        "participants": []
    })

    await sleep(duration * 60)

    data = collection.find_one({"chat_id": message.chat.id, "message_id": msg.id})
    participants = data["participants"]

    if not participants:
        await msg.reply("**No participants joined the giveaway.**")
        collection.delete_one({"_id": data["_id"]})
        return

    winner_id = random.choice(participants)
    try:
        winner = await client.get_users(winner_id)
        winner_mention = winner.mention
    except:
        winner_mention = f"`{winner_id}`"

    await msg.reply_photo(
        photo="https://i.ibb.co/sRgxMfW/winner.jpg",
        caption=f">>> **🏆 Giveaway Ended!**\n\n**Prize:** `{title}`\n**Winner:** {winner_mention}\n\nThanks for participating!"
    )
    collection.delete_one({"_id": data["_id"]})


@Client.on_callback_query(filters.regex(r"join_(\d+)"))
async def join_giveaway_callback(client: Client, callback_query: CallbackQuery):
    chat_id = int(callback_query.matches[0].group(1))
    data = collection.find_one({"chat_id": chat_id})

    if not data:
        return await callback_query.answer("This giveaway has ended.", show_alert=True)

    user_id = callback_query.from_user.id
    if user_id in data["participants"]:
        return await callback_query.answer("You already joined!", show_alert=True)

    collection.update_one({"_id": data["_id"]}, {"$push": {"participants": user_id}})
    await callback_query.answer("You're in! Good luck!")
