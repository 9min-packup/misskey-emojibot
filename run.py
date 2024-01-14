import json
from emojibot import *

CONFIG_FILE = "config.json"

try :
    with open(CONFIG_FILE) as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"{CONFIG_FILE}ファイルがありません")
    exit()

bot = EmojiBot(config)
bot.run()