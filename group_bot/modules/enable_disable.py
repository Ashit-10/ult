import os
import json
from pyrogram import *
from pyrogram.types import *
from group_bot import bot
import re
from config import *
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin

enable_disable_able = ['notes', 'filters', 'pin_unpin', 'blocklists', 'ablocklists', 'promote_demote', 'greetings', 'fban',
                       "mute", "locks", 'sg', 'approve', 'warn', 'ban', 'kick', 'report', 'rules', 'antiflood', 'raid', 'ping', 'nsfw_check', 'id', 'info']

on_off = ['on', 'off', 'yes', 'no']


async def enable(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        if await can_edit(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        if " " in m.text:
            chat_id = m.chat.id
            astrn = ""
            strn = ""
            try:
                texts = str(m.command)
                with open(f"db/X{chat_id}_db.txt", 'r') as f:
                    obj = json.load(f)
                for yg in enable_disable_able:
                    if re.search(rf"\b{yg}\b", texts):
                        if obj[f"{bot_id}"]['enable_disable'][f"{yg}"] is True:
                            astrn += f"`{yg}`, "
                        else:
                            obj[f"{bot_id}"]['enable_disable'][f"{yg}"] = True
                            strn += f"`{yg}`, "
                with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
                    json.dump(obj, rf, indent=4)
                if not len(astrn) < 1:
                    astrn = f"{astrn[:-2]} already enabled !"
                if not len(strn) < 1:
                    strn = f"{strn[:-2]} have been enabled !"
                main_str = f"{astrn}\n\n{strn}"
                await m.reply_text(main_str)
            except Exception as e:
                if "[400 MESSAGE_EMPTY]" in str(e):
                    await m.reply_text("Didn't find that function to turn-on !")
                else:
                    await m.reply_text(str(e))
        else:
            await m.reply_text("What to enable ?, check /enableable")


async def disable(client, m):
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        if await can_edit(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        if " " in m.text:
            chat_id = m.chat.id
            astrn = ""
            strn = ""
            try:
                texts = str(m.command)
                with open(f"db/X{chat_id}_db.txt", 'r') as f:
                    obj = json.load(f)
                for yg in enable_disable_able:
                    if re.search(rf"\b{yg}\b", texts):
                        if obj[f"{bot_id}"]['enable_disable'][f"{yg}"] is False:
                            astrn += f"`{yg}`, "
                        else:
                            obj[f"{bot_id}"]['enable_disable'][f"{yg}"] = False
                            strn += f"`{yg}`, "
                with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
                    json.dump(obj, rf, indent=4)
                if not len(astrn) < 1:
                    astrn = f"{astrn[:-2]} already disabled !"
                if not len(strn) < 1:
                    strn = f"{strn[:-2]} have been disabled !"
                main_str = f"{astrn}\n\n{strn}"
                await m.reply_text(main_str)
            except Exception as e:
                if "[400 MESSAGE_EMPTY]" in str(e):
                    await m.reply_text("Didn't find that function to turn-off !")
                else:
                    await m.reply_text(str(e))
        else:
            await m.reply_text("What to disable ?, check /disableable")


async def en_dis_able(client, m):
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        if m:
            await m.reply_text("""
`ablocklists`
`antiflood`
`approve`
`ban`     
`blocklists`
`fban`
`filters`
`id`
`info`
`greetings`
`kick`
`locks`
`mute`
`notes`
`nsfw_check`
`pin_unpin`
`ping`
`promote_demote`
`purge`
`raid`
`report`
`rules`
`sg`
`warn`
""", quote=True)


async def disabled(client, m):
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        dc = []
        title = m.chat.title
        if m:
            chat_id = m.chat.id
            with open(f"db/X{chat_id}_db.txt", 'r') as f:
                obj = json.load(f)
            alls = obj[f"{bot_id}"]['enable_disable']
            if alls['ablocklists'] is False:
                dc.append("`ablocklists`")
            if alls['antiflood'] is False:
                dc.append("`antiflood`")
            if alls['approve'] is False:
                dc.append("`approve`")
            if alls['ban'] is False:
                dc.append("`ban`")
            if alls['blocklists'] is False:
                dc.append("`blocklists`")
            if alls['fban'] is False:
                dc.append("`fban`")
            if alls['filters'] is False:
                dc.append("`filters`")
            if alls['id'] is False:
                dc.append("`id`")
            if alls['info'] is False:
                dc.append("`info`")
            if alls['greetings'] is False:
                dc.append("`greetings`")
            if alls['kick'] is False:
                dc.append("`kick`")
            if alls['locks'] is False:
                dc.append("`locks`")
            if alls['mute'] is False:
                dc.append("`mute`")
            if alls['notes'] is False:
                dc.append("`notes`")
            if alls['nsfw_check'] is False:
                dc.append("`nsfw_check`")
            if alls['pin_unpin'] is False:
                dc.append("`pin_unpin`")
            if alls['ping'] is False:
                dc.append("`ping`")
            if alls['raid'] is False:
                dc.append("`raid`")
            if alls['report'] is False:
                dc.append("`report`")
            if alls['rules'] is False:
                dc.append("`rules`")
            if alls['sg'] is False:
                dc.append("`sg`")
            if alls['warn'] is False:
                dc.append("`warn`")
            if alls['purge'] is False:
                dc.append("`purge`")
            dc.sort()
            filterslists = str(dc)[2:-2]
            ed = re.sub(r"', '", '\n', filterslists)
            if len(ed) < 3:
                await m.reply_text(f"No commands are disabled in `{title}` !")
            else:
                await m.reply_text(f"The following commands are disabled in `{title}`:\n{ed}")


async def enabled(client, m):
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        if m:
            dc = []
            title = m.chat.title
            chat_id = m.chat.id
            with open(f"db/X{chat_id}_db.txt", 'r') as f:
                obj = json.load(f)
            alls = obj[f"{bot_id}"]['enable_disable']
            if alls['ablocklists'] is True:
                dc.append("`ablocklists`")
            if alls['antiflood'] is True:
                dc.append("`antiflood`")
            if alls['approve'] is True:
                dc.append("`approve`")
            if alls['ban'] is True:
                dc.append("`ban`")
            if alls['blocklists'] is True:
                dc.append("`blocklists`")
            if alls['fban'] is True:
                dc.append("`fban`")
            if alls['filters'] is True:
                dc.append("`filters`")
            if alls['id'] is True:
                dc.append("`id`")
            if alls['info'] is True:
                dc.append("`info`")
            if alls['greetings'] is True:
                dc.append("`greetings`")
            if alls['kick'] is True:
                dc.append("`kick`")
            if alls['locks'] is True:
                dc.append("`locks`")
            if alls['mute'] is True:
                dc.append("`mute`")
            if alls['notes'] is True:
                dc.append("`notes`")
            if alls['nsfw_check'] is True:
                dc.append("`nsfw_check`")           
            if alls['pin_unpin'] is True:
                dc.append("`pin_unpin`")
            if alls['ping'] is True:
                dc.append("`ping`")
            if alls['raid'] is True:
                dc.append("`raid`")
            if alls['report'] is True:
                dc.append("`report`")
            if alls['rules'] is True:
                dc.append("`rules`")
            if alls['sg'] is True:
                dc.append("`sg`")
            if alls['warn'] is True:
                dc.append("`warn`")
            if alls['purge'] is True:
                dc.append("`purge`")
            dc.sort()
            filterslists = str(dc)[2:-2]
            ed = re.sub(r"', '", '\n', filterslists)
            if len(ed) < 3:
                await m.reply_text(f"No commands are enabled in `{title}` !")
            else:
                await m.reply_text(f"The following commands are enabled in `{title}`:\n{ed}")


async def antiservice(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        try:
            cmd = (str(m.text).split()[0])[1:]
            ww = obj[bot_id]["on_off"][f"{cmd}"]
            link_pre = str(m.text).split()[1]
            if link_pre in on_off:
                if link_pre == 'on' or link_pre == 'yes':
                    link_prev = True
                else:
                    link_prev = False
                wut = obj[bot_id]["on_off"][f"{cmd}"]
                if wut == link_prev:
                    await m.reply_text(
                        f"{cmd} is already `{link_pre}` !")
                else:
                    obj[bot_id]["on_off"][f"{cmd}"] = link_prev
                    with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
                        json.dump(obj, rf, indent=4)
                    await m.reply_text(
                        f"{cmd} has been turned `{link_pre}` !")
            else:
                await m.reply_text(
                    f"'`{link_pre}`'  isn't a correct parameter,\nselect one between {on_off}\n{cmd} is {ww} rn !")
        except Exception as e:
            if str(e) == "list index out of range":
                await m.reply_text(f"To enable or disable it choose among {on_off}\n{cmd} is {ww} rn !")


async def cmode(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        if " " in m.text:
            try:
                texts = m.command
                with open(f"db/X{chat_id}_db.txt", 'r') as f:
                    obj = json.load(f)
                cts = obj[f"{bot_id}"]["captchamode"]
                if str(texts[1]) == "text":
                    if cts == "text":
                        await m.reply_text("Captcha mode was 'text' only !")
                    else:
                        obj[f"{bot_id}"]["captchamode"] = "text"
                        with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                            json.dump(obj, wf, indent=4)
                        await m.reply_text("Successfully changed captcha mode to 'text'")
                elif str(texts[1]) == "button":
                    if cts == "button":
                        await m.reply_text("Captcha mode was 'button' only !")
                    else:
                        obj[f"{bot_id}"]["captchamode"] = "button"
                        with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                            json.dump(obj, wf, indent=4)
                        await m.reply_text("Successfully changed captcha mode to 'button'")
                else:
                    await m.reply_text("Select only between 'text', 'button' !")
            except Exception as ed:
                await m.reply_text(str(ed))
        else:
            await m.reply_text("Give a value between 'text', 'button' !")
