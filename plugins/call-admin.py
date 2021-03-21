# Code Rewrited By Jijinr 
# Heroku Support Added By Jijinr

from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config


@Client.on_message(filters.command("admin", "@")
                   & filters.chat(Config.GROUP_ID)
                   & filters.incoming
                   & ~filters.edited)
async def call_admin(client, message: Message):
    if message.sender_chat or (message.reply_to_message
                               and message.reply_to_message.sender_chat):
        return
    u_call = message.from_user
    await message.reply_text(f"<b>Hey admins,</b> {u_call.mention()} "
                             "<b>asked me to call you!</b>")
    text = message.text.markdown.removeprefix('@admin').removeprefix(' ')
    m_link = message.link
    for user in Config.AUTH_USER:
        await client.send_message(
            user,
            f"**{u_call.mention()}**: "
            f"{text}\n{m_link}"
        )
