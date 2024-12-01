from config import bot_username
from group_bot.modules.helpers.send import filter_helper
import os
import json
from pyrogram import *
from pyrogram.types import *
from group_bot import bot
import re
from config import bot_id
from group_bot.modules.helpers.notes_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.db import create_db
import asyncio
from group_bot.modules.helpers.names import make_answers
import html
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
import html

action_lists = ['text', 'document', 'sticker',
                'photo', 'audio', 'video', 'gif', 'any']

on_off = ['on', 'off', 'yes', 'no']


async def addnotes(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        is_enabled = obj[f"{bot_id}"]["enable_disable"]["notes"]
        if is_enabled is True:
            if await can_edit(client, m, m.chat.id, user_id) is not True:
                await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
                return
            try:
                iftexr = m.command[1]
                if os.path.isfile(f"db/X{chat_id}_db.txt"):
                    filterslist = []
                    a_u = "added"
                    try:
                        trigger = ""
                        disable_link_preview = True
                        full_match = False
                        action_on = "text"
                        trigger_for_admins = True
                        trigger_for_members = True
                        if m.reply_to_message and m.reply_to_message.reply_markup:
                            return1 = await _markup(client, m)
                        else:
                            return1 = await _markup2(client, m)
                       # print(return1)
                        btn_url = return1[0]
                        if len(str(btn_url)) < 10:
                            btn_url = None
                        text = return1[1]
                        if len(str(text)) < 1:
                            text = None
                        typee = return1[2]
                        file_id = return1[3]
                        trigger = return1[4]
                        if len(str(file_id)) < 10:
                            file_id = None
                        disable_link_preview = True
                        admins_only = False
                        disable_link_preview = return1[5]
                        admins_only = return1[6]
                        protect = return1[7]
                       # trigger = str(m.text.split(' ')[1]).lower()
                        if len(str(trigger)) < 1:
                            await m.reply_text("Note can't be empty !")
                            return
                        if (not m.reply_to_message) and (len(str(text)) < 1 or text is None):
                            await m.reply_text("You need to give the note some content !")
                            return

                        triggers_list = obj[f"{bot_id}"]['notes']
                        if triggers_list:                      
                            for i in triggers_list:
                                if i['trigger'] == trigger.lower():
                                    ind = int(triggers_list.index(i))
                                    del obj[f"{bot_id}"]['notes'][ind]
                                    a_u = "updated"
                        notecode = len(triggers_list) + 1
                        new_obj = {"trigger": trigger.lower(), "text": text, "btn_url": btn_url, "file_id": file_id,
                                   "typee": typee, "disable_link_preview": disable_link_preview, "admins_only": admins_only, "is_protected": protect, "notecode": str(notecode)}
                        obj[f"{bot_id}"]['notes'].append(new_obj)
                        with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                            json.dump(obj, wf, indent=4)
                        await m.reply_text(
                            f"Note {a_u} '`{html.escape(trigger)}`' !")
                    except Exception as e:
                        await m.reply_text(str(e))
                else:
                    await create_db(chat_id)
                    await addnotes(client, m)
            except Exception as n:
                if n == "list index out of range":
                    await m.reply_text("You need to give note's name and context !")
                else:
                    await m.reply_text(str(n))


async def pvt_notes(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        is_enabled = obj[f"{bot_id}"]["enable_disable"]["notes"]
        if is_enabled is not True:
            return
        if m.text:
            chat_id = m.chat.id
            filterslist = []
            try:
                link_pre = str(m.text.split()[1])
                if link_pre in on_off:
                    if link_pre == 'on' or link_pre == 'yes':
                        link_prev = True
                    else:
                        link_prev = False
                    wut = obj[bot_id]["on_off"]['private_notes']
                    if wut == link_prev:
                        await m.reply_text(
                            f"Private notes already has been turned `{link_pre}` !")
                    else:
                        obj[f"{bot_id}"]["on_off"]["private_notes"] = link_prev
                        with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
                            json.dump(obj, rf, indent=4)
                        await m.reply_text(
                            f"Private notes has been turned `{link_pre}` !")
                else:
                    await m.reply_text(
                        f"'`{link_pre}`'  isn't a correct parameter,\nselect one between {on_off}")
            except Exception as e:
                print(e)


async def delnotes(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        is_enabled = obj[f"{bot_id}"]["enable_disable"]["notes"]
        if is_enabled is not True:
            return
        if await can_edit(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_CHANGE_INFO]")
            return
        filterslist = []
        try:
            trigger = str(m.text.split()[1]).lower()
            chat_id = m.chat.id
            triggers_list = obj[f"{bot_id}"]['notes']
            for i in triggers_list:
                word = i['trigger']
                filterslist.append(word)
            if trigger in filterslist:
                if triggers_list:
                    for i in triggers_list:
                        if i['trigger'] == trigger:
                            ind = int(triggers_list.index(i))
                            del obj[f"{bot_id}"]['notes'][ind]
                            if not len(str(obj)) < 20:
                                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                                    json.dump(obj, wf, indent=4)
                                    await m.reply_text(
                                        f"Note deleted for '`{html.escape(trigger)}`' !")
                                    break
            else:
                await m.reply_text(
                    "You haven't saved any note with this name yet !")
        except Exception as e:
            if str(e) == "list index out of range":
                await m.reply_text("Mention note name to delete it !")
            else:
                await m.reply_text(str(e))


async def noteslist(client, m):
    filterslist = []
    admi = ""
    show_hash = "#"
    chat_id = m.chat.id
    title = m.chat.title
    end_line = "You can retrieve these notes by using `/get notename`, or `#notename`"
    if os.path.isfile(f"db/X{chat_id}_db.txt"):
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        triggers = obj[f"{bot_id}"]['notes']
        if not obj[bot_id]["on_off"]["noteshash"]:
            show_hash = ""
            end_line = "You can retrieve these notes by using `/get notename`, or `#notename`"
        if len(str(triggers)) > 3:
            for i in triggers:
                word = html.escape(i['trigger'])
                if i['admins_only'] is True:
                    admi = "__{admin}__"
                filterslist.append(f"- <code>{show_hash}{word}</code>")
            filterslist.sort()
            filterslists = "\n".join(filterslist)           
            try:
                await m.reply_text(
                    f"**Currently available notes in {title} are:**\n{filterslists}\n{end_line}")
            except Exception as r:
                await m.reply_text(str(r))
        else:
            await m.reply_text(f"No notes in {title} !")
    else:
        create_db(chat_id)
        await noteslist(client, m)


async def private_notes(client, m, chat_id, note_name):
    rtm = m.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    notes = obj[f"{bot_id}"]['notes']
    r_chat_id = m.chat.id
    
    if len(str(notes)) > 3:      
        for i in notes: 
            if i['notecode'] == note_name:
                await filter_helper(client, m, i, r_chat_id, rtm)


async def group_notes(client, m):
    chat_id = m.chat.id
    note = str(m.text).split()[0][1:].lower()
    if m.reply_to_message:
        rtm = m.reply_to_message.id
    else:
        rtm = m.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    notes = obj[f"{bot_id}"]['notes']
    is_pvt = obj[f"{bot_id}"]["on_off"]["private_notes"]
    if m.from_user:
        uid = m.from_user.id
    else:
        uid = m.sender_chat.id
    user_admin = await is_admin(client, m, chat_id, uid)
    milgaya = None
    if len(str(notes)) > 1:
        for i in notes:
            if i['trigger'] == note:
                milgaya = i
                break
        if milgaya and not is_pvt:
            if user_admin is True and milgaya['admins_only'] is True:
                asyncio.create_task(filter_helper(
                    client, m, milgaya, chat_id, rtm))
            else:
                asyncio.create_task(filter_helper(
                    client, m, milgaya, chat_id, rtm))
                    
        elif milgaya and is_pvt:
            if user_admin is True and milgaya['admins_only'] is True:
                asyncio.create_task(button_notes(
                    client, m, milgaya, chat_id, rtm))
            else:
                asyncio.create_task(button_notes(
                    client, m, milgaya, chat_id, rtm))



async def button_notes(c, m, milgaya, chat_id, rtm):
    notename = milgaya["trigger"]
    notecode = milgaya["notecode"]
    await c.send_message(text=f"Click here to get `{notename}` in private !",
        reply_to_id = rtm,
        chat_id = chat_id,
        reply_markup= InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                          text="Click here !",
                          url=f"t.me/{bot_username}?start={chat_id}_NOTES_{notecode}"
                          )]]))