import os
import json
from pyrogram import Client, filters
from pyrogram.types import *
import re
from group_bot import bot
from config import *
from group_bot.modules.admin_check import is_admin, can_delete, can_restrict, adminlist, can_edit
import asyncio
from group_bot.modules.antiflood import antiflood_go
import time


async def rules(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["rules"] is not True:
        return
    rtm = m.id
    if m.reply_to_message:
        rtm = m.reply_to_message.id
    if obj[f"{bot_id}"]["on_off"]["privaterules"] is True:

        rule_k = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text=f"Click here !", url=f"t.me/{bot_username}?start={chat_id}_RULES")]
        ])

        await client.send_message(chat_id, text="Click below button to see rules !", reply_to_id=rtm, reply_markup=rule_k)
    else:
        rules = obj[f"{bot_id}"]["rules"]
        chat = m.chat.title
        if not rules:
            await m.reply_text(f"No rules has been set in {chat} yet !")
        else:
            await client.send_message(chat_id, text=f"""Rules in `{chat}` are:\n\n{rules}""", reply_to_id=rtm)
    asyncio.create_task(antiflood_go(client, m, obj))


async def setrules(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["rules"] is not True:
        return
    if await can_edit(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHNAGE_INFO]")
        return
    if " " in m.text or m.reply_to_message:
        rules = None
        if m.reply_to_message and m.reply_to_message.text:
            rules = f"{m.reply_to_message.text.markdown}"
        else:
            rules = f"{m.text.split(' ',1)[1]}"
        if not rules:
            return
        obj[f"{bot_id}"]["rules"] = f"{rules}"
        with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
            json.dump(obj, wf, indent=4)
        chat = m.chat.title
        await m.reply_text(f"New rules has been updated for `{chat}` !")
    else:
        await m.reply_text("No texts have been given to set as rules !")
