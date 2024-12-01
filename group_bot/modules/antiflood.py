import json
from pyrogram import *
from pyrogram.types import *
from group_bot import mention_html, bot
import asyncio
from config import *
from group_bot.modules.blocklist import ban, mute, tmute, kick_member, tban, tmute, warn
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin


antiact = ['warn', 'ban', 'kick', 'mute']


anti = {}


async def antiflood_go(client, m, obj):
    chat_id = m.chat.id
    is_sender = None
    # with open(f"db/X{chat_id}_db.txt", 'r') as f:
    #     obj = json.load(f)
    anti_time = obj[f"{bot_id}"]["flood"]["messages"]
    anti_action = obj[f"{bot_id}"]["flood"]["action"]
    if m.sender_chat:
        user_id = m.sender_chat.id
        fname = m.sender_chat.username
        is_sender = True
    else:
        user_id = m.from_user.id
        fname = m.from_user.first_name
    ag = anti.get(chat_id)
    if not ag:
        anti.update({chat_id: {"user": user_id, "count": 2}})
    elif user_id != ag["user"]:
        anti.pop(chat_id)
        anti.update({chat_id: {"user": user_id, "count": 2}})
    elif user_id == ag["user"] and ag["count"] >= anti_time:
        anti.pop(chat_id)
        if await immutable(client, m, chat_id, user_id) is not True:
            if int(user_id) not in obj[f"{bot_id}"]["approved_channels_and_users"]:
                text = "Stop Flooding !"
                user = await mention_html(user_id, fname)
                show_msg = True
                if anti_action == "mute":
                    if not is_sender:
                        asyncio.create_task(mute(client, m, chat_id,
                                                 user_id, text, user, show_msg, None))

                elif anti_action == "ban":
                    asyncio.create_task(ban(client, m, chat_id,
                                            user_id, text, user, show_msg, None))

                elif anti_action == "kick":
                    asyncio.create_task(kick_member(
                        client, m, chat_id, user_id, text, user, show_msg, None))

                elif anti_action == "warn":
                    asyncio.create_task(warn(client, m, chat_id,
                                             user_id, text, user, show_msg, None))

                elif "tban" in anti_action:
                    asyncio.create_task(tban(client, m, chat_id, user_id, str(
                        anti_action).split()[1], text, user, show_msg, None))

                elif "tmute" in anti_action:
                    if not is_sender:
                        asyncio.create_task(tmute(client, m, chat_id, user_id, str(
                            anti_action).split()[1], text, user, show_msg, None))

    else:
        rn = ag["count"] + 1
        anti.update({chat_id: {"user": user_id, "count": rn}})
  #  print(anti)


async def rt(t):
    if "d" in t:
        if t[:-1] == "1":
            tt = "1 day"
        else:
            tt = f"{t[:-1]} days"
    elif "m" in t:
        if t[:-1] == "1":
            tt = "1 minute"
        else:
            tt = f"{t[:-1]} minutes"
    elif "h" in t:
        if t[:-1] == "1":
            tt = "1 hour"
        else:
            tt = f"{t[:-1]} hours"
    elif "w" in t:
        if t[:-1] == "1":
            tt = "1 week"
        else:
            tt = f"{t[:-1]} weeks"
    return tt


async def flood(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["antiflood"] is not True:
        return
    if await can_edit(client, m, m.chat.id, user_id) is not True:
        await m.reply_text(f"You don't have sufficient to permission; caused by [CAN_CHANGE_GROUP_INFO]")
        return
    try:
        count = obj[f"{bot_id}"]["flood"]["messages"]
        action = obj[f"{bot_id}"]["flood"]["action"]
        chat = m.chat.title
        if "tmute" in action:
            t = action.split()[1]
            tm = await rt(t)
            act = f"temporarily muted for {tm}"
        elif "tban" in action:
            t = action.split()[1]
            tm = await rt(t)
            act = f"temporarily banned for {tm}"
        elif action == "warn":
            act = "warned"
        elif action == "ban":
            act = "banned"
        elif action == "kick":
            act = "kicked"

        await m.reply_text(f"User sends `{count}` messages in a row will be `{act}` !")
    except Exception as r:
        await m.reply_text(str(r))


async def anticount(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["antiflood"] is not True:
        return
    if await can_edit(client, m, m.chat.id, user_id) is not True:
        await m.reply_text(f"You don't have sufficient to permission; caused by [CAN_CHANGE_GROUP_INFO]")
        return
    if " " in m.text:
        try:
            count = int(m.text.split()[1])
            if count == 0 or count == 1:
                await m.reply_text(f"Can't set antiflood to '{count}', select an integer more than '`2`' atleast !")
                return
            obj[f"{bot_id}"]["flood"]["messages"] = count
            with open(f"db/X{chat_id}_db.txt", 'w+') as f:
                json.dump(obj, f, indent=4)
            chat = m.chat.title
            await m.reply_text(f"Antiflood message counts has been set to {count} for `{chat}`!")
        except:
            await m.reply_text("Give a valid integer !")
    else:
        await m.reply_text("Give a valid integer !")


async def antimode(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["antiflood"] is not True:
        return
    if await can_edit(client, m, m.chat.id, user_id) is not True:
        await m.reply_text(f"You don't have sufficient to permission; caused by [CAN_CHANGE_GROUP_INFO]")
        return
    if await can_restrict(client, m, m.chat.id, user_id) is not True:
        await m.reply_text(f"You don't have sufficient to permission; caused by [CAN_RESTRICT_MEMBERS]")
        return
    if " " in m.text:
        try:
            count = m.text.split(' ', 1)[1]
            if str(count) == "warn":
                action = "warn"
            elif str(count) == "ban":
                action = "ban"
            elif str(count) == "kick":
                action = "kick"
            elif "tban" in str(count):
                ee = str(count).split()[1]
                if (
                    "m" in ee
                   or "h" in ee
                   or "d" in ee
                   or "w" in ee
                   ):
                    try:
                        tm = int(ee[:-1])
                        action = f"tban {ee}"
                    except:
                        await m.reply_text("Give a valid integer for time !")
                        return
                else:
                    await m.reply_text("Give a valid time format !")
                    return
            elif "tmute" in str(count):
                ee = str(count).split()[1]
                if (
                    "m" in ee
                   or "h" in ee
                   or "d" in ee
                   or "w" in ee
                   ):
                    try:
                        tm = int(ee[:-1])
                        action = f"tmute {ee}"
                    except:
                        await m.reply_text("Give a valid integer for time !")
                        return
                else:
                    await m.reply_text("Give a valid time format !")
                    return

            obj[f"{bot_id}"]["flood"]["action"] = action
            with open(f"db/X{chat_id}_db.txt", 'w+') as f:
                json.dump(obj, f, indent=4)
            chat = m.chat.title
            await m.reply_text(f"Antiflood action mode has been set to {action} for `{chat}`!")
        except Exception as ed:
            await m.reply_text(str(ed))
    else:
        await m.reply_text("Action mode can't be empty !")
