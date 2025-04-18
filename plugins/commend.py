import os, random, asyncio, time 
from Script import script
from database.users_db import db
from pyrogram import Client, filters, enums
from pyrogram.errors import *
from pyrogram.types import *
from info import BOT_USERNAME, ADMINS, OWNER_USERNAME, SUPPORT, PICS, CHANNEL, LOG_CHANNEL, FSUB, BIN_CHANNEL
import re
from utils import get_readable_time
from web.utils import StartTime, __version__
from plugins.avbot import is_user_joined

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT.format(message.from_user.id, message.from_user.mention)
        )

    if FSUB:
        if not await is_user_joined(client, message):
            return

    if len(message.command) != 2 or (len(message.command) == 2 and message.command[1] == "start"):
        buttons = [[
            InlineKeyboardButton("G", callback_data="help"),
            InlineKeyboardButton("O", callback_data="help"),
            InlineKeyboardButton("J", callback_data="help"),
            InlineKeyboardButton("O", callback_data="help")
        ],[
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")
        ],[
            InlineKeyboardButton("Hᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)

        m = await message.reply_text(
            "<i>Wᴇʟᴄᴏᴍᴇ ᴛᴏ <b>ɢᴏᴊᴏ</b>.\nʟᴏᴀᴅɪɴɢ ɪɴᴛᴇʀғᴀᴄᴇ...</i>",
            parse_mode=enums.ParseMode.HTML
        )
        await asyncio.sleep(0.4)
        await m.edit_text("👀")
        await asyncio.sleep(0.5)
        await m.edit_text("✨")
        await asyncio.sleep(0.5)
        await m.edit_text("<b><i>Sᴛᴀʀᴛɪɴɢ...</i></b>")
        await asyncio.sleep(0.4)
        await m.delete()

        sticker = await message.reply_sticker(
            "CAACAgUAAxkBAAEORWdn9t14H6o0kLthL0Q7rX0T2dYdgQACpxUAAoIFuFYlqHCk6hgEjDYE"
        )
        await asyncio.sleep(1)
        await sticker.delete()

        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, BOT_USERNAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            message_effect_id=5104841245755180586 #🔥
        )
	    
	
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "about":
        buttons = [[
	    InlineKeyboardButton('Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/RexySama')
	],[
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
	    InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        me2 = (await client.get_me()).mention
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(me2, me2, get_readable_time(time.time() - StartTime), __version__),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('G', callback_data='help'),
	    InlineKeyboardButton('O', callback_data='help'),
	    InlineKeyboardButton('J', callback_data='help'),
	    InlineKeyboardButton('O', callback_data='help')
        ],[
            InlineKeyboardButton('Dᴇᴠᴇʟᴏᴘᴇʀ', url=f"https://t.me/{OWNER_USERNAME}")
        ],[
	    InlineKeyboardButton('Hᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, BOT_USERNAME),
            reply_markup=reply_markup,
             parse_mode=enums.ParseMode.HTML
        )


	
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Aᴅᴍɪɴ', callback_data='admincmd')
	],[
	    InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
	    InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )  

    elif query.data == "admincmd":
        #if user isnt admin then return
        if not query.from_user.id in ADMINS:
            return await query.answer('This Feature Is Only For Admins !' , show_alert=True)
        buttons = [[
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_CMD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
       )

#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP
	
    elif query.data.startswith("sendAlert"):
        user_id =(query.data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        if len(str(user_id)) == 10:
            reason = str(query.data.split("_")[2])
            try:
                await client.send_message(user_id , f"<b>ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ʙʏ [ᴀᴠ ᴄʜᴀᴛ ᴏᴡɴᴇʀ](https://telegram.me/AV_OWNER_BOT)\nʀᴇᴀsᴏɴ : {reason}</b>")
                await query.message.edit(f"<b>Aʟᴇʀᴛ sᴇɴᴛ ᴛᴏ <code>{user_id}</code>\nʀᴇᴀsᴏɴ : {reason}</b>")
            except Exception as e:
                await query.message.edit(f"<b>sʀʏ ɪ ɢᴏᴛ ᴛʜɪs ᴇʀʀᴏʀ : {e}</b>")
        else:
            await query.message.edit(f"<b>Tʜᴇ ᴘʀᴏᴄᴇss ᴡᴀs ɴᴏᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴡᴀs ɴᴏᴛ ᴠᴀʟɪᴅ, ᴏʀ ᴘᴇʀʜᴀᴘs ɪᴛ ᴡᴀs ᴀ ᴄʜᴀɴɴᴇʟ ɪᴅ</b>")
    elif query.data.startswith('noAlert'):
        user_id =(query.data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        await query.message.edit(f"<b>Tʜᴇ ʙᴀɴ ᴏɴ <code>{user_id}</code> ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sɪʟᴇɴᴛʟʏ.</b>")

    elif query.data.startswith('sendUnbanAlert'):
        user_id =(query.data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        if len(str(user_id)) == 10:
            try:
                unban_text = "<b>ʜᴜʀʀᴀʏ..ʏᴏᴜ ᴀʀᴇ ᴜɴʙᴀɴɴᴇᴅ ʙʏ [ᴏᴡɴᴇʀ](https://telegram.me/RexySama)</b>"
                await client.send_message(user_id , unban_text)
                await query.message.edit(f"<b>Uɴʙᴀɴɴᴇᴅ Aʟᴇʀᴛ sᴇɴᴛ ᴛᴏ <code>{user_id}</code>\nᴀʟᴇʀᴛ ᴛᴇxᴛ : {unban_text}</b>")
            except Exception as e:
                await query.message.edit(f"<b>sʀʏ ɪ ɢᴏᴛ ᴛʜɪs ᴇʀʀᴏʀ : {e}</b>")
        else:
            await query.message.edit(f"<b>Tʜᴇ ᴘʀᴏᴄᴇss ᴡᴀs ɴᴏᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴡᴀs ɴᴏᴛ ᴠᴀʟɪᴅ, ᴏʀ ᴘᴇʀʜᴀᴘs ɪᴛ ᴡᴀs ᴀ ᴄʜᴀɴɴᴇʟ ɪᴅ</b>")
            
    elif query.data.startswith('NoUnbanAlert'):
        user_id =(query.data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        await query.message.edit(f"Tʜᴇ ᴜɴʙᴀɴ ᴏɴ <code>{user_id}</code> ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sɪʟᴇɴᴛʟʏ.")

#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP

@Client.on_message(filters.command("rules"))
async def help(client, message):
    btn = [[
       InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close_data'), 
       InlineKeyboardButton('Dᴇᴠᴇʟᴏᴘᴇʀ', url=f"https://t.me/{OWNER_USERNAME}")
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await message.reply_photo(
        photo="https://i.ibb.co/Z7Sx6kH/photo-2025-04-04-10-30-02-7489403360462766096.jpg",  # or a local file like "images/help.jpg"
        caption=script.HELP2_TXT,
        reply_markup=reply_markup, 
	    message_effect_id=5104841245755180586 #🔥
     )

#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP

@Client.on_message(filters.command("about"))
async def about(client, message):
    buttons = [[
       InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close_data'), 
       InlineKeyboardButton('Dᴇᴠᴇʟᴏᴘᴇʀ', url=f"https://t.me/{OWNER_USERNAME}")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    me2 = (await client.get_me()).mention
    await message.reply_photo(
	photo="https://i.ibb.co/gLqGzf3p/photo-2025-04-04-10-31-34-7489403759894724612.jpg",
	caption=script.ABOUT_TXT2.format(me2, me2, get_readable_time(time.time() - StartTime)),
	reply_markup=reply_markup, 
	    message_effect_id=5104841245755180586 #🔥
     )

	
#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP
