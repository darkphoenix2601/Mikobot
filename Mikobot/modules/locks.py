from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import ChatNotModified
from pyrogram.types import ChatPermissions

from Mikobot import SUDOERS, app
from Mikobot.core.decorators.errors import capture_err
from Mikobot.core.decorators.permissions import adminsOnly
from Mikobot.modules.admin import current_chat_permissions, list_admins
from Mikobot.utils.functions import get_urls_from_text

__MODULE__ = "Locks"
__HELP__ = """

**Admin only:**
× /lock `[Parameters]`
× /unlock `[Parameters]`
× /locks [No Parameters Required]
× /locktypes: Check available lock Parameters!

**Parameters:**
    - messages 
    - stickers 
    - gifs 
    - media 
    - games 
    - polls
    - inline 
    - url 
    - group_info 
    - user_add 
    - pin
    
**Example:** /lock all
You can only pass the "all" parameter with /lock, not with /unlock
"""
__basic_cmds__ = __HELP__

incorrect_parameters = "Incorrect Parameters, Check Locks Section In Help."
# Using disable_preview as a switch for url checker
# That way we won't need an additional db to check
# If url lock is enabled/disabled for a chat
data = {
    "messages": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "group_info": "can_change_info",
    "useradd": "can_invite_users",
    "pin": "can_pin_messages",
}


async def tg_lock(message, permissions: list, perm: str, lock: bool):
    if lock:
        if perm not in permissions:
            return await message.reply_text("Already locked.")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.reply_text("Already Unlocked.")
        permissions.append(perm)

    permissions = {perm: True for perm in list(set(permissions))}

    try:
        await app.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.reply_text(
            "To unlock this, you have to unlock 'messages' first."
        )

    await message.reply_text(("Locked." if lock else "Unlocked."))


@app.on_message(filters.command(["lock", "unlock"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def locks_func(_, message):
    if len(message.command) != 2:
        return await message.reply_text(incorrect_parameters)

    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()

    if parameter not in data and parameter != "all":
        return await message.reply_text(incorrect_parameters)

    permissions = await current_chat_permissions(chat_id)

    if parameter in data:
        await tg_lock(
            message,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        await app.set_chat_permissions(chat_id, ChatPermissions())
        await message.reply_text(f"Locked Everything in {message.chat.title}")

    elif parameter == "all" and state == "unlock":
        await app.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False,
            ),
        )
        await message.reply(f"Unlocked Everything in {message.chat.title}")

@app.on_message(filters.command("locks") & ~filters.private)
@capture_err
async def locktypes(_, message):
    permissions = await current_chat_permissions(message.chat.id)

    if not permissions:
        return await message.reply_text("No Permissions.")

    perms = ""
    for i in permissions:
        perms += f"×**{i}**\n"

    await message.reply_text(perms)

@app.on_message(filters.command("locktypes") & ~filters.private)
@capture_err
async def locktpes(_, message):
    msg = """  
    - messages 
    - stickers 
    - gifs 
    - media 
    - games 
    - polls
    - inline 
    - url 
    - group_info 
    - user_add 
    - pin"""
    await message.reply_text(msg)

@app.on_message(filters.text & ~filters.private, group=69)
async def url_detector(_, message):
    user = message.from_user
    chat_id = message.chat.id
    text = message.text.lower().strip()

    if not text or not user:
        return
    if user.id in (SUDOERS + (await list_admins(chat_id))):
        return

    check = get_urls_from_text(text)
    if check:
        permissions = await current_chat_permissions(chat_id)
        if "can_add_web_page_previews" not in permissions:
            try:
                await message.delete()
            except Exception:
                await message.reply_text(
                    "This message contains a URL, "
                    + "but i don't have enough permissions to delete it"
                )
