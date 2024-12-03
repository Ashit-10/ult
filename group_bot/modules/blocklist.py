from group_bot import bot, mention_html, sql, db
import os, asyncio 
import json
import re
import time
from pyrogram import *
from pyrogram.types import *
from datetime import datetime, timedelta
from config import *
from group_bot.modules.helpers.db import create_db
from group_bot.modules.helpers.decode_btns import decode_btns
from group_bot.modules.helpers.filter_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.notes import group_notes, private_notes
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
from group_bot.modules.fbans import fed_admins, ben


blocklist_actions = ['warn', 'ban', 'kick', 'tmute', 'mute', 'tban', 'fban']

action_lists = ['text', 'document', 'sticker',
                'photo', 'audio', 'video', 'gif', 'any']

t_f = ["true", "false"]

on_off = ['on', 'off', 'yes', 'no']

admins = ['administrator', 'creator']


async def blocklist(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["blocklists"] is not True:
            return
        filterslist = []
        disable_link_preview = ""
        full_match = ""
        trigger_for = ""
        chat_id = m.chat.id
        triggers = obj[f"{bot_id}"]['blocklist']
        if len(str(triggers)) > 3:
            for i in triggers:
                word = i['trigger']
                action_on = i['action_on']
                action_mode = i['action_mode']
                show_warning_message = i['show_warning_message']

                filterslist.append(
                    f"》<code>{word}</code>     <i>{{{action_on}}} {{{action_mode}}} {{{show_warning_message}}} </i>")
                filterslists = '\n'.join(filterslist)
            try:
                await m.reply_text(
                    f"<b>Currently available blocklists are:</b>\n{filterslists}", parse_mode=enums.ParseMode.HTML)
            except Exception as r:
                print(str(r))
        else:
            await m.reply_text("No blocklists has been saved yet")


async def delblocklist(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["blocklists"] is not True:
            return
        if await can_edit(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        filterslist = []
        try:
            trigger = str(m.text.split()[1]).lower()
            chat_id = m.chat.id
            triggers_list = obj[f"{bot_id}"]['blocklist']
            for i in triggers_list:
                word = i['trigger']
                filterslist.append(word)
            if trigger in filterslist:
                if triggers_list:
                    for i in triggers_list:
                        if i['trigger'] == trigger:
                            ind = int(triggers_list.index(i))
                            del obj[f"{bot_id}"]['blocklist'][ind]
                            if not len(str(obj)) < 20:
                                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                                    json.dump(obj, wf, indent=4)
                                    await m.reply_text(
                                        f"Blocklist deleted for '`{trigger}`' !")
                                    break
            else:
                await m.reply_text(
                    "You haven't added any blocklist with this name yet !")
        except Exception as e:
            await m.reply_text(str(e))


async def addblocklist(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["blocklists"] is not True:
            return
        if await can_edit(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        if " " in m.text:
            chat_id = m.chat.id
            filterslist = []
            a_u = "added"
            text = None
            if os.path.isfile(f"db/X{chat_id}_db.txt"):
                try:
                    trigger = str(m.text.split(' ')[1]).lower()
                    if str(trigger).startswith('"'):
                        find_ptn = re.compile("\"(.*?)\"")
                        for xy in find_ptn.finditer(str(m.text.split(' ', 1)[1])):
                           # trigger = xy.group(0)
                            trigger = str(xy.group(0))[1:-1]
                            break

                    chat_id = m.chat.id
                    triggers_list = obj[f"{bot_id}"]['blocklist']
                    for i in triggers_list:
                        word = i['trigger']
                        filterslist.append(word)
                    if trigger in filterslist:
                        if triggers_list:
                            for i in triggers_list:
                                if i['trigger'] == trigger:
                                    ind = int(triggers_list.index(i))
                                    del obj[f"{bot_id}"]['blocklist'][ind]
                                    if not len(str(obj)) < 20:
                                        with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                                            json.dump(obj, wf, indent=4)
                                        a_u = "updated"
                                        break
                except:
                    a_u = "added"
                action_mode = ""
                action_on = ""
                show_warning_message = ""
                should_delete = True
                trigger = str(m.text.split(' ')[1]).lower()
                patrigger = trigger
                mtext = m.text.split(' ', 1)[1]
                if " " in mtext:
                    text = (mtext.split(" ",1)[1]).strip()
                else:
                     text = ""
                if str(trigger).startswith('"'):
                    find_ptn = re.compile("\"(.*?)\"")
                    for xy in find_ptn.finditer(mtext):
                        patrigger = xy.group(0)
                        trigger = str(xy.group(0))[1:-1]
                        text = (mtext[:xy.span(0)[0]] +  mtext[xy.span(0)[1]:]).strip()
                        break
                
                
                pat = re.compile(r'\{(.*?)\}')
                for gg in pat.finditer(str(text).lower()):
                    gg_b = str(gg.group(0))
                    gg_o = str(gg.group(0))[1:-1]

                    if str(gg_o).split()[0] in blocklist_actions:
                        action_mode = gg_o
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass

                    if str(gg_o).split()[0] in action_lists:
                        action_on = gg_o
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass

                    if str(gg_o).split()[0] in ['dont_del', 'delete', 'del']:
                        if gg_o == 'dont_del':
                           should_delete = False                       
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass
                            
                    if str(gg_o).split()[0] in t_f:
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass
                        if str(gg_o).split()[0] == "true":
                            show_warning_message = True
                        else:
                            show_warning_message = False

                if len(text.strip()) < 1:
                    text = None
                else:
                    text = text.lower()
                try:
                    text = text.replace('  ', '')
                except:
                    pass
                if len(str(action_mode)) < 2:
                    action_mode = "nothing"

                if len(str(action_on)) < 2:
                    action_on = "text"

                if len(str(show_warning_message)) < 2:
                    show_warning_message = True
                is_advanced = False
                with open(f"db/X{chat_id}_db.txt", 'r+') as f:
                    obj = json.load(f)
                    new_obj = {"trigger": trigger.lower(), "text": text, "action_on": action_on, "action_mode": action_mode,
                               "should_delete": should_delete, "show_warning_message": show_warning_message}  # ,"is_advanced": is_advanced}
                    obj[f"{bot_id}"]['blocklist'].append(new_obj)
                    f.seek(0)
                    json.dump(obj, f, indent=4)
                    await m.reply_text(
                        f"'`{trigger.lower()}`' has been {a_u} to blocklist will action on '*{action_on}*' !")

            else:
                create_db(chat_id)
                await addblocklist(client, m)
        else:
            await m.reply_text("No arguments given !")


async def ablocklist(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["ablocklists"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:

        filterslist = []
        disable_link_preview = ""
        full_match = ""
        trigger_for = ""
        chat_id = m.chat.id
        triggers = obj[f"{bot_id}"]['advancedblocklist']
        if len(str(triggers)) > 3:
            for i in triggers:
                word = i['trigger']
                action_on = i['action_on']
                action_mode = i['action_mode']
                show_warning_message = i['show_warning_message']
                times = str(i["times"]) + "times"
                within = i['within']

                filterslist.append(
                    f"》<code>{word}</code>  <i>{{{action_on}}} {{{action_mode}}} {{{times}}} {{{within}}} {{{show_warning_message}}} </i>")
                filterslists = '\n'.join(filterslist)

            try:
                await m.reply_text(
                    f"<b>Currently available advanced blocklists are:</b>\n{filterslists}", parse_mode=enums.ParseMode.HTML)
            except Exception as r:
                print(str(r))
        else:
            await m.reply_text("No advanced blocklists has been saved yet")


async def delablocklist(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["blocklists"] is not True:
            return
        if await can_edit(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        filterslist = []
        try:
            trigger = str(m.text.split()[1]).lower()
            chat_id = m.chat.id
            triggers_list = obj[f"{bot_id}"]['advancedblocklist']
            for i in triggers_list:
                word = i['trigger']
                filterslist.append(word)
            if trigger in filterslist:
                if triggers_list:
                    for i in triggers_list:
                        if i['trigger'] == trigger:
                            ind = int(triggers_list.index(i))
                            del obj[f"{bot_id}"]['advancedblocklist'][ind]
                            if not len(str(obj)) < 20:
                                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                                    json.dump(obj, wf, indent=4)
                                    await m.reply_text(
                                        f"Advanced blocklist deleted for '`{trigger}`' !")
                                    break
            else:
                await m.reply_text(
                    "You haven't added any advanced blocklist with this name yet !")
        except Exception as e:
            await m.reply_text(str(e))


async def addablocklist(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["blocklists"] is not True:
            return
        if await can_edit(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        chat_id = m.chat.id
        filterslist = []
        a_u = "added"
        text = None
        if os.path.isfile(f"db/X{chat_id}_db.txt"):
            if not m.reply_to_message and (not " " in m.text):
                await m.reply_text("Give some content when ?")
                return
            action_mode = ""
            action_on = ""
            show_warning_message = True
            times = ""
            within = ""

            trigger = str(m.text.split(' ')[1]).lower()
            patrigger = trigger
            if str(trigger).startswith('"'):
                find_ptn = re.compile("\"(.*?)\"")
                for xy in find_ptn.finditer(str(m.text.split(' ', 1)[1])):
                    patrigger = xy.group(0)
                    trigger = str(xy.group(0))[1:-1]
                    break

            text = str(m.text.split(' ', 1)[1])
            try:
                text = text.replace(patrigger, '', 1)
            except:
                pass
            t_was = 1
            pat = re.compile(r'\{(.*?)\}')
            try:
                for gg in pat.finditer(str(m.text)):
                    gg_b = str(gg.group(0))
                    gg_o = str(gg.group(0))[1:-1]

                    if str(gg_o).split()[0] in blocklist_actions:
                        action_mode = gg_o
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass
                    elif str(gg_o).split()[0] in action_lists:
                        action_on = gg_o
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass

                    elif "s" in str(gg_o).split()[0] or "m" in str(gg_o).split()[0] or "h" in str(gg_o).split()[0] or "d" in str(gg_o).split()[0]:
                        if "s" in str(gg_o).split()[0]:
                            within = str(gg_o).split()[0].replace('s', '')
                            t_was = 1
                        elif "m" in str(gg_o).split()[0]:
                            within = str(gg_o).split()[0].replace('m', '')
                            t_was = 60
                        elif "h" in str(gg_o).split()[0]:
                            within = str(gg_o).split()[0].replace('h', '')
                            t_was = 60 * 60
                        elif "d" in str(gg_o).split()[0]:
                            within = str(gg_o).split()[0].replace('d', '')
                            t_was = 60 * 60 * 24
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass

                    elif str(gg_o).split()[0] in t_f:

                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass
                        if str(gg_o).split()[0] == "true":
                            show_warning_message = True
                        else:
                            show_warning_message = False

                    elif str(gg_o).split()[1] == "times":
                        times = int(str(gg_o).split()[0])
                        try:
                            text = text.replace(gg_b, '', 1)
                        except:
                            pass

            except Exception as nf:
                print(str(nf))
                await m.reply_text(
                    "Something is missing , check this example:\n`/addablocklist *.apk Plz don't spam apk here {document} {tmute 1m} {3 times} {10s}`\n**NB:**(suffixes for within time can be `s`, `m`, `h` or `d` only)\nand `fillings` should be lower case !", quote=True)
                return
            if len(str(text).replace(' ', '')) < 1:
                text = None
            try:
                text = text.replace('  ', '')
            except:
                pass
            if len(str(action_mode)) < 2:
                action_mode = "nothing"

            if len(str(action_on)) < 2:
                action_on = "text"

            if len(str(show_warning_message)) < 2:
                show_warning_message = True

            if not str(times).isdigit:
                await m.reply_text(
                    "'howmany times' isn't specified , check this example:\n`/addablocklist *.apk Plz don't spam apk here {document} {tmute 1m} {3 times} {10s}`", quote=True)
                return
            if len(str(within)) < 1:
                await m.reply_text(
                    "'within time' isn't specified , check this example:\n`/addablocklist *.apk Plz don't spam apk here {document} {tmute 1m} {3 times} {10s}`", quote=True)
                return
            else:
                try:
                    within = int(within) * t_was
                except:
                    await m.reply_text(
                        "'within time' is in incorrect format, check this example:\n`/addablocklist *.apk Plz don't spam apk here {document} {tmute 1m} {3 times} {10s}`", quote=True)
                    return
            if trigger and action_on and action_mode and times and within:
                try:
                    trigger = str(m.text.split(' ')[1]).lower()
                    if str(trigger).startswith('"'):
                        find_ptn = re.compile("\"(.*?)\"")
                        for xy in find_ptn.finditer(str(m.text.split(' ', 1)[1])):
                            trigger = xy.group(0)
                            break

                    chat_id = m.chat.id
                    triggers_list = obj[f"{bot_id}"]['advancedblocklist']
                    for i in triggers_list:
                        word = i['trigger']
                        filterslist.append(word)
                    if trigger in filterslist:
                        if triggers_list:
                            for i in triggers_list:
                                if i['trigger'] == trigger:
                                    ind = int(triggers_list.index(i))
                                    del obj[f"{bot_id}"]['advancedblocklist'][ind]
                                    if not len(str(obj)) < 20:
                                        with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                                            json.dump(obj, wf, indent=4)
                                            a_u = "clientd"
                                            break
                except:
                    a_u = "added"
                new_obj = {"trigger": trigger, "text": text, "action_on": action_on, "action_mode": action_mode, "times": times, "within": within,
                           "should_delete": True, "show_warning_message": show_warning_message}
                with open(f"db/X{chat_id}_db.txt", 'r+') as f:
                    obj = json.load(f)
                    obj[f"{bot_id}"]['advancedblocklist'].append(new_obj)
                    f.seek(0)
                    json.dump(obj, f, indent=4)
                    await m.reply_text(
                        f"'`{trigger}`' has been {a_u} to advanced blocklist will do --{action_mode}-- if --{action_on}-- is found --{times}-- times within --{within}-- seconds !")

        else:
            create_db(chat_id)
            await addablocklist(client, m)


async def roll_blocklist(client, m, obj):
    chat_id = m.chat.id
    rtm = m.id
    is_sender = None
    if m.sender_chat:
        user_id = m.sender_chat.id
        username = f"@{m.sender_chat.username}"
        user = m.sender_chat.title
        is_sender = True
    else:
        user_id = m.from_user.id
        user_fname = m.from_user.first_name
        user = f"""<a href="tg://user?id={user_id}">{user_fname}</a>"""
        if os.path.isfile(f"db/X{chat_id}_db.txt"):
            filter_text = ""
            update_msg = ""
            if m.text:
                filter_text += str(m.text.markdown).lower()
                update_msg += "text"
            else:
                if m.caption:
                    filter_text += str(m.caption.markdown).lower()
                    update_msg += "text"
                if m.animation:
                    try:
                        filter_text += str(
                            m.animation.file_name).lower()
                        update_msg += "gif"
                    except:
                        filter_text = ""
                        update_msg = ""
                if m.sticker:
                    filter_text += str(m.sticker.emoji)
                    update_msg += "sticker"
                if m.video:
                    filter_text += str(m.video.file_name).lower()
                    update_msg += "video"
                if m.photo:
                    try:
                        filter_text += str(
                            m.photo.file_name).lower()
                        update_msg += "photo"
                    except:
                        filter_text = ""
                        update_msg = ""
                if m.audio:
                    filter_text += str(m.audio.file_name)
                    update_msg += "audio"
                if m.document:
                    filter_text += str(m.document.file_name)
                    update_msg += "document"
            triggers = obj[f"{bot_id}"]['blocklist']
            if len(str(triggers)) > 3:
                for i in triggers:
                    trigger_text = re.escape(str(i['trigger']))
                    if '\*' in trigger_text:
                        trigger_text = trigger_text.replace('\*', '(.*?)')
                    block_partn = re.compile(
                        rf"(?=\b|^){trigger_text}(?=\b|$)")
                    pmatch = block_partn.finditer(str(filter_text))
                    matched = None
                    for fi in pmatch:
                        matched = True
                        break
                    if matched:
                        trigger_type = i['action_on']
                        text = i['text']
                        if not text:
                            text = f"due to a match on blocklist '`{i['trigger']}`'"
                        action_mode = i['action_mode']
                        if i['show_warning_message'] is True:
                            show_msg = True
                        else:
                            show_msg = False
                        if (str(trigger_type) in str(update_msg)) or (trigger_type == "any"):
                            if i["should_delete"]:
                                try:
                                    await m.delete()
                                except:
                                    await m.reply_text("Well, I haven't got permission to delete messages yet, how the fuk Blocklist will work !")
                            if action_mode == "mute":
                                if not is_sender:
                                    await mute(client, m, chat_id,
                                               user_id, text, user, show_msg, None)
                                    break
                            elif action_mode == "ban":
                                await ban(client, m, chat_id,
                                          user_id, text, user, show_msg, None)
                                break
                            elif action_mode == "kick":
                                await kick_member(
                                    client, m, chat_id, user_id, text, user, show_msg)
                                break
                            elif action_mode == "warn":
                                await warn(client, m, chat_id,
                                           user_id, text, user, show_msg, None)
                                break
                            elif action_mode == "fban":
                                await warn(client, m, chat_id,
                                           user_id, text, user, show_msg, None)
                                break
                            elif "tban" in action_mode:
                                await tban(client, m, chat_id, user_id, str(
                                    action_mode).split()[1], text, user, show_msg, None)
                                break
                            elif "tmute" in action_mode:
                                if not is_sender:
                                    await tmute(client, m, chat_id, user_id, str(
                                        action_mode).split()[1], text, user, show_msg, None)
                                    break
                            else:
                                if i['show_warning_message'] is True:
                                    text = f"{user} triggered a blocklist !\n<b>Reason:</b> {text}"
                                    await client.send_message(
                                        text=text, chat_id=chat_id)
                                    break


async def mute(client, m, chat_id, user_id, text, user, show_msg, send_keyboard):
    reason = text
    keyboard = None
    if send_keyboard:
        keyboard = send_keyboard
    try:
        await client.restrict_chat_member(chat_id=chat_id,
                                          user_id=user_id,
                                          permissions=ChatPermissions()

                                          )
        if not keyboard:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text=f"Unmute (Admin only)", callback_data=f"{user_id}_unmute")]
            ])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(
                text=f"Unmute (Admin only)", callback_data=f"{user_id}_unmute")])
        if show_msg is True:
            await client.send_message(
                text=f"""Muted {user} !\n<b>Reason:</b> {reason}""", chat_id=chat_id, reply_markup=keyboard)
    except Exception as em:
        await client.send_message(text=str(em), chat_id=chat_id)


async def ban(client, m, chat_id, user_id, text, user, show_msg, send_keyboard):
    reason = text
    keyboard = None
    if send_keyboard:
        keyboard = send_keyboard
    reason = text
    try:
        await client.ban_chat_member(chat_id=chat_id,
                                     user_id=user_id)

        if show_msg is True:
            if not keyboard:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text=f"Unban (Admin only)", callback_data=f"{user_id}_unban")]
                ])
            else:
                keyboard.inline_keyboard.append([InlineKeyboardButton(
                    text=f"Unban (Admin only)", callback_data=f"{user_id}_unban")])
            await client.send_message(
                text=f"""Banned {user} !\n<b>Reason:</b> {reason}""", chat_id=chat_id, reply_markup=keyboard)
    except Exception as eb:
        await client.send_message(text=str(eb), chat_od=chat_id)


async def kick_member(client, m, chat_id, user_id, text, user, show_msg, *args):
    reason = text
    keyboard = None
    reason = text
    try:
        await client.ban_chat_member(chat_id=chat_id,
                                     user_id=user_id, until_date = datetime.now() + timedelta(seconds=35))        
        if show_msg is True:
            await client.send_message(
                text=f"""Kicked {user} !\n<b>Reason:</b> {reason}""", chat_id=chat_id)
    except Exception as ek:
        await client.send_message(text=str(ek), chat_id=chat_id)
    finally:
        await client.unban_chat_member(chat_id=chat_id,
                                       user_id=user_id)


async def warn(client, m, chat_id, user_id, text, user, show_msg, send_keyboard):
    reason = text
    keyboard = None
    if send_keyboard:
        keyboard = send_keyboard
    reason = text
    reasons = ''
    try:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        y = obj[f"{bot_id}"]['max_warns']
        with open("db/warns.txt", "r") as se:
             wob = json.load(se)
        try:
            reasons = wob["warns"][f"{chat_id}_{user_id}"]
        except KeyError:
            reasons = ""         
        if len(str(reasons)) > 1 and reasons:
            reason_lists = reasons.split('[%%%]')
            warn_numbers = len(reason_lists) - 1
        else:
            warn_numbers = 0
        reasons += f"""{reason}[%%%]"""
        wants = warn_numbers+1
        if str(wants) >= str(y):
            await warn_damage(client, m, user_id, chat_id)
            wob["warns"][f"{chat_id}_{user_id}"] = reasons
            with open("db/warns.txt", "w+") as se:
                json.dump(wob, se, indent=6, sort_keys=True)
            return
        if show_msg is True:
            if not keyboard:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text=f"Remove warn (Admin only)", callback_data=f"{user_id}_unwarn")]
                ])
            else:
                keyboard.inline_keyboard.append([InlineKeyboardButton(
                    text=f"Remove warn ", callback_data=f"{user_id}_unwarn")])
            await client.send_message(chat_id=chat_id,
                                      text=f"{user} have {wants}/{y} warnings !\n<b>Reason:</b> {reason}", reply_markup=keyboard)
    except Exception as ew:
        await client.send_message(chat_id=chat_id, text=str(ew))
    finally:
          wob["warns"][f"{chat_id}_{user_id}"] = reasons
          with open("db/warns.txt", "w+") as se:
               json.dump(wob, se, indent=6, sort_keys=True)


