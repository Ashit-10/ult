import time
from datetime import timedelta
import datetime
import os
import json
from pyrogram import *
from pyrogram.types import *
import re
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.helpers.decode_btns import decode_btns
from config import *
import random
import string
from group_bot import bot
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import time
import asyncio 
tz = pytz.timezone("Asia/kolkata")
sj = BackgroundScheduler(timezone="Asia/kolkata")


async def welcome_sender(client, m, i, chat_id, rtm, captcha, user_id, is_bot, clean, mem, captcha_mode, oldMember):
    text = i['text']
    if text:
        text = str(await make_answers(client, m, str(text), mem))
    else:
        text = ""
    Markup = i['btn_url']
    if Markup:
        Markup = await decode_btns(Markup)
    if captcha is True and is_bot is False and not oldMember:
        if captcha_mode == "button":
            if not Markup:
                Markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=f"Click here to prove you're a human", url=f"t.me/{bot_username}?start={chat_id}_CAPTCHA_{user_id}")]])
            else:
                Markup.inline_keyboard.append(
                    [InlineKeyboardButton(text="Click here to prove you're a human", url=f"t.me/{bot_username}?start={chat_id}_CAPTCHA_{user_id}")])
        elif captcha_mode == "text":
            if not Markup:
                Markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=f"🤖  Verify now !",
                                          callback_data=f"{user_id}_givecaptcha")]])
            else:
                Markup.inline_keyboard.append(
                    [InlineKeyboardButton(text=f"🤖  Verify now !",
                                          callback_data=f"{user_id}_givecaptcha")])
            text = text.strip()
            text = f"{text}\n\n** Complete the captcha by pressing `Verify now` button below !**"
    file_id = i['file_id']
    typee = i['typee']
    disable_link_preview = i['disable_link_preview']
    # old gandu
 #   if oldMember:
        
    if typee == 0:
        try:
            wm = await client.send_message(chat_id=chat_id,
                                           reply_to_message_id=rtm,
                                           parse_mode=enums.ParseMode.MARKDOWN,
                                           disable_web_page_preview=disable_link_preview,
                                           text=text,
                                           reply_markup=Markup,
                                           )
            if clean is True:
                if captcha_mode != "text" or captcha is not True:
                    asyncio.create_task(
                        cleaner(client, m, chat_id, wm.id, user_id))
                    if not is_bot:
                        asyncio.create_task(kicksh(client, m, chat_id, user_id))
        except Exception as e:
             pass
           # await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 1:
        try:
            wm = await client.send_sticker(chat_id=chat_id,
                                           reply_to_message_id=rtm,
                                           sticker=file_id,
                                           reply_markup=Markup)
            if clean is True:
                if captcha_mode != "text" or captcha is not True:
                    asyncio.create_task(
                        cleaner(client, m, chat_id, wm.id, user_id))
                    if not is_bot:
                        asyncio.create_task(kicksh(client, m, chat_id, user_id))
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 2:
        try:
            wm = await client.send_photo(chat_id=chat_id,
                                         reply_to_message_id=rtm,
                                         photo=file_id,
                                         caption=text,
                                         parse_mode=enums.ParseMode.MARKDOWN,
                                         reply_markup=Markup)    
            if clean is True:
                if captcha_mode != "text" or captcha is not True:               
                    asyncio.create_task(
                        cleaner(client, m, chat_id, wm.id, user_id))
                    if not is_bot:
                        asyncio.create_task(kicksh(client, m, chat_id, user_id))
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 3:
        try:
            wm = await client.send_document(chat_id=chat_id,
                                            reply_to_message_id=rtm,
                                            document=file_id,
                                            reply_markup=Markup,
                                            caption=text,
                                            parse_mode=enums.ParseMode.MARKDOWN,

                                            )
            if clean is True:
                if captcha_mode != "text" or captcha is not True:
                    asyncio.create_task(
                        cleaner(client, m, chat_id, wm.id, user_id))
                    if not is_bot:
                        asyncio.create_task(kicksh(client, m, chat_id, user_id))
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 4:
        try:
            wm = await client.send_video(chat_id=chat_id,
                                         #  allow_sending_without_reply=True,
                                         reply_to_message_id=rtm,
                                         video=file_id,
                                         reply_markup=Markup,
                                         caption=text,
                                         parse_mode=enums.ParseMode.MARKDOWN,

                                         )
            if clean is True:
                if captcha_mode != "text" or captcha is not True:
                    asyncio.create_task(
                        cleaner(client, m, chat_id, wm.id, user_id))
                    if not is_bot:
                        asyncio.create_task(kicksh(client, m, chat_id, user_id))
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 5:
        try:
            wm = await client.send_audio(chat_id=chat_id,
                                         #  allow_sending_without_reply=True,
                                         reply_to_message_id=rtm,
                                         audio=file_id,
                                         reply_markup=Markup,
                                         caption=text,
                                         parse_mode=enums.ParseMode.MARKDOWN,

                                         )
            if clean is True:
                if captcha_mode != "text" or captcha is not True:
                    asyncio.create_task(
                        cleaner(client, m, chat_id, wm.id, user_id))
                    if not is_bot:
                        asyncio.create_task(kicksh(client, m, chat_id, user_id))
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 6:
        try:
            wm = await client.send_animation(chat_id=chat_id,
                                             reply_to_message_id=rtm,
                                             animation=file_id,
                                             reply_markup=Markup,
                                             caption=text,
                                             parse_mode=enums.ParseMode.MARKDOWN,
                                             )
            if clean is True:
                if captcha_mode != "text" or captcha is not True:
                    asyncio.create_task(
                        cleaner(client, m, chat_id, wm.id, user_id))
                    if not is_bot:
                        asyncio.create_task(kicksh(client, m, chat_id, user_id))
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True


