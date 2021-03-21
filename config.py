import os

class Config(object):

    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    AUTH_USER = [id for id in os.environ.get("AUTH_USER").split(" ")]
    GROUP_ID = int(os.environ.get("GROUP_ID", 12345))
    CHANNEL_FORWARD_TO = int(os.environ.get("CHANNEL_FORWARD_TO", 12345))
    MUSIC_MAX_LENGTH = 10800
    MUSIC_DELAY_DELETE_INFORM = 10
    PING_DELAY_DELETE = 8
    WELCOME_DELAY_KICK_MIN = 2

# Commands Translation

    COMMANDS_TEXT_START = """<i>This is a music downloader bot for 
members of the channel and group</i>"""
    COMMANDS_TEXT_CONTACTS = """<i>Regarding any issues with the bot 
feel free to contact</i>"""
    COMMANDS_TEXT_HELP = """
<b>This is a music downloader bot for members of the channel and group</b>

<b>Usage</b>:\n
<i>- Send a message that only contains a YouTube/SoundCloud/Mixcloud link 
to download the music</i>\n
<i>- Playlists are not supported</i>\n
<i>- Your message will be deleted in private chat after the music gets 
successfully uploaded</i>\n
<i>- You can get YouTube links with inline bot @vid</i>\n
<i>- You can sent your YouTube Link in Group Only</i>\n\n
<b>This bot only serves the specified group and 
its members in private chat</b>"""
    MUSIC_INFORM_AVAILABILITY = """<b>This bot only serves the specified group and 
its members in private chat</b>"""

