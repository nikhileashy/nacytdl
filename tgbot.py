# Code Rewrited By Jijinr 
# Heroku Support Added By Jijinr

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
import os

from config import Config

from pyrogram import Client

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )

    app = Client(
        "tgbot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        workers=75,
        plugins=plugins
    )
    app.run()
