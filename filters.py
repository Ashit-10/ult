from group_bot.modules.nsfw import nchek
import pytz
from group_bot.modules.fbans import fban1, unfban1
from datetime import timedelta
import datetime
from os import listdir
from group_bot.modules.lovk import locks
from group_bot.modules.helpers.welcome_sender import welcome_sender
from group_bot.modules.blocklist import roll_blocklist, callback_spam, resend_file
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.helpers.filter_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.decode_btns import decode_btns
from group_bot.modules.db import create_db
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
from group_bot import bot, mention_html
from config import *
from pyrogram.types import *
from pyrogram import *
from config import my_bot_id
from group_bot.modules.helpers.send import filter_helper
import os
import time
import json
import re
import random
from group_bot.modules.antiflood import antiflood_go
from group_bot.modules.helpers.welcome_sender import sj
from group_bot.modules.purge import purgey, ping, purgeyto, purgeyfrom
from group_bot.modules.report import reports
from group_bot.modules.afky import menafk, afk
from group_bot.modules.pin_unpin import pin, unpin
# from textblob import TextBlob as detect
from group_bot.modules.notes import group_notes, private_notes, noteslist
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0
tz = pytz.timezone("Asia/kolkata")


action_lists = ['text', 'document', 'sticker',
                'photo', 'audio', 'video', 'gif', 'any']

on_off = ['on', 'off', 'yes', 'no']

admins = ['administrator', 'creator']


# Daily backup