async def tfban(client, m, chat_id, user_id, text, user, show_msg, send_keyboard):        
        if not await is_admin(client, m, chat_id, user_id):
            with open(f"db/fed.txt", "r") as fr:
                fcons = json.load(fr)
            try:
                cfed = fcons["per_group"][str(chat_id)]
            except KeyError:
                await m.reply_text("This group doesn't have any federation connected !", show_alert=True)
                return
            fadms = fcons['allfeds'][str(cfed)]["admins"]   
            reason = text.strip()
            if fadms:
                if int(user_id) in fadms or int(user_id) in fed_admins:
                    try:
                        await client.ban_chat_member(chat_id=chat_id,
                                                     user_id=user_id)
                    except Exception as e:
                        if '[400 USER_ADMIN_INVAID]' in str(e):
                            try:
                                await m.chat.promote_member(
                                    user_id=user_id,
                                    can_change_info=False,
                                    can_invite_users=False,
                                    can_delete_messages=False,
                                    can_restrict_members=False,
                                    can_pin_messages=False,
                                    can_promote_members=False,
                                    can_manage_chat=False,
                                    can_manage_voice_chats=False,
                                )
                            except:
                                await m.reply_text('I can not ban that admin !')
                                return
                        else:
                            await m.reply_text(str(e))
                            return
                    ulink = f"[Link](tg://openmessage?user_id={user_id})"
                    fadmin = m.from_user.first_name

                    fedname = fcons['allfeds'][str(cfed)]["name"]
                    with open("db/fedbans.txt", "r") as red:
                        fbanned = json.load(red)
                    try:
                        reason = fbanned[str(cfed)][str(user_id)]
                        await m.reply_text(f"{user} is already fbanned in current federation {fedname}\n**Reason:** {reason}")
                        return
                    except KeyError:
                        try:
                            fbanned[str(cfed)][str(user_id)] = str(reason)
                        except:
                            fbanned.update(
                                {str(cfed): {str(user_id): str(reason)}})
                    if show_msg:
                         await m.reply_text(f"""
**New FedBan**
**Fed:** {fedname}
**FedAdmin:** {fadmin}
**User:** {user}
**User ID:** `{user_id}`
**permanent link:** {ulink}
**Reason:** {reason}              
""", quote=False)
                    asyncio.create_task(ben(client, m, cfed, user_id))
                    with open("db/fedbans.txt", "w+") as rit:
                        json.dump(fbanned, rit, indent=4)

    
