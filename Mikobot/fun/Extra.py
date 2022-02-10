import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Mikobot import app
from pyrogram.errors import RPCError
from speedtest import Speedtest
from pyrogram.types import InputMediaPhoto
import aiohttp
import os
from pyrogram import filters
from Mikobot.modules.admin import adminsOnly 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from requests import get
import requests
import pytz
import datetime
from Mikobot.utils.dbfunctions import get_served_chats, get_served_users
# url shortner
from pyrogram import filters
from Mikobot import app
import requests



picmetxt = """
🔥 **Simple Logo & Image Tool** ✨
✌️**Pic me**👀 : `Capture Your Profile Picture`
👨‍💻**Logo For Me** 🙈 : `Generate Logo With Your Name`
🌷 Wallpapers : `Generate HD Wallpapers`
◇️ ━━━━━━━━━ ◇️
👨‍💻 **Generated By**: [szMikobotbot](https://t.me/szMikobotbot)
🙋‍♂️ **Requestor** : {}
⚡️ **Powered By**   : [szteambots](https://t.me/szteambots)
◇️ ━━━━━━━━━ ◇️
**©2022** [@szMikobotbot](http://t.me/szMikobotbot) **Bot All Rights Reserved**
"""

picmebtns = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("◇─────────────────◇", callback_data="picme not")           
                ],        
                [
                    InlineKeyboardButton("◈──✌️Pic me👀──◈", callback_data="picme me")
                ],
                [
                    InlineKeyboardButton("◈──👨‍💻Logo For Me 🙈──◈", callback_data="picme new")           
                ],
                [
                    InlineKeyboardButton("◈──🌺Wallpaper🌺──◈", callback_data="picme wall")           
                ],
                [
                    InlineKeyboardButton("◈──💁‍♂️Send Pm ──◈", callback_data="picme pm")
                ],
                [
                    InlineKeyboardButton("◈──👮‍♀️ About Me 👮‍♀️──◈", callback_data="picme why")           
                ],
                [
                    InlineKeyboardButton("✘【SZ™】✘Support Chat", url="https://t.me/slbotzone"),
                    InlineKeyboardButton("✘【SZ™】✘Updates Channel", url="https://t.me/szteambots")       
                ],         
            ]
        )
pm = """
✍️ **Logo Generated Successfully**✅
◇───────────────◇
👨‍💻 **Generated By** : [szMikobotbot](https://t.me/szMikobotbot)
🙋‍♂️ **Requestor** : {}
⚡️ **Powered By**   : [szteambots](https://t.me/szteambots)
◇───────────────◇️
**©2022** [@szMikobotbot](http://t.me/szMikobotbot) **Bot All Rights Reserved**
"""

CHANNEL = -1001325914694

@app.on_message(filters.command("picme") & filters.user([1441379756,1467358214]))
async def sendthepicme(_, message):
    await app.send_photo(chat_id=int(CHANNEL),photo="https://telegra.ph/file/1f393138c4a4d4199e9df.jpg",caption=picmetxt.format(message.from_user.mention), reply_markup=picmebtns)

@app.on_callback_query(filters.regex("picme"))
async def mylogo(_, query):
    mode = query.data.split()[1].strip()
    picmetext = picmetxt.format(query.from_user.mention)
    if mode == "me" and query.from_user.photo:
        await query.answer("⚙️Capture started....", show_alert=True)
        photoid = query.from_user.photo.big_file_id  
        photo = await app.download_media(photoid)
        await query.edit_message_media(InputMediaPhoto(media=photo, caption=picmetext), reply_markup=picmebtns)
        if os.path.exists(photo):os.remove(photo)
    if mode == "why" or not query.from_user.photo:
        Time_Zone = "Asia/Kolkata"
        zone = datetime.datetime.now(pytz.timezone(f"{Time_Zone}"))  
        timer = zone.strftime("%I:%M %p")
        dater = zone.strftime("%b %d")    
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        await query.answer(f"""
My informations here 👮‍♀️
⏱ Latest Update Time : 2022 {dater}:{timer}
📊 User Count : {served_users} 
📖 Total Groups : {served_chats}
🎭 Powerd By @szteambots
""", show_alert=True)
    if mode == "new" or not query.from_user.photo:
        await query.answer("⚙️ Creating Your logo..", show_alert=True)
        api = get(f"https://api.single-developers.software/logo?name={query.from_user.first_name}")
        await query.edit_message_media(InputMediaPhoto(media=api.url, caption=picmetext), reply_markup=picmebtns)
    if mode == "wall" or not query.from_user.photo:
        await query.answer("⚙️ Creating Your Wallpaper...", show_alert=True)
        q = "none"
        api = requests.get(f"https://single-developers.herokuapp.com/wallpaper?search={q}".json())
        await query.edit_message_media(InputMediaPhoto(media=api.url, caption=picmetext), reply_markup=picmebtns)
    if mode == "pm":
        try:
            photo = await app.download_media(query.message.photo.file_id)
            await app.send_photo(query.from_user.id, photo=photo, caption=pm.format(query.from_user.mention))
            if os.path.exists(photo):os.remove(photo)   
            return await query.answer("🥲 Sent to PM, Check your pm now.", show_alert=True) 
        except Exception as e:
            await query.answer("Please Frist Start This 👉 @szMikobotbot")
            print(str(e))
            if os.path.exists(photo):os.remove(photo)     





@app.on_message(filters.command("speedtest") & ~filters.edited)
async def statsguwid(_, message):
    m = await message.reply("__running__")
    speed = Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    img = speed.results.share()
    cap = "Here are the results of speedtest \n" + ('Ping: %s ms\nDownload: %0.2f M%s/s\nUpload: %0.2f M%s/s' %
          (speed.results.ping,
          (speed.results.download / 1000.0 / 1000.0) / units[1],
          units[0],
          (speed.results.upload / 1000.0 / 1000.0) / units[1],
          units[0]))
    await message.reply_photo(photo=img, caption=cap)
    await m.delete()
    
@app.on_message(filters.command("send") & ~filters.edited)
async def send(_, message):
    chat_id = message.chat.id   
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Use /send with text or by replying to message.")
    if message.reply_to_message:
        if len(message.command) > 1:
            send = message.text.split(None, 1)[1]
            reply_id = message.reply_to_message.message_id
            return await app.send_message(chat_id, 
                         text = send, 
                         reply_to_message_id=reply_id)
        else:
           return await message.reply_to_message.copy(chat_id) 
    else:
        await app.send_message(chat_id, text=message.text.split(None, 1)[1])
        
  

__MODULE__ = "Extras"
__HELP__ = """
× /couple 
        To Choose Couple Of The Day
× /crypto [currency]
        Get Real Time value from currency given.
× /dice : Roll a dice.       
× /info [USERNAME|ID]:  Get info about a user.
× /chat_info [USERNAME|ID] : Get info about a chat.  
× /paste : To Paste Replied Text Or Document To A Pastebin
× /proxy : Get socks5 proxy which you can
× /q : To quote a message.
× /q [INTEGER] : To quote more than 1 messages.
× /q r : to quote a message with it's reply
× /reddit [query] : results something from reddit
× /repo : To Get My Github Repository Link " "And Support Group Link
× /send `[text or reply or both]` : Send as bot.
× /speedtest : test bot speed
× /github [username] : get github user info
"""
__funtools__ = __HELP__
  