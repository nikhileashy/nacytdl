![image](https://telegra.ph/file/e3491a7de8ce33dec0cc8.jpg)

# YouTube Mp3 Bot

_This is a music downloader bot for 
members of the channel and group_

### Pre Requisites 

• _Your Bot Token From @BotFather_

• _Your APP ID And API Harsh From [Telegram](http://www.my.telegram.org) or [@UseTGXBot](http://www.telegram.dog/UseTGXBot)_

• _Your telegram id from [Rose Bot](https://t.me/MissRose_bot)_

• _Your Group ID_

• _Channel Id This is Not required_ 🤷

### Deploy:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Jijinr/YouTube-Mp3)

## tgbot

A Telegram bot made with [Pyrogram Smart Plugins](https://docs.pyrogram.org/topics/smart-plugins)

## Requirements

- Python 3.6 or higher (some plugins may require higher versions)
- A [Telegram API key](//docs.pyrogram.org/intro/setup#api-keys)
- A [Telegram bot token](//t.me/botfather)

## Run

1. `virtualenv venv` to create a virtual environment
2. install `python3-devel zlib-devel libjpeg-turbo-devel libwebp-devel`,
   clear cache of pip (`~/.cache/pip` on linux distro)
   for building wheel for Pillow.
   `venv/bin/pip install -U -r requirements.txt` to install the requirements
3. Create a new `config.ini` file, copy-paste the following and replace the
   values with your own. Exclude or include plugins to fit your needs.
   Create `config.py` and add constants that are specified in module docstrings
   of enabled plugins.
   ```
   [pyrogram]
   api_id = 1234567
   api_hash = 0123456789abcdef0123456789abcdef
   bot_token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

   [plugins]
   root = plugins
   exclude = welcome
   ```
4. Run with `venv/bin/python tgbot.py`
5. Stop with <kbd>CTRL+C</kbd>

## License

AGPL-3.0-or-later