async def tban(client, m, chat_id, user_id, action_mode, text, user, show_msg, send_keyboard):
    reason = text
    keyboard = None
    if send_keyboard:
        keyboard = send_keyboard
    reason = text
    try:
        if "m" in action_mode:
            dtime = int(str(action_mode).replace('m', '')) * 60
            if dtime == 60:
                action_mode = action_mode.replace('m', ' minute')
            else:
                action_mode = action_mode.replace('m', ' minutes')

        elif 'h' in action_mode:
            dtime = int(str(action_mode).replace('h', '')) * 3600
            if dtime == 3600:
                action_mode = action_mode.replace('h', ' hour')
            else:
                action_mode = action_mode.replace('h', ' hours')
        elif 'd' in action_mode:
            dtime = int(str(action_mode).replace(
                'd', '')) * 3600 * 24
            if dtime == 86400:
                action_mode = action_mode.replace('d', ' day')
            else:
                action_mode = action_mode.replace('d', ' days')
        else:
            dtime = 10
            action_mode = None
        await client.ban_chat_member(chat_id=chat_id,
                                     until_date=datetime.now() + timedelta(seconds=dtime),
                                     user_id=user_id)
        if not keyboard:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text=f"Unban (Admin only)", callback_data=f"{user_id}_unban")]
            ])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(
                text=f"Unban (Admin only)", callback_data=f"{user_id}_unban")])
        if action_mode:
            if show_msg is True:
                await client.send_message(
                    text=f"""Banned {user} for {action_mode}.\n<b>Reason:</b> {text}""", chat_id=chat_id, reply_markup=keyboard)
        else:
            if show_msg is True:
                if not keyboard:
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                         text=f"Unmute (Admin only)", callback_data=f"{user_id}_unmute")]
                    ])
                else:
                    keyboard = keyboard.inline_keyboard.append([InlineKeyboardButton(
                        text=f"Unmute (Admin only)", callback_data=f"{user_id}_unmute")])
                await client.send_message(
                    text=f"""Banned {user} !\n<b>Reason:</b> {reason}""", chat_id=chat_id, reply_markup=keyboard)
    except Exception as et:
        await client.send_message(trxt=str(et), chat_id=chat_id)


