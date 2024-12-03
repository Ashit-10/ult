from pyrogram import *
from pyrogram.types import *
from config import *
from group_bot import bot
import json
import os
import time


async def users_id(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["id"] is not True:
        return
    user_id = None
    text = None
    if m.reply_to_message:
        try:
            user_id = m.reply_to_message.from_user.id
            if m.reply_to_message.from_user.first_name:
                fname = m.reply_to_message.from_user.first_name
            else:
                fname = m.reply_to_message.from_user.last_name
            await m.reply_text(
                f"{fname}'s ID is `{user_id}`")
            return
        except:
            user_id = m.reply_to_message.sender_chat.id
            fname = m.reply_to_message.sender_chat.title
            await m.reply_text(
                f"{fname}'s ID is `{user_id}`")
            return
    else:
        if ' ' in m.text:
            if str(m.text.split()[1]).startswith('@'):
                try:
                    per_id = await client.get_chat(str(m.text.split()[1]))
                    user_id = per_id.id
                    fname = per_id.first_name
                    if not fname:
                        fname = per_id.title
                    try:
                        if len(str(ord(str(fname)))) > 3:
                            fname = "User"
                    except:
                        pass
                    await m.reply_text(
                        f"{fname}'s ID is `{user_id}`")
                    return
                except:
                    await m.reply_text(
                        f"Invalid username !")
                    return
            try:
                user_id = m.entities[1].user.id
                fname = m.entities[1].user.first_name
                await m.reply_text(
                    f"{fname}'s ID is `{user_id}`")
                return
            except Exception as e:
                print(e)
                pass
        else:
            user_id = m.chat.id
            await m.reply_text(
                f"This chat's ID is `{user_id}`")
            return


async def return_id(client, m):
    user_id = None
    text = None
    if m.reply_to_message:
        if m.reply_to_message.sender_chat:
            user_id = m.reply_to_message.sender_chat.id
        else:
            user_id = m.reply_to_message.from_user.id
        if ' ' in m.text:
            text = m.text.split(' ', 1)[1]
        return user_id, text
    else:
        if ' ' in m.text:                    
            if m.entities:                          
                if len(m.entities) > 0 and str(m.text.split()[1]).startswith("@"):                    
                    uid = m.text.split()[1]
                    pid2 = await client.get_chat(uid)
                    user_id = pid2.id
                    if len(m.text.split()) > 2:              
                        text = str(m.text.split(' ', 2)[2])
                    else:
                        text = None                    
                    return user_id, text
                elif len(m.entities) > 1 and m.entities[1].type == "text_mention":
                    if m.entities[1].offset <= (len(str(m.text.split()[0])) + 2):
                        user_id = m.entities[1].user.id
                        text = m.text[(m.entities[1].offset +
                                       m.entities[1].length):]
                        if len(str(text)) < 1:
                            text = None
                    return user_id, text

                elif len(m.entities) > 1 and m.entities[1].type == "mention":
                    if m.entities[1].offset <= (len(str(m.text.split()[0])) + 2):
                        pid = m.text[(m.entities[1].offset):(
                            m.entities[1].offset + m.entities[1].length)]
                        pid2 = await client.get_chat(pid)
                        user_id = pid2.id
                        text = m.text[(m.entities[1].offset + 1 +
                                       m.entities[1].length):]
                        if len(str(text)) < 1:
                            text = None
                    return user_id, text

            
            if not user_id:
                try:
                    user_id = int(m.text.split()[1])
                    try:
                        text = m.text.split(' ', 2)[2]
                    except:
                        pass
                    return user_id, text
                except:
                    return user_id, text
