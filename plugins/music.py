# Code Rewrited By Jijinr 
# Heroku Support Added By Jijinr

import os
import asyncio
from datetime import timedelta
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from youtube_dl import YoutubeDL
from PIL import Image
import ffmpeg
from opencc import OpenCC
from config import Config
from config import Config

TG_THUMB_MAX_LENGTH = 320
REGEX_SITES = (
    r"^((?:https?:)?\/\/)"
    r"?((?:www|m)\.)"
    r"?((?:youtube\.com|youtu\.be|soundcloud\.com|mixcloud\.com))"
    r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$"
)
REGEX_EXCLUDE_URL = (
    r"\/channel\/|\/playlist\?list=|&list=|\/sets\/"
)
s2tw = OpenCC('s2tw.json').convert


@Client.on_message(filters.text
                   & (filters.chat(Config.GROUP_ID) | filters.private)
                   & filters.incoming
                   & filters.regex(REGEX_SITES)
                   & ~filters.regex(REGEX_EXCLUDE_URL)
                   & ~filters.edited)
async def music_downloader(client, message: Message):
    """Add members of specified chats to the list when it's a private
    chat
    """
    # print(' '.join([str(u) for u in Config.AUTH_USER]))
    if message.chat.type == "private":
        user_id = message.from_user.id
        if user_id not in Config.AUTH_USER:
            for chat in Config.GROUP_ID:
                try:
                    await client.get_chat_member(chat, user_id)
                    Config.AUTH_USER.append(user_id)
                    break
                except UserNotParticipant:
                    pass
        if user_id not in Config.AUTH_USER:
            await message.reply(Config.MUSIC_INFORM_AVAILABILITY)
            return
    await _fetch_and_send_music(message)


async def _fetch_and_send_music(message: Message):
    await message.reply_chat_action("typing")
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        ydl = YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(message.text, download=False)
        # send a link as a reply to bypass Music category check
        if not message.reply_to_message \
                and _youtube_video_not_music(info_dict):
            inform = ("__This won't be downloaded__"
                      "__because it's not under Music category__")
            await _reply_and_delete_later(message, inform,
                                          Config.MUSIC_DELAY_DELETE_INFORM)
            return
        if info_dict['duration'] > Config.MUSIC_MAX_LENGTH:
            readable_max_length = str(timedelta(seconds=Config.MUSIC_MAX_LENGTH))
            inform = ("__This won't be downloaded because its audio length is__"
                      "__longer than the limit__ `{}` __which is set by the bot__"
                      .format(readable_max_length))
            await _reply_and_delete_later(message, inform,
                                          Config.MUSIC_DELAY_DELETE_INFORM)
            return
        d_status = await message.reply_text("__Downloading...__", quote=True,
                                            disable_notification=True)
        ydl.process_info(info_dict)
        audio_file = ydl.prepare_filename(info_dict)
        task = asyncio.create_task(_upload_audio(message, info_dict,
                                                 audio_file))
        await message.reply_chat_action("upload_document")
        await _delay_delete_messages((d_status, message), Config.PING_DELAY_DELETE)
       # await d_status.delete()
        while not task.done():
            await asyncio.sleep(4)
            await message.reply_chat_action("upload_document")
        await message.reply_chat_action("cancel")
        if message.chat.type == "private":
            await message.delete()
    except Exception as e:
        await message.reply_text(repr(e))


def _youtube_video_not_music(info_dict):
    if info_dict['extractor'] == 'youtube' \
            and 'Music' not in info_dict['categories']:
        return True
    return False


async def _reply_and_delete_later(message: Message, text: str, delay: int):
    reply = await message.reply_text(text, quote=True)
    await asyncio.sleep(delay)
    await reply.delete()


async def _upload_audio(message: Message, info_dict, audio_file):
    basename = audio_file.rsplit(".", 1)[-2]
    if info_dict['ext'] == 'webm':
        audio_file_opus = basename + ".opus"
        ffmpeg.input(audio_file).output(audio_file_opus, codec="copy").run()
    thumbnail_url = info_dict['thumbnail']
    if os.path.isfile(basename + ".jpg"):
        thumbnail_file = basename + ".jpg"
    else:
        thumbnail_file = basename + "." + \
            _get_file_extension_from_url(thumbnail_url)
    squarethumb_file = basename + "_squarethumb.jpg"
    make_squarethumb(thumbnail_file, squarethumb_file)
    webpage_url = info_dict['webpage_url']
    title = s2tw(info_dict['title'])
    caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
    duration = int(float(info_dict['duration']))
    performer = s2tw(info_dict['uploader'])
    await message.reply_audio(audio_file_opus,
                              caption=caption,
                              duration=duration,
                              performer=performer,
                              title=title,
                              parse_mode='HTML',
                              thumb=squarethumb_file)
    for f in (audio_file, audio_file_opus, thumbnail_file, squarethumb_file):
        os.remove(f)


def _get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


def make_squarethumb(thumbnail, output):
    """Convert thumbnail to square thumbnail"""
    # https://stackoverflow.com/a/52177551
    original_thumb = Image.open(thumbnail)
    squarethumb = _crop_to_square(original_thumb)
    squarethumb.thumbnail((TG_THUMB_MAX_LENGTH, TG_THUMB_MAX_LENGTH),
                          Image.ANTIALIAS)
    squarethumb.save(output)


def _crop_to_square(img):
    width, height = img.size
    length = min(width, height)
    left = (width - length) / 2
    top = (height - length) / 2
    right = (width + length) / 2
    bottom = (height + length) / 2
    return img.crop((left, top, right, bottom))

async def _delay_delete_messages(messages: tuple, delay: int):
    await asyncio.sleep(delay)
    for msg in messages:
        await msg.delete()
