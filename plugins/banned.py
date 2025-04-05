from utils import temp 
from database.users_db import db
from info import *
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from pyrogram.errors import ChatAdminRequired
import asyncio
from pyrogram.enums import ParseMode

#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def do_ban(bot, message):
    userid = message.text.split(" ", 2)[1] if len(message.text.split(" ", 1)) > 1 else None
    reason = message.text.split(" ", 2)[2] if len(message.text.split(" ", 2)) > 2 else None

    if not userid:
        await message.reply_photo(
            photo="https://i.ibb.co/BHqdCMCY/photo-2025-04-03-11-48-19-7489356433650090000.jpg",  # Generated image path
            caption=(
                "<b><blockquote>Pʟᴇᴀsᴇ ᴀᴅᴅ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ/ᴄʜᴀɴɴᴇʟ ɪᴅ ᴡɪᴛʜ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ</blockquote>\n"
                "<blockquote>ᴇx : /ban (user/channel_id) (banning reason[Optional]) \n"
                "ʀᴇᴀʟ ᴇx : <code>/ban 1234567899</code>\n"
                "ᴡɪᴛʜ ʀᴇᴀsᴏɴ ᴇx:<code>/ban 1234567899 sending adult links to bot</code>\n"
                "ᴛᴏ ʙᴀɴ ᴀ ᴄʜᴀɴɴᴇʟ :\n<code>/ban CHANEL_ID</code>\n"
                "ᴇx : <code>/ban -1001234567899</code></blockquote></b>"
            ),
            parse_mode=ParseMode.HTML
        )
        return
    text = await message.reply("<b><blockquote>Lᴇᴛ ᴍᴇ ᴄʜᴇᴄᴋ 👀</blockquote></b>")
    banSts = await db.ban_user(userid)
    if banSts == True:
        await text.edit(
    text=f"<b><code>{userid}</code> ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\n\nSʜᴏᴜʟᴅ I sᴇɴᴅ ᴀɴ ᴀʟᴇʀᴛ ᴛᴏ ᴛʜᴇ ʙᴀɴɴᴇᴅ ᴜsᴇʀ?</b>",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ʏᴇs ✅", callback_data=f"sendAlert_{userid}_{reason if reason else 'no reason provided'}"),
                InlineKeyboardButton("ɴᴏ ❌", callback_data=f"noAlert_{userid}"),
            ],
        ]
    ),
)
    else:
        await text.edit(f"<b>Cᴏɴᴛʀᴏʟʟ ʏᴏᴜʀ ᴀɴɢᴇʀ ʙʀᴏ...\n<code>{userid}</code> ɪs ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ !!</b>")
    return

#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP

 @Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def do_unban(bot, message):
    userid = message.text.split(" ", 2)[1] if len(message.text.split(" ", 2)) > 1 else None
    # Your logic here
if not userid:
    return await message.reply(
        '<blockquote>Gɪᴠᴇ ᴍᴇ ᴀɴ ɪᴅ\nᴇx : <code>/unban 1234567899</code></blockquote>'
    )

# Send an image before checking
await bot.send_photo(
    chat_id=message.chat.id,
    photo="https://i.ibb.co/BHqdCMCY/photo-2025-04-03-11-48-19-7489356433650090000.jpg",  # Replace with your own URL or Telegram file_id
    caption="🔓 Uɴʙᴀɴ Pʀᴏᴄᴇss Sᴛᴀʀᴛᴇᴅ..."
)

text = await message.reply("<b><blockquote>Lᴇᴛ ᴍᴇ ᴄʜᴇᴄᴋ 🥱</blockquote></b>")

unban_chk = await db.is_unbanned(userid)

if unban_chk == True:
    await text.edit(
        text=f'<b><blockquote><code>{userid}</code> ɪs ᴜɴʙᴀɴɴᴇᴅ\nSʜᴏᴜʟᴅ I sᴇɴᴅ ᴛʜᴇ ʜᴀᴘᴘʏ ɴᴇᴡs ᴀʟᴇʀᴛ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ?</blockquote></b>',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yᴇs ✅", callback_data=f"sendUnbanAlert_{userid}"),
                    InlineKeyboardButton("Nᴏ ❌", callback_data=f"NoUnbanAlert_{userid}"),
                ],
                [
                    InlineKeyboardButton("🔗 Vɪᴇᴡ Iᴍᴀɢᴇ", url="https://i.ibb.co/BHqdCMCY/photo-2025-04-03-11-48-19-7489356433650090000.jpg")
                ]
            ]
        )
    )

elif unban_chk == False:
    await text.edit('<b><blockquote>Usᴇʀ ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ ʏᴇᴛ.</blockquote></b>')
else:
    await text.edit(
        f"<b><blockquote>Fᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴜsᴇʀ/ᴄʜᴀɴɴᴇʟ.\nʀᴇᴀsᴏɴ : {unban_chk}</blockquote></b>"
    )


#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP
