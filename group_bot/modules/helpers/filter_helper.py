import os
import json
from pyrogram import *
from pyrogram.types import *
import re

action_lists = ['{text}', '{document}', '{sticker}',
                '{photo}', '{audio}', '{video}', '{gif}', '{any}']

on_off = ['on', 'off', 'yes', 'no']


async def _markup(client, m):
    if m.reply_to_message:
        btns = ""
        typee = 0
        file_id = ""
        text = ''
        button_urls = []
        if m.reply_to_message and m.reply_to_message.text:
            text = m.reply_to_message.text.markdown
        if m.reply_to_message and m.reply_to_message.sticker:
            file_id = m.reply_to_message.sticker.file_id
            typee = 1
        if m.reply_to_message and m.reply_to_message.photo:
            file_id = m.reply_to_message.photo.file_id
            typee = 2
        if m.reply_to_message and m.reply_to_message.document:
            file_id = m.reply_to_message.document.file_id
            typee = 3
        if m.reply_to_message and m.reply_to_message.video:
            file_id = m.reply_to_message.video.file_id
            typee = 4
        if m.reply_to_message and m.reply_to_message.audio:
            file_id = m.reply_to_message.audio.file_id
            typee = 5
        elif m.reply_to_message and m.reply_to_message.animation:
            file_id = m.reply_to_message.animation.file_id
            typee = 6
        if m.reply_to_message and m.reply_to_message.caption:
            text = m.reply_to_message.caption.markdown

        if m.reply_to_message and m.reply_to_message.reply_markup:
            msg = m.reply_to_message.reply_markup

            yio = len(
                m.reply_to_message.reply_markup['inline_keyboard']) + 2
            i = 0
            while i < yio:
                dash = []
                try:
                    hm1 = msg['inline_keyboard'][i][0]['text']
                    hm2 = msg['inline_keyboard'][i][0]['url']
                    btns += f"""[{hm1}](buttonurl://{hm2})"""
                    leny = len(msg['inline_keyboard'][i])
                    j = 1
                    while j < leny:
                        hm11 = msg['inline_keyboard'][i][j]['text']
                        hm21 = msg['inline_keyboard'][i][j]['url']
                        btns += f"""[{hm11}](buttonurl://{hm21}:same)"""
                        j += 1
                    i += 1
                except Exception as e:
                    i += 1

        try:

            geta = await tescape(client, m)
            text += geta[0]
            trigger = geta[1]
            disable_link_preview = geta[2]
            full_match = geta[3]
            action_on = geta[4]
            trigger_for_admins = geta[5]
            trigger_for_members = geta[6]
            btns += geta[7]
            protect = geta[8]
        except Exception as e:

            await m.reply_text(str(e))

        return btns, text, typee, file_id, trigger, disable_link_preview, full_match, action_on, trigger_for_admins, trigger_for_members, protect


async def tescape(client, m):
    msg = str(m.text.markdown.split(' ',1)[1])
    trigger = str(msg).split()[0]
    trlen = len(trigger)
    text = msg[trlen:]
    if str(trigger).startswith('"'):  
        fq = re.search(r'"([^"]*)"', msg)
        if fq:
           trigger = fq.group(0)[1:-1]
           trgend = fq.span()[1]
           text = msg[trgend:]

    disable_link_preview = True
    full_match = False
    action_on = "text"
    trigger_for_admins = True
    trigger_for_members = True
    protect = False
    buttons = ""
    
    pat = re.compile(r"\{([^}]+)\}")
    for gg in pat.finditer(rf"{text}"):
        gg_word = gg.group(0)
        gg_len1, gg_len2 = gg.span(0)[0], gg.span(0)[1]
    
        if gg_word == "{preview}":
            text = re.sub(r"{preview}", '', rf"{text}", 1, re.IGNORECASE)
            disable_link_preview = False
           # print(text)

        elif gg_word == "{full_match}":
            text = re.sub(r"{full_match}", '', rf"{text}", 1, re.IGNORECASE)
            full_match = True
            
        elif gg_word == "{admin}":
            text = re.sub(r"{admin}", '', rf"{text}", 1, re.IGNORECASE)
            trigger_for_members = False
            
        elif gg_word == "{members}":
            text = re.sub(r"{members}", '', rf"{text}", 1, re.IGNORECASE)
            trigger_for_admins = False
            
        elif gg_word == "{protect}":
            text = re.sub(r"{protect}", '', rf"{text}", 1, re.IGNORECASE)
            protect = True
   
        elif gg_word in action_lists:
            text = re.sub(rf"{gg_word}", '', rf"{text}", 1, re.IGNORECASE)
            action_on = gg_word[1:-1]
            
   # print(text)
    text = text.strip()
    try:
        patt = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{1,2})(.+?)(:same)?\))")
        ptn = patt.finditer(rf"{text}")
        for patn in ptn:
            buttons += patn.group(0)
            onebtn = str(patn.group(0)).strip()
            text = text.replace(onebtn, '')
        buttons = buttons.strip()

    except Exception as e:
        await m.reply_text(str(e))
   
    return text.strip(), trigger, disable_link_preview, full_match, action_on, trigger_for_admins, trigger_for_members, buttons, protect


async def _markup2(client, m):
    buttons = ""
    ogtext = ""
    text = ""
    typee = 0
    file_id = ""
    btns = ""
    if m.reply_to_message and m.reply_to_message.text:
        ogtext = m.reply_to_message.text
        text = m.reply_to_message.text.markdown
    elif m.reply_to_message and m.reply_to_message.caption:
        ogtext = m.reply_to_message.caption
        text = m.reply_to_message.caption.markdown

   # extracting buttons
    if text:
        patt = re.compile(r"(\[([^\[]+?)\]\((buttonurl):(?:/{1,2})(.+?)(:same)?\))")
        ptn = patt.finditer(str(text))
        try:
            for patn in ptn:
                btns += patn.group(0)
                onebtn = str(patn.group(0)).strip()
                text = text.replace(onebtn, '')
            btns = btns.strip()

        except Exception as e:
            await m.reply_text(str(e))
    
    try:

        geta = await tescape(client, m)
        text += geta[0]
        trigger = geta[1]
        disable_link_preview = geta[2]
        full_match = geta[3]
        action_on = geta[4]
        trigger_for_admins = geta[5]
        trigger_for_members = geta[6]
        btns += geta[7]
        protect = geta[8]
    except Exception as e:
        await m.reply_text(str(e))
        # pass
    if m.reply_to_message and m.reply_to_message.sticker:
        file_id = m.reply_to_message.sticker.file_id
        typee = 1
    elif m.reply_to_message and m.reply_to_message.photo:
        file_id = m.reply_to_message.photo.file_id
        typee = 2
    elif m.reply_to_message and m.reply_to_message.document:
        file_id = m.reply_to_message.document.file_id
        typee = 3
    elif m.reply_to_message and m.reply_to_message.video:
        file_id = m.reply_to_message.video.file_id
        typee = 4
    elif m.reply_to_message and m.reply_to_message.audio:
        file_id = m.reply_to_message.audio.file_id
        typee = 5
    elif m.reply_to_message and m.reply_to_message.animation:
        file_id = m.reply_to_message.animation.file_id
        typee = 6

    return btns, text, typee, file_id, trigger, disable_link_preview, full_match, action_on, trigger_for_admins, trigger_for_members, protect