async def exp(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = None
    else:
        user_id = m.from_user.id
    if not user_id:
        return
    if int(user_id) == 1602293216 and "all" in m.text:
        fc = await m.reply_text("`Exporting ...`")
        path = "db"
        files = os.listdir(path)
        for fil in files:
            if str(fil).endswith("_db.txt"):
                await client.send_document(chat_id=m.chat.id, document=f"db/{fil}")
        await fc.delete()
    elif (await client.get_chat_member(chat_id=chat_id, user_id=user_id)).status == "creator" or int(user_id) == 1602293216:
        await client.send_document(chat_id=m.chat.id, document=f"db/X{chat_id}_db.txt")
    else:
        await m.reply_text("Only chat owner can import/export !")


async def imp(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = None
    else:
        user_id = m.from_user.id
    if not user_id:
        return
    if not m.reply_to_message:
        return
    if int(user_id) == 1602293216 and ("me" in m.text or "py" in m.text):
        if m.reply_to_message and not "py" in m.text:
            oke = await m.reply_text("`importing ...`")
            fn = m.reply_to_message.document.file_name
            await client.download_media(m.reply_to_message.document.file_id, file_name=f"db/{fn}")
            await oke.edit(f"Succesfully imported `{fn}`")
        else:
            oke = await m.reply_text("`importing module ...`")
            fn = m.reply_to_message.document.file_name
            await client.download_media(m.reply_to_message.document.file_id, file_name=f"group_bot/modules/{fn}")
            await oke.edit(f"Succesfully imported the module `{fn}`")

    elif (await client.get_chat_member(chat_id=chat_id, user_id=user_id)).status == "creator":
        try:
            fn = m.reply_to_message.document.file_name
            await client.download_media(m.reply_to_message.document.file_id, file_name=f"db/{fn}")
            await m.reply_text(f"Succesfully imported `{fn}`")
        except Exception as cf:
            await m.reply_text(str(cf))
    else:
        await m.reply_text("Only chat owner can import/export !")


async def addfilter(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["filters"] is not True:
            return
        if await can_restrict(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        try:
            iftexr = m.command[1]
            chat_id = m.chat.id
            if os.path.isfile(f"db/X{chat_id}_db.txt"):
                filterslist = []
                a_u = "added"
                is_enabled = obj[f"{bot_id}"]["enable_disable"]["filters"]
                if is_enabled is not True:
                    return
                try:
                    trigger = str(m.text.split(' ')[1])
                    patrigger = trigger
                    if str(trigger).startswith('"'):
                        find_ptn = re.compile(r"\"(.*?)\"")
                        for xy in find_ptn.finditer(str(m.text.split(' ', 1)[1])):
                            patrigger = xy.group(0)
                            trigger = str(xy.group(0))[1:-1]
                            break

                    disable_link_preview = True
                    full_match = False
                    action_on = "text"
                    trigger_for_admins = True
                    trigger_for_members = True

                    if m.reply_to_message and m.reply_to_message.reply_markup:
                        print("1")
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
                    trigger = return1[4]
                    disable_link_preview = return1[5]
                    full_match = return1[6]
                    action_on = return1[7]
                    trigger_for_admins = return1[8]
                    trigger_for_members = return1[9]
                    protect = return1[10]
                    if len(str(file_id)) < 7:
                        file_id = None

                    if len(str(text).replace(' ', '')) < 1:
                        text = None
                    if not m.reply_to_message and (len(str(text)) < 1 or text is None):
                        await m.reply_text("You need to give the filter some content !")
                        return

                    triggers_list = obj[f"{bot_id}"]['filters']['filters']
                    if triggers_list:

                        for i in triggers_list:
                            if i['trigger'] == trigger.lower():
                                ind = int(triggers_list.index(i))
                                del obj[f"{bot_id}"]['filters']['filters'][ind]
                                a_u = "updated"

                    new_obj = {"trigger": trigger.lower(), "text": text, "btn_url": btn_url, "file_id": file_id,
                               "action_on": action_on, "typee": typee, "disable_link_preview": disable_link_preview, "full_match": full_match, "trigger_for_admins": trigger_for_admins, "trigger_for_members": trigger_for_members, "is_protected": protect}
                    obj[f"{bot_id}"]['filters']['filters'].append(new_obj)
                    with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                        json.dump(obj, wf, indent=4)
                        await m.reply_text(
                            f"Filter {a_u} for '`{trigger}`' with action on '**{action_on}**' !")

                except Exception as e:
                    print(e)
                    await m.reply_text(str(e))

            else:
                create_db(client, m)
                await addfilter(client, m)
        except Exception as idk:
            if str(idk) == "list index out of range":
                await m.reply_text("You need to give filter's name and some content too.")
            else:
                await m.reply_text(str(idk))


async def delfilter(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["filters"] is not True:
            return
        if await can_restrict(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        filterslist = []
        try:
            trigger = str(m.text.split(' ', 1)[1]).lower()
            chat_id = m.chat.id
            triggers_list = obj[f"{bot_id}"]['filters']['filters']           
            for i in triggers_list:
                word = i['trigger']
                filterslist.append(word)          
            if trigger in filterslist:
                if triggers_list:
                    for i in triggers_list:
                        if i['trigger'] == trigger:
                            ind = int(triggers_list.index(i))
                            del obj[f"{bot_id}"]['filters']['filters'][ind]
                            if not len(str(obj)) < 20:
                                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                                    json.dump(obj, wf, indent=4)
                                    await m.reply_text(
                                        f"Filter deleted for '`{trigger}`' !")
                                    break
            else:
                await m.reply_text(
                    "You haven't saved any filter with this name yet !")
        except Exception as e:
            if str(e) == "list index out of range":
                await m.reply_text("You have to specify filter's name !")
            else:
                await m.reply_text(str(e))


async def filterslist(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["filters"] is not True:
            return
        filterslist = []
        disable_link_preview = ""
        full_match = ""
        trigger_for = ""
        chat_id = m.chat.id
        triggers = obj[f"{bot_id}"]['filters']['filters']
        is_enabled = obj[f"{bot_id}"]["enable_disable"]["filters"]
        if is_enabled is not True:
            return
        if len(str(triggers)) > 3:
            for i in triggers:
                disable_link_preview = ""
                full_match = ""
                trigger_for = ""
                word = i['trigger']
                action_on = i['action_on']
                if i['disable_link_preview'] is False:
                    disable_link_preview = "{preview}"
                if i['full_match'] is True:
                    full_match = "{full_match}"
                if i['trigger_for_admins'] is False:
                    trigger_for = "{members}"
                if i['trigger_for_members'] is False:
                    trigger_for = "{admins}"
                filterslist.append(
                    f"》<code>{word}</code>    <i>{{{action_on}}} {disable_link_preview} {full_match} {trigger_for}</i>")
            filterslist.sort()
            filterslists = "\n".join(filterslist)
  
            try:
                await m.reply_text(
                    f"<b>Currently available filters are:</b>\n{filterslists}")
            except Exception as r:
                print(str(r))
        else:
            await m.reply_text("No filters has been saved yet")


langs = ['id', 'ar', 'cn', 'ru']

welcome_service = {}


async def raid_go(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["raid"] is not True:
        return
    if await can_restrict(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
        return
    currentTime = int(time.time())
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    RaidStatus = obj[f"{bot_id}"]["raid"]["status"]
    RaidDuration = obj[f"{bot_id}"]["raid"]["duration"]
    RaidKick = obj[f"{bot_id}"]["raid"]["kick_for"]

    if RaidStatus == "on":
        obj[f"{bot_id}"]["raid"]["status"] = "off"
        obj[f"{bot_id}"]["raid"]["started_time"] = 0
        await m.reply_text("Raid mode has been closed !")

    else:
        obj[f"{bot_id}"]["raid"]["status"] = "on"
        obj[f"{bot_id}"]["raid"]["started_time"] = currentTime
        await m.reply_text(f"Raid mode has been turned on !\nNew members will be banned for {RaidKick}.")

    with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
        json.dump(obj, wf, indent=4)


async def notes(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    check_note = obj[bot_id]["on_off"]['private_notes']
    is_enabled = obj[f"{bot_id}"]["enable_disable"]["notes"]
    if is_enabled is not True:
        return
    if check_note is True:
        CHECK_THIS_OUT = str(chat_id) + "_PRIVATE-NOTES-LIST"
        url = f't.me/{bot_username}?start={chat_id}_PRIVATE-NOTES-LIST'
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="click here !", url=url)]])
        await m.reply_text(
            "click here to view notes !", reply_markup=keyboard)
    else:
        await noteslist(client, m)
    asyncio.create_task(antiflood_go(client, m, obj))


async def noteslist_callback(client, m, chat_id):
    filterslist = []
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    triggers = obj[f"{bot_id}"]['notes']
    if len(str(triggers)) > 3:
        for i in triggers:
            word = i['trigger']
            filterslist.append(
                f"- [{word}](t.me/{bot_username}?start={chat_id}_NOTES_{word})")
        filterslist.sort()
        filterslists = str(filterslist)[2:-2]
        filterslists = re.sub(r"', '", '\n', filterslists)
        filterslists = str(filterslists) + \
            "\nRetrive them by tapping on it !"
        try:
            chat_i = await client.get_chat(chat_id)
            title = chat_i.title
            await m.reply_text(
                f"<b>Currently available notes in `{title}` are:</b>\n{filterslists}")
        except Exception as r:
            print(str(r))
    else:
        await m.reply_text("No notes have been saved yet")


async def filters_yo(client, m, obj, user_id):
    og = ""
    is_a_admin = False
    chat_id = m.chat.id
    rtm = m.message_id
    filter_text = ""
    update_msg = ""
    if m.text:
        filter_text += str(m.text.markdown).lower()
        og = str(m.text).lower()
        update_msg += "text"
    else:
        if m.caption:
            filter_text += str(m.caption.markdown).lower()
            og = str(m.caption).lower()
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

    triggers = obj[f"{bot_id}"]['filters']['filters']
    if len(update_msg) > 1:
        is_a_admin = await is_admin(client, m, m.chat.id, user_id)
        if len(str(triggers)) > 3:
            for i in triggers:
                trigger_text = i['trigger']
                full_match = i['full_match']
                matched = None

                if (str(trigger_text) == str(og)) and (full_match is True):
                    trigger_type = i['action_on']
                    if (trigger_type in update_msg) or (trigger_type == "any"):
                        if is_a_admin is True and i['trigger_for_admins'] is False:
                            pass
                        elif is_a_admin is not True and i['trigger_for_members'] is False:
                            pass
                        else:
                            le_see = await filter_helper(
                                client, m, i, chat_id, rtm)
                            if le_see is True:
                                break

                elif full_match is False:
                    trigger_text = re.escape(str(trigger_text))
                    if '\*' in trigger_text:
                        trigger_text = trigger_text.replace(
                            '\*', '(.*?)')
                    partn = re.compile(
                        rf"(?=\b|^){trigger_text}(?=\b|$)")
                    pmatch = partn.finditer(str(filter_text))
                    for fi in pmatch:
                        matched = True
                        break
                    if matched:
                        trigger_type = i['action_on']
                        if (str(trigger_type) in str(update_msg)) or (trigger_type == "any"):
                            if (is_a_admin is True) and (i['trigger_for_admins'] is False):
                                pass
                            else:
                                le_see = await filter_helper(
                                    client, m, i, chat_id, rtm)
                                if le_see is True:
                                    break


langs = ['id', 'ar', 'cn', 'es', 'ru']


async def lang_detection(client, m, obj):
    if m.text or m.caption:
        get_one = None
        chat_id = m.chat.id
        if m.text:
            text = m.text.lower()
        elif m.caption:
            text = m.caption.lower()
        skip_words = obj[f"{bot_id}"]["pass_words"]
        try:
            for xyz in skip_words:
                if str(xyz) in text:
                    get_one = True
                    break
            if not get_one:
                lang_catch = detect(f"{text}")

                if lang_catch in langs:
                    await m.reply_text(f"Please english only !\nDetected lang: `{lang_catch}`")
        except Exception as e:
            pass


async def verify_captcha(client, m, chat_id):
    user_id = m.from_user.id
    verifying = await m.reply_text("`verifying ...`", quote=True)
    chat = await client.get_chat(chat_id)    
    link = chat.invite_link
    group = chat.title
    stat = await client.get_chat_member(chat_id, user_id)  
    print(stat) 
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)  
    with open(f"db/mem/X{chat_id}.txt", 'r') as ff:
        objj = json.load(ff)   
    print("q")
    oldNew = objj[f"{bot_id}"][f"{chat_id}"]
    print("w")
    chat_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text=f"Back to support group 🔙", url=f"{link}")]
    ])
    print(stat)
    if stat.status == "creator" or stat.status == "administrator":
        await verifying.edit(f"You are already an admin in {group} !", reply_markup=chat_keyboard)
    elif (stat.status == "member") or (stat.can_send_messages is True) or (int(user_id) in oldNew):
        await verifying.edit("You have already verified the captcha !", reply_markup=chat_keyboard)
    else:
        if (
            stat.is_member is True
            and stat.user.is_scam is False
            and stat.user.is_bot is False
            and stat.user.is_fake is False
        ):
            if_cap = obj[f"{bot_id}"]["on_off"]["captcharules"]
            if if_cap is True:
                rules = obj[bot_id]["rules"]
                newk = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=f"I have read and accept the rules", callback_data=f"{chat_id}_{user_id}_iaccept")]])
                await verifying.edit(text=f"Rules in {group} are:\n\n{rules}", reply_markup=newk)
            else:
                try:
                    await client.restrict_chat_member(chat_id=chat_id,
                                                      user_id=user_id,
                                                      permissions=ChatPermissions(
                                                          can_send_messages=True,
                                                          can_send_media_messages=True,
                                                          can_invite_users=True,
                                                          can_send_polls=True,
                                                          can_change_info=True,
                                                          can_pin_messages=True,
                                                          can_send_other_messages=True,
                                                          can_add_web_page_previews=True)
                                                      )

                    await verifying.edit(f"You have been verified and unmuted in {group} !", reply_markup=chat_keyboard)
                finally:
                    with open(f"db/mem/X{chat_id}.txt", "r") as rd:
                         nob = json.load(rd)
                    nob[f"{chat_id}"].append(int(user_id))
                    with open(f"db/mem/X{chat_id}.txt", 'w+') as f:
                        json.dump(nob, f, indent=4)
        else:
            await verifying.edit(f"Seems like you aren't a member of {group}, if u think this is wrong rejoin the group and try again !")


def cw(info):
    try:
        bot.delete_messages(chat_id=info.split('_')[0],
                            message_ids=int(info.split('_')[1]) + 1)
    except:
        pass


async def check_rules_cb(client, m, chat_id):
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    rules = obj[f"{bot_id}"]["rules"]
    chat = (await client.get_chat(chat_id)).title
    if not rules:
        await m.reply_text(f"No rules has been set yet in {chat}", quote=True)
    else:
        await m.reply_text(f"Rules in `{chat}` are:\n\n{rules}", quote=True)


async def antipin(client, m):
    if m.sender_chat and m.views:
        chat_id = m.chat.id
        my_ch = (await client.get_chat(chat_id)).linked_chat.id
        if int(m.sender_chat.id) == int(my_ch):
            try:
                await client.unpin_chat_message(chat_id=chat_id, message_id=m.message_id)
            except:
                pass
