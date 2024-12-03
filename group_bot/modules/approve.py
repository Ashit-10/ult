import json
from pyrogram import Client, filters
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
from group_bot.modules.give_id import return_id
from group_bot import bot, mention_html
from config import *


async def approve(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["approve"] is not True:
            return
        if await can_restrict(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_RESTRICT_MEMBERS]")
            return
        if m.reply_to_message or " " in m.text:
            try:
                user_id = (await return_id(client, m))[0]
                if await immutable(client, m, chat_id, user_id) is True:
                    await m.reply_text("He is already a admin or your channel , they don't need to be approved !")
                    return
                wuser = await client.get_chat(user_id)
                fname = wuser.title
                if not fname:
                    fname = wuser.first_name
                user = await mention_html(user_id, fname)
                chat = m.chat.title
                approvers = obj[f"{bot_id}"]["approved_channels_and_users"]
                if user_id not in approvers:
                    obj[f"{bot_id}"]["approved_channels_and_users"].append(
                        user_id)
                    with open(f"db/X{chat_id}_db.txt", 'w+') as ff:
                        json.dump(obj, ff, indent=4)
                    await m.reply_text(f"{user} has been approved in `{chat}` ! They will now be ignored by locks, antiflood and blocklists.")
                else:
                    await m.reply_text(f"{user} is already approved in `{chat}` !")
            except:
                await m.reply_text("User id not found !")
        else:
            await m.reply_text("Reply to user or mention him to approve him !")


async def disapprove(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["approve"] is not True:
            return
        if await can_restrict(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_RESTRICT_MEMBERS]")
            return
        if m.reply_to_message or " " in m.text:
            try:
                user_id = (await return_id(client, m))[0]
                if await immutable(client, m, chat_id, user_id) is True:
                    await m.reply_text("He is already a admin or your channel , they don't need to be approved !")
                    return
                wuser = await client.get_chat(user_id)
                fname = wuser.title
                if not fname:
                    fname = wuser.first_name
                user = await mention_html(user_id, fname)
                chat = m.chat.title
                approvers = obj[f"{bot_id}"]["approved_channels_and_users"]
                if user_id in approvers:
                    obj[f"{bot_id}"]["approved_channels_and_users"].remove(
                        user_id)
                    with open(f"db/X{chat_id}_db.txt", 'w+') as ff:
                        json.dump(obj, ff, indent=4)
                    await m.reply_text(f"{user} has been disapproved in `{chat}` ! They will now be ignored by locks, antiflood and blocklists.")
                else:
                    await m.reply_text(f"{user} was not approved in `{chat}` !")
            except:
                await m.reply_text("User id not found !")
        else:
            await m.rey_text("Reply to user or mention him to disapprove him !")
