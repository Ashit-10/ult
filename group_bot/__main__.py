import os
import asyncio
from . import *
from config import *
from pyrogram import idle
from group_bot.modules.helpers.welcome_sender import sj

def main():
    print("starting... ")
    bot.start()
    try:
        with open("re.txt", "r") as red:
            mid = red.read()
        chat_id = mid.split('_')[0]
        msg_id = mid.split('_')[1]
        bot.edit_message_text(chat_id=chat_id,
                              message_id=int(msg_id), text="Restarted !")
        os.remove("re.txt")
    except Exception as tc:
        pass
    sj.start()
    bot2.start()
    secure_me()
    print("Started !")
    idle()
    bot.stop()
    bot2.stop()

if __name__ == "__main__":
    main()