async def cleaner(client, m, chat_id, msgid, user_id):
    ct = time.time()
    ifjobs = sj.get_job(f"{chat_id}")
    if ifjobs:
        jargs = ifjobs.args[0]
        try:
            msg_id = str(jargs).split('_')[1]
            await client.delete_messages(chat_id=m.chat.id, message_ids=int(msg_id))
            sj.remove_job(f"{chat_id}")
        except Exception as r:
            sj.remove_job(f"{chat_id}")
        finally:
            det = datetime.datetime.now(tz)+timedelta(seconds=600)
            sj.add_job(cw, "date", run_date=det, args=[
                f"{chat_id}_{msgid}_{user_id}"], id=f"{chat_id}")
    else:
        det = datetime.datetime.now(tz)+timedelta(seconds=600)
        sj.add_job(cw, "date", run_date=det, args=[
                   f"{chat_id}_{msgid}_{user_id}"], id=f"{chat_id}")
    

def cw(info):
    infos = str(info).split('_')
    chat_id = infos[0]
    msgid = infos[1]
    user_id = infos[2]
    try:
        bot.delete_messages(chat_id=int(chat_id), message_ids=int(msgid))
    except Exception as wth:
        print("Below is the error of cleanwelcome")
        print(wth)


async def kicksh(client, m, chat_id, user_id):
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["on_off"]["captchakick"] is True:
        ifjobs = sj.get_job(f"{chat_id}_{user_id}_de_kick")
        if ifjobs:
            sj.remove_job(f"{chat_id}_{user_id}_de_kick")
        det = datetime.datetime.now(tz)+timedelta(seconds=3600)
        sj.add_job(kicksch, "date", run_date=det, args=[
            f"{chat_id}_{user_id}"], id=f"{chat_id}_{user_id}_de_kick")
      

def kicksch(info):
    infos = str(info).split('_')
    chat_id = infos[0]
    user_id = infos[1]
    LeaveHim = None
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["on_off"]["captchakick"] is True:
        with open(f"db/mem/X{chat_id}.txt", 'r') as f:
            objs = json.load(f)
        for u in objs[str(chat_id)]:
            if int(u) == int(user_id):
                LeaveHim = True
                break
                return

        if not LeaveHim:
            try:
                user = bot.get_users(int(user_id))
                bot.ban_chat_member(chat_id=chat_id,
                                      until_date=time.time() + 35,
                                      user_id=user_id)
                bot.send_message(int(
                    chat_id), f"kicked {user.mention} for not verifying CAPTCHA, they can try again later !")                
            except:
                pass
            finally:
                bot.unban_chat_member(chat_id=int(
                    chat_id), user_id=int(user_id))
