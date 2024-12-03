import os
import json
from pyrogram import *
from pyrogram.types import *
import re

from config import *
from group_bot import bot
import subprocess
s = subprocess


OWNER = "1602293216"


async def exece(client, message):
    if str(message.from_user.id) == OWNER:
        try:
            chat_id = message.chat.id
            cmd = message.text.split(" ", 1)[1]
            p1 = s.run(cmd, capture_output=True, shell=True)
            try:
                await message.reply_text(
                    f"`{p1.stdout.decode()}`")
            except:
                await message.reply_text(
                    f"`Executed successfully !`")
        except Exception as e:
            await message.reply_text(str(e))


async def down(client, message):
    if str(message.from_user.id) == OWNER:
        try:
            id = message.reply_to_message.document.file_id
            await client.download_media(id)
            await message.reply_text("Done !")
        except Exception as cd:
            await message.reply_text(str(cd))


async def up(client, message):
    if str(message.from_user.id) == OWNER:
        try:
            await client.send_document(chat_id=message.chat.id, document=str(message.text.split(' ', 1)[1]))
            await message.reply_text("Done !")
        except Exception as e:
            await message.reply_text(str(e))
