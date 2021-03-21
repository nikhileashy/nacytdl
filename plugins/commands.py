# Code Rewrited By Jijinr 
# Heroku Support Added By Jijinr

from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config


@Client.on_message(filters.command(["start"])
                   & (filters.chat(Config.GROUP_ID) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_start(_, message: Message):
    """/start introduction of the bot"""
    await message.reply(Config.COMMANDS_TEXT_START)


@Client.on_message(filters.command(["help"])
                   & (filters.chat(Config.GROUP_ID) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_help(_, message: Message):
    """/help usage of the bot"""
    await message.reply(Config.COMMANDS_TEXT_HELP)


@Client.on_message(filters.command(["json"])
                   & (filters.chat(Config.GROUP_ID) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_json(_, message: Message):
    """/json get user info"""
    await message.reply(f"<code>{message}</code>")


@Client.on_message(filters.command(["id"])
                   & (filters.chat(Config.GROUP_ID) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_id(_, message: Message):
    """/id get user info"""
    await message.reply(f"<code>{message.from_user}</code>")
