from pyrogram.types import *
from pyrogram import *
from group_bot import bot
import re
from config import bot_id
from group_bot.modules.helpers.welcome_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.db import create_db
import json
import time
from group_bot.modules.helpers.names import make_answers
import os
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
from group_bot.modules.helpers.null_helper import null_sender
import asyncio

on_off = ['on', 'off', 'yes', 'no']


async def setwelcome(client, m, *args):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        chat_id = m.chat.id
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["greetings"] is True:
            if await can_edit(client, m, m.chat.id, user_id) is not True:
                await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
                return
            chat_id = m.chat.id
            if m.reply_to_message and m.reply_to_message.reply_markup:
                return1 = await _markup(client, m)
            else:
                return1 = await _markup2(client, m)
            btn_url = return1[0]
            if len(str(btn_url)) < 10:
                btn_url = None
            text = return1[1]
            if len(str(text)) < 1:
                text = None
            typee = return1[2]
            file_id = return1[3]
            if len(str(file_id)) < 10:
                file_id = None
            disable_link_preview = True
            disable_link_preview = return1[4]
            if not text and not file_id:
                await m.reply_text("Welcome message shouldn't be empty !")
                return
            new_obj = {"text": text, "btn_url": btn_url, "file_id": file_id,
                       "typee": typee, "disable_link_preview": disable_link_preview}
            if args:
                del obj[f"{bot_id}"]['2nd_welcome'][0]
                obj[f"{bot_id}"]['2nd_welcome'].append(new_obj)
                new_2 = "2nd "
            else:
                del obj[f"{bot_id}"]['welcome'][0]
                obj[f"{bot_id}"]['welcome'].append(new_obj)
                new_2 = ""
            with open(f"db/X{chat_id}_db.txt", 'w+') as ff:
                json.dump(obj, ff, indent=4)
            await m.reply_text(
                f"New {new_2}welcome message has been added !")
        else:
            await create_db(chat_id)
            await setwelcome(client, m)


async def setgoodbye(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        chat_id = m.chat.id
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["greetings"] is not True:
            return
        if await can_edit(client, m, m.chat.id, user_id) is True:
            chat_id = m.chat.id
            if m.reply_to_message and m.reply_to_message.reply_markup:
                return1 = await _markup(client, m)
            else:
                return1 = await _markup2(client, m)
            btn_url = return1[0]
            if len(str(btn_url)) < 10:
                btn_url = None
            text = return1[1]
            if len(str(text)) < 1:
                text = None
            typee = return1[2]
            file_id = return1[3]
            if len(str(file_id)) < 10:
                file_id = None
            disable_link_preview = True
            disable_link_preview = return1[4]
            new_obj = {"text": text, "btn_url": btn_url, "file_id": file_id,
                       "typee": typee, "disable_link_preview": disable_link_preview}
            with open(f"db/X{chat_id}_db.txt", 'r') as f:
                obj = json.load(f)
            del obj[f"{bot_id}"]['goodbye'][0]
            obj[f"{bot_id}"]['goodbye'].append(new_obj)
            with open(f"db/X{chat_id}_db.txt", 'w+') as ff:
                json.dump(obj, ff, indent=4)
            await m.reply_text(
                f"New goodbye message has been added !")
        else:
            create_db(chat_id)
            await setgoodbye(client, m)


async def welcome(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["greetings"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    msg = obj[f"{bot_id}"]["welcome"][0]
    asyncio.create_task(null_sender(
        client, m, msg, chat_id))


async def resetwelcome(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["greetings"] is not True:
        return
    if await can_edit(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
        return
    default_w = {
        "text": "Hey {mention} !\nWelcome to {group} . Have a nice day :)",
        "btn_url": None,
        "file_id": None,
        "typee": 0,
        "disable_link_preview": True
    }
    chat_id = m.chat.id
    if os.path.isfile(f"db/X{chat_id}_db.txt"):
        try: 
            if args:
                obj[f"{bot_id}"]['2nd_welcome'].clear()
                obj[f"{bot_id}"]['2nd_welcome'].append(default_w)
                n_2 = "2nd "
            else:
                obj[f"{bot_id}"]['welcome'].clear()
                obj[f"{bot_id}"]['welcome'].append(default_w)
                n_2 = ""

            with open(f"db/X{chat_id}_db.txt", 'w+') as wf:                
                json.dump(obj, wf, indent=4)
            await m.reply_text(
                "{n_2}Welcome Message has been reset to default !", quote=True)
        except Exception as w:
            await m.reply_text(str(w), quote=True)


async def resetgoodbye(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["greetings"] is not True:
        return
    if await can_edit(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
        return
    default_w = {
        "text": "Nice knowing you !",
        "btn_url": None,
        "file_id": None,
        "typee": 0,
        "disable_link_preview": True
    }
    chat_id = m.chat.id
    if os.path.isfile(f"db/X{chat_id}_db.txt"):
        try:
            with open(f"db/X{chat_id}_db.txt", 'r+') as f:
                obj = json.load(f)
                obj[f"{bot_id}"]['goodbye'].clear()

            with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                obj[f"{bot_id}"]['goodbye'].append(default_w)
                json.dump(obj, wf, indent=4)
            await m.reply_text(
                "Goodbye Message has been reset to default !", quote=True)
        except Exception as w:
            await m.reply_text(str(w), quote=True)
