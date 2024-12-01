import os
import json
from pyrogram import *
from pyrogram.types import *
import re


async def make_answers(client, m, MESSGAE_TO_FORMAT, *args):
    if args:
        try:
            user_id = args[0].id
            if args[0].first_name:
                first_name = args[0].first_name
            else:
                first_name = ""
            if args[0].last_name:
                last_name = args[0].last_name
            else:
                last_name = ""
            if args[0].username:
                user_name = args[0].username
            else:
                user_name = ""

            full_name = f"""{first_name} {last_name}"""
            mention = f"""[{first_name}](tg://user?id={user_id})"""
            group = m.chat.title

        except Exception as e1:
            print(e1)
            pass
    elif m.reply_to_message:
        try:
            if m.reply_to_message.from_user.id:
                user_id = m.reply_to_message.from_user.id
            else:
                user_id = ''
            if m.reply_to_message.from_user.first_name:
                first_name = str(m.reply_to_message.from_user.first_name)
            else:
                first_name = ''
            if m.reply_to_message.from_user.last_name:
                last_name = str(m.reply_to_message.from_user.last_name)
            else:
                last_name = ''
            if m.reply_to_message.from_user.username:
                user_name = str(m.reply_to_message.from_user.username)
            else:
                user_name = ''

            full_name = f"""{first_name} {last_name}"""
            mention = f"""[{first_name}](tg://user?id={user_id})"""
            group = m.chat.title

        except Exception as e1:
            print(f"Decode names ERROR:\n{e1}")
            pass
    else:
        try:
            if m.from_user.id:
                user_id = m.from_user.id
            else:
                user_id = ''
            if m.from_user.first_name:
                first_name = str(m.from_user.first_name)
            else:
                first_name = ''
            if m.from_user.last_name:
                last_name = str(m.from_user.last_name)
            else:
                last_name = ''
            if m.from_user.username:
                user_name = str(m.from_user.username)
            else:
                user_name = ''

            full_name = f"""{first_name} {last_name}"""
            mention = f"""[{first_name}](tg://user?id={user_id})"""
            group = m.chat.title
        except Exception as e:
            print(e)
            pass
    try:        
        if "{id}" in MESSGAE_TO_FORMAT:
            MESSGAE_TO_FORMAT = re.sub(
                "{id}", f"{user_id}", MESSGAE_TO_FORMAT)
        if "{first}" in MESSGAE_TO_FORMAT:
            MESSGAE_TO_FORMAT = re.sub(
                "{first}", f"{first_name}", MESSGAE_TO_FORMAT)
        if "{last}" in MESSGAE_TO_FORMAT:
            MESSGAE_TO_FORMAT = re.sub(
                "{last}", f"{last_name}", MESSGAE_TO_FORMAT)
        if "{username}" in MESSGAE_TO_FORMAT:
            if len(user_name) < 1:
                MESSGAE_TO_FORMAT = re.sub(
                    "{username}", "", MESSGAE_TO_FORMAT)
            else:
                MESSGAE_TO_FORMAT = re.sub(
                    "{username}", f"@{user_name}", MESSGAE_TO_FORMAT)
        if "{mention}" in MESSGAE_TO_FORMAT:
            MESSGAE_TO_FORMAT = re.sub(
                "{mention}", f"{mention}", MESSGAE_TO_FORMAT)
        if "{group}" in MESSGAE_TO_FORMAT:
            MESSGAE_TO_FORMAT = re.sub(
                "{group}", f"{group}", MESSGAE_TO_FORMAT)

        return MESSGAE_TO_FORMAT
    except Exception as e3:
        print(e3)
        return None
