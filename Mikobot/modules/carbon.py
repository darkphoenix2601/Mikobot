from pyrogram import filters
from Mikobot import app
from Mikobot.core.decorators.errors import capture_err
from Mikobot.utils.functions import make_carbon


@app.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a text message to make carbon."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Reply to a text message to make carbon."
        )
    m = await message.reply_text("Preparing Carbon")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("Uploading")
    await app.send_document(message.chat.id, carbon)
    await m.delete()
    carbon.close()

__MODULE__ = "carbon"
__HELP__ = """
× /carbon : make carbon of any text
 """
__funtools__ = __HELP__