async def tmute(client, m, chat_id, user_id, action_mode, text, user, show_msg, send_keyboard):
    reason = text
    keyboard = None
    if send_keyboard:
        keyboard = send_keyboard
    reason = text
    try:
        if "m" in action_mode:
            dtime = int(str(action_mode).replace('m', '')) * 60
            if dtime == 60:
                action_mode = action_mode.replace('m', ' minute')
            else:
                action_mode = action_mode.replace('m', ' minutes')
        elif 'h' in action_mode:
            dtime = int(str(action_mode).replace('h', '')) * 3600
            if dtime == 3600:
                action_mode = action_mode.replace('h', ' hour')
            else:
                action_mode = action_mode.replace('h', ' hours')
        elif 'd' in action_mode:
            dtime = int(str(action_mode).replace(
                'd', '')) * 3600 * 24
            if dtime == 86400:
                action_mode = action_mode.replace('d', ' day')
            else:
                action_mode = action_mode.replace('d', ' days')
        else:
            dtime = 10
            action_mode = None
        await client.restrict_chat_member(chat_id=chat_id,
                                          user_id=user_id,
                                          until_date=datetime.now() + timedelta(seconds=dtime),
                                          permissions=ChatPermissions()

                                          )
        if not keyboard:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text=f"Unmute (Admin only)", callback_data=f"{user_id}_unmute")]
            ])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(
                text=f"Unmute (Admin only)", callback_data=f"{user_id}_unmute")])
        if action_mode:
            if show_msg is True:
                await client.send_message(
                    text=f"""Muted {user} for {action_mode}.\n<b>Reason:</b> {text}""", chat_id=chat_id, reply_markup=keyboard)
        else:
            if show_msg is True:
                await client.send_message(
                    text=f"""Muted {user} !\n<b>Reason:</b> {reason}""", chat_id=chat_id, reply_markup=keyboard)
    except Exception as ett:
        await client.send_message(chat_id=chat_id, text=str(ett))


