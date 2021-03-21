# Code Rewrited By Jijinr 
# Heroku Support Added By Jijinr

import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from config import Config

WELCOME_DELAY_KICK_SEC = Config.WELCOME_DELAY_KICK_MIN * 60


@Client.on_message(filters.chat(Config.GROUP_ID) & filters.new_chat_members)
async def welcome(_, message: Message):
    """Mute new member and send message with button"""
    new_members = [f"{u.mention}" for u in message.new_chat_members]
    text = (f"__Welcome,__ {', '.join(new_members)}\n**Are you human?**\n"
            "__You will be removed from this chat if you are not verified__"
            f"__in__ {Config.WELCOME_DELAY_KICK_MIN} __min__")
    await message.chat.restrict_member(message.from_user.id, ChatPermissions())
    button_message = await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Press Here to Verify",
                        callback_data="pressed_button"
                    )
                ]
            ]
        ),
        quote=True
    )
    await kick_restricted_after_delay(WELCOME_DELAY_KICK_SEC, button_message)


@Client.on_callback_query(filters.regex("^pressed_button$"))
async def callback_query_welcome_button(_, callback_query):
    """After the new member press the button, set his permissions to
    chat permissions, delete button message and join message
    """
    button_message = callback_query.message
    join_message = button_message.reply_to_message
    pending_user = join_message.from_user
    pending_user_id = pending_user.id
    pressed_user_id = callback_query.from_user.id
    if pending_user_id == pressed_user_id:
        await callback_query.answer("Congrats, verification passed!")
        await button_message.chat.unban_member(pending_user_id)
        await button_message.delete()
        await join_message.delete()
    else:
        await callback_query.answer(f"This is for {pending_user.first_name}")


async def kick_restricted_after_delay(delay, button_message: Message):
    """If the new member is still restricted after the delay, delete
    button message and join message and then kick him
    """
    await asyncio.sleep(delay)
    join_message = button_message.reply_to_message
    group_chat = button_message.chat
    user_id = join_message.from_user.id
    await join_message.delete()
    await button_message.delete()
    await _ban_restricted_user_until_date(group_chat, user_id, duration=delay)


@Client.on_message(filters.chat(Config.GROUP_ID) & filters.left_chat_member)
async def left_chat_member(_, message: Message):
    """When a restricted member left the chat, ban him for a while"""
    group_chat = message.chat
    user_id = message.left_chat_member.id
    await _ban_restricted_user_until_date(group_chat, user_id,
                                          duration=WELCOME_DELAY_KICK_SEC)


async def _ban_restricted_user_until_date(group_chat,
                                          user_id: int,
                                          duration: int):
    try:
        member = await group_chat.get_member(user_id)
        if member.status == "restricted":
            until_date = int(datetime.utcnow().timestamp() + duration)
            await group_chat.kick_member(user_id, until_date=until_date)
    except UserNotParticipant:
        pass
