import os
import json
from pyrogram import *
from pyrogram.types import *
import re
from config import my_bot_id
from group_bot.modules.admin_check import is_admin, can_delete, can_restrict, immutable, adminlist
from group_bot import mention_html, bot
import time
from config import *


async def reports(client, m):
    if m.reply_to_message:
        chat_id = m.chat.id
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["report"] is not True:
            return
        try:
            await m.delete()
        except:
             await m.reply_text("I haven't got permissions to delete messages !")
        if m.sender_chat:
            user_id = m.sender_chat.id
        else:
            user_id = m.from_user.id
        if await immutable(client, m, m.chat.id, user_id) is True:
            return
        if m.reply_to_message.sender_chat:
            user_id1 = m.reply_to_message.sender_chat.id
        else:
            user_id1 = m.reply_to_message.from_user.id
        if await immutable(client, m, m.chat.id, user_id1) is True:
            return
        elif m and m.reply_to_message:
            culprit_id = m.reply_to_message.from_user.id
            culprit = await mention_html(
                culprit_id, m.reply_to_message.from_user.first_name)
            chat_id = m.chat.id
            admin_ids = []
            dont_tag_me = []
            mention_string = ""
            dont_tag_me = obj[f"{bot_id}"]['dont_mention_admins']
            adminlists = await adminlist(client, m, chat_id)
            for dn in adminlists:
                if dn not in dont_tag_me:
                    mention_string = "".join([await mention_html(dn, "\u200D")])
            if culprit_id == m.from_user.id:
                pass
            if culprit_id == my_bot_id:
                pass
            elif culprit_id in admin_ids:
                pass
            else:
                admin_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=f"Ignore", callback_data=f"{culprit_id}_ignore"), 
                        InlineKeyboardButton(text=f"warn", callback_data=f"{culprit_id}_warn"),
                        InlineKeyboardButton(text=f"ban", callback_data=f"{culprit_id}_rban"), ],
                    [InlineKeyboardButton(text=f"delete", callback_data=f"{culprit_id}_delete"), InlineKeyboardButton(
                     text="mute", callback_data=f"{culprit_id}_mute"),
                    InlineKeyboardButton(text=f"fban", callback_data=f"{culprit_id}_rfban"), ],
                ])

                await client.send_message(chat_id=chat_id, reply_to_message_id=m.reply_to_message.id,
                                          text=mention_string + f"{culprit} has been reported to admins !", parse_mode="html", reply_markup=admin_keyboard)


async def dreport(client, m):
    if m and not m.reply_to_message:
        chat_id = m.chat.id
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["report"] is not True:
            return
        if m.sender_chat:
            user_id = m.sender_chat.id
        else:
            user_id = m.from_user.id
        if await immutable(client, m, m.chat.id, user_id) is True:
            admins_list = obj[f"{bot_id}"]['dont_mention_admins']
            if user_id in admins_list:
                await m.reply_text(
                    "You weren't getting notified either !", quote=True)
            else:
                admins_list.append(int(user_id))
                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                    json.dump(obj, wf, indent=4)
                await m.reply_text(
                    f"Ok ,You aren't not gonna mention on reports !", parse_mode='MARKDOWN', quote=True)


async def mreport(client, m):
    if m and not m.reply_to_message:
        chat_id = m.chat.id
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["report"] is not True:
            return
        if m.sender_chat:
            user_id = m.sender_chat.id
        else:
            user_id = m.from_user.id
        if await immutable(client, m, m.chat.id, user_id) is True:
            admins_list = obj[f"{bot_id}"]['dont_mention_admins']
            if user_id not in admins_list:
                await m.reply_text(
                    "You are already being notified !", quote=True)
            else:
                admins_list.remove(int(user_id))
                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                    json.dump(obj, wf, indent=4)
                await m.reply_text(
                    f"Ok ,You will be getting mention on reports !", parse_mode='MARKDOWN', quote=True)