"""
eg: /advancedblocklist SystemUI.apk {document} {tmute 1h} {2 times} {3m}
"""


apk_spam = {}

resend_infos = {}


async def callback_spam(client, m, obj):
    chat_id = m.chat.id
    rtm = m.id
    if m.sender_chat:
        user_id = m.sender_chat.id
        username = f"@{m.sender_chat.username}"
        user = m.sender_chat.title
    else:
        user_id = m.from_user.id
        user_fname = m.from_user.first_name
        user = f"""<a href="tg://user?id={user_id}">{user_fname}</a>"""
        if os.path.isfile(f"db/X{chat_id}_db.txt"):
            filter_text = ""
            dbl = None
            update_msg = ""
            user_id = m.from_user.id
            if m.text:
                filter_text += str(m.text.markdown).lower()
                update_msg += "text"
            else:
                if m.caption:
                    filter_text += str(m.caption.markdown).lower()
                    update_msg += "text"
                if m.animation:
                    try:
                        filter_text += str(
                            m.animation.file_name).lower()
                        update_msg += "gif"
                    except:
                        filter_text = ""
                        update_msg = ""
                if m.sticker:
                    filter_text += str(m.sticker.emoji)
                    update_msg += "sticker"
                if m.video:
                    filter_text += str(m.video.file_name).lower()
                    update_msg += "video"
                if m.photo:
                    try:
                        filter_text += str(
                            m.photo.file_name).lower()
                        update_msg += "photo"
                    except:
                        filter_text = ""
                        update_msg = ""
                if m.audio:
                    filter_text += str(m.audio.file_name)
                    update_msg += "audio"
                if m.document:
                    filter_text += str(m.document.file_name)
                    update_msg += "document"

            spam_lists = obj[f"{bot_id}"]['advancedblocklist']

            if len(str(spam_lists)) > 3 and len(filter_text) > 1:
                for i in spam_lists:
                    trigger_text = re.escape(str(i['trigger']))
                    if '\*' in trigger_text:
                        trigger_text = trigger_text.replace('\*', '(.*?)')
                    block_partn = re.compile(
                        rf"(?=\b|^){trigger_text}(?=\b|$)")
                    pmatch = block_partn.finditer(str(filter_text))
                    matched = None
                    for fi in pmatch:
                        matched = True
                        break

                    if matched:
                        trigger_type = i['action_on']
                        send_keyboard = None
                       # ((update_msg)
                      #  print(filter_text)
                        if (str(trigger_type) in str(update_msg)) or (trigger_type == "any"):
                            text = i['text']
                            if not text:
                                text = f"due to a match on blocklist '{i['trigger']}'"
                            action_mode = i['action_mode']
                            num_of_spams = i['times']
                            if_exists = apk_spam.get(user_id)
                            if not if_exists:
                                apk_spam.update(
                                    {user_id: {"num": 1, "time": time.time()}})                              
                            else:
                                spam_num = if_exists['num']
                                spam_num += 1
                                old_spam_time = if_exists['time']
                                bich_time = int(
                                    time.time()) - int(if_exists['time'])
                                if str(spam_num) == str(num_of_spams) and bich_time <= int(i['within']):
                                    apk_spam.pop(user_id)
                                    if i['show_warning_message'] is True:
                                        show_msg = True
                                    else:
                                        show_msg = False
                                    try:
                                        if m.document or m.photo or m.audio or m.video or m.animation:
                                            fwed = await m.copy(-1001574127754)
                                            msgid = fwed.id
                                        await m.delete()
                                        if "document" in str(update_msg):
                                            send_keyboard = InlineKeyboardMarkup([
                                                [InlineKeyboardButton(text=f"Get file (Admins only)", url=f"t.me/{bot_username}?start={chat_id}_resendfile_{msgid}")]])
                                    except Exception as fg:
                                        print(fg)
                                        
                                    if action_mode == "mute":
                                        await mute(client, m, chat_id,
                                                   user_id, text, user, show_msg, send_keyboard)
                                        break
                                    elif action_mode == "ban":
                                        await ban(client, m, chat_id,
                                                  user_id, text, user, show_msg, send_keyboard)
                                        break
                                    elif action_mode == "kick":
                                        await kick_member(
                                            client, m, chat_id, user_id, text, user, show_msg, send_keyboard)
                                        break
                                    elif action_mode == "warn":
                                        await warn(client, m, chat_id,
                                                   user_id, text, user, show_msg, send_keyboard)
                                        break
                                    elif "tban" in action_mode:
                                        await tban(client, m, chat_id, user_id, str(
                                            action_mode).split()[1], text, user, show_msg, send_keyboard)
                                        break
                                    elif "tmute" in action_mode:
                                        await tmute(client, m, chat_id, user_id, str(
                                            action_mode).split()[1], text, user, show_msg, send_keyboard)
                                        break
                                    else:
                                        if i['show_warning_message'] is True:
                                            text = f"{user} triggered a blocklist !\n<b>Reason:</b> {text}"
                                            await client.send_message(
                                                text=text, chat_id=chat_id)
                                            break

                                elif bich_time >= int(i['within']):
                                    apk_spam.pop(user_id)
                                else:
                                    apk_spam.update(
                                        {user_id: {"num": spam_num, "time": old_spam_time}})


# callback warn damage

async def warn_damage(client, m, user_id, chat_id):
    try:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
            warn_action = obj[f'{bot_id}']['warn_action']
        text = 'Warning limit crossed !'

        fnames = await client.get_chat(user_id)
        try:
            fname = fnames.title
            user = f"@{fnames.username}"
        except:
            fname = fnames.first_name
            user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
        show_msg = True
        if warn_action == 'ban':
            await ban(client, m, chat_id, user_id, text, user, show_msg)
        elif warn_action == 'kick':
            await kick_member(
                client, m, chat_id, user_id, text, user, show_msg)
        elif 'tban' in warn_action:
            await tban(client, m, chat_id, user_id, str(
                warn_action).split()[1], text, user, show_msg)
    except Exception as e:
        print(e)


async def resend_file(client, m, chat_id, msgid):
    schat_id = -1001574127754
    chat_id = m.from_user.id
    try:
        await client.forward_messages(chat_id=chat_id,
                                      from_chat_id=schat_id,
                                      ids=int(msgid))
    except Exception as dr:
        await m.reply_text(str(dr))
