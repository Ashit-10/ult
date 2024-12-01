import os
import json
import re
from pyrogram import *
from pyrogram.types import *
from config import *
from group_bot import bot, sql, db
from group_bot.modules.antiflood import antiflood_go
import time
from group_bot.modules.helpers.db import create_db
from group_bot.modules.helpers.decode_btns import decode_btns
from group_bot.modules.helpers.filter_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.notes import group_notes, private_notes
from group_bot.modules.admin_check import is_admin, admins_col, immutable
from group_bot.modules.give_id import return_id
import html
from group_bot.modules.blocklist import ban, mute, tmute, kick_member, tban, tmute, warn


async def warns_check(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
  
    suid = await return_id(client, m)
    if not suid or not suid[0]:
        await m.reply_text("seems like you're not referring to any user !")
        return
    user_id = suid[0]
    chat_id = str(m.chat.id)
    if await immutable(client, m, chat_id, user_id) is True:
        if str(user_id).startswith('-1'):
            await m.reply_text(
                text="Your group/channel can't be warned !")
        else:
            await m.reply_text(
                text="Admins can't be warned !")
        return
    else:
        total_reason = ""
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        y = obj[f"{bot_id}"]['max_warns']
        with open("db/warns.txt", "r") as se:
               wob = json.load(se)
        try:
             reasons = wob["warns"][f"{chat_id}_{user_id}"]
        except KeyError:
             reasons = ""
        if len(str(reasons)) > 0:
            reason_lists = reasons.split('[%%%]')
            warn_numbers = len(reason_lists) - 1
            for xy in reason_lists:
                if len(str(xy)) > 0:
                    total_reason += f"- {xy}\n"
        else:
            warn_numbers = 0
        fnames = await client.get_chat(user_id)
       
        if not fnames.title:
            fname = html.escape(fnames.first_name)
            user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
        else:
             user = f"@{fnames.username}"
        if warn_numbers:
            await m.reply_text(
                text=f"{user} has {warn_numbers}/{y} warnings!\n<b>Reasons:</b>\n{total_reason}", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
        else:
            await m.reply_text(
                text=f"{user} have no warnings !")


async def save_warns(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
            return
        i_t = await return_id(client, m)
        if not i_t or not i_t[0]:
            await m.reply_text("seems like you're not referring to any user !")
            return
        user_id = i_t[0]
        add_reason = i_t[1]
        chat_id = str(m.chat.id)
        if await immutable(client, m, chat_id, user_id) is True:
            if str(user_id).startswith('-1'):
                await m.reply_text(
                    text="Your group/channel can't be warned !")
            else:
                await m.reply_text(
                    text="Admins can't be warned !")
            return
        else:
            if len(str(add_reason)) < 1:
                add_reason = None   
            y = obj[f"{bot_id}"]['max_warns']
            with open("db/warns.txt", "r") as se:
               wob = json.load(se)
            try:
                reasons = wob["warns"][f"{chat_id}_{user_id}"]
            except KeyError:
                reasons = ""         
            if len(str(reasons)) >= 1 and reasons:
                reason_lists = reasons.split('[%%%]')
                warn_numbers = len(reason_lists) - 1
                reasons += f"""{add_reason}[%%%]"""
            else:
                warn_numbers = 0
                reasons = f"""{add_reason}[%%%]"""
           
            wants = warn_numbers+1
            fnames = await client.get_chat(user_id)
    
            if not fnames.title:
                fname = html.escape(fnames.first_name)
                user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
            else:
               user = f"@{fnames.username}"
            if str(wants) >= str(y):     
                await warn_damage(client, m, user_id, chat_id)      
                with open("db/warns.txt", "w+") as se:
                    json.dump(wob, se, indent=6, sort_keys=True)
            else:
                warn_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text=f"Remove warn ", callback_data=f"{user_id}_unwarn")]
                ])
                try:
                    await m.reply_text(reply_markup=warn_keyboard,
                                      text=f"{user} has {wants}/{y} warnings! watch out Retard;\n<b>Reason:</b> {add_reason}", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                except Exception as cs:
                    await m.reply_text(text=str(cs))
                finally:
                    wob["warns"][f"{chat_id}_{user_id}"] = reasons
                    with open("db/warns.txt", "w+") as se:
                        json.dump(wob, se, indent=6, sort_keys=True)


async def dsave_warns(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, m.from_user.id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
            return
        try:
            await m.reply_to_message.delete()
        except:
            pass      
        i_t = await return_id(client, m)
        if not i_t or not i_t[0]:
            await m.reply_text("seems like you're not referring to any user !")
            return
        user_id = i_t[0]
        add_reason = i_t[1]
        chat_id = str(m.chat.id)
        if await immutable(client, m, chat_id, user_id) is True:
            if str(user_id).startswith('-1'):
                await m.reply_text(
                    text="Your group/channel can't be warned !")
            else:
                await m.reply_text(
                    text="Admins can't be warned !")
            return
        else:
            if len(str(add_reason)) < 1:
                add_reason = None
            with open(f"db/X{chat_id}_db.txt", 'r') as f:
                obj = json.load(f)
            y = obj[f"{bot_id}"]['max_warns']
            with open("db/warns.txt", "r") as se:
               wob = json.load(se)
            try:
                reasons = wob["warns"][f"{chat_id}_{user_id}"]
            except KeyError:
                reasons = ""
            if len(str(reasons)) > 0 and reasons:
                reason_lists = reasons.split('[%%%]')
                warn_numbers = len(reason_lists) - 1
                reasons += f"""{add_reason}[%%%]"""
            else:
                warn_numbers = 0
                reasons = f"""{add_reason}[%%%]"""
            wants = warn_numbers+1
            fnames = await client.get_chat(user_id)
    
            if not fnames.title:
                fname = html.escape(fnames.first_name)
                user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
            else:
               user = f"@{fnames.username}"
            if str(wants) >= str(y):
                await warn_damage(client, m, user_id, chat_id)
                del wob["warns"][f"{chat_id}_{user_id}"]
                with open("db/warns.txt", "w+") as se:
                    json.dump(wob, se, indent=6, sort_keys=True)
            else:
                warn_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text=f"Remove warn (Admin only)", callback_data=f"{user_id}_unwarn")]
                ])
                try:
                    await m.reply_text(reply_markup=warn_keyboard,
                                      text=f"{user} has {wants}/{y} warnings!  watch out Retard;\n<b>Reason:</b> {add_reason}", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                except Exception as cs:
                    await m.reply_text(text=str(cs))
                finally:
                    wob["warns"][f"{chat_id}_{user_id}"] = reasons
                    with open("db/warns.txt", "w+") as se:
                        json.dump(wob, se, indent=6, sort_keys=True)


async def sdsave_warns(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, m.from_user.id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
            return
        try:
            await m.reply_to_message.delete()
        except:
            pass      
        i_t = await return_id(client, m)
        if not i_t or not i_t[0]:
            await m.reply_text("seems like you're not referring to any user !")
            return
        user_id = i_t[0]
        add_reason = i_t[1]
        chat_id = str(m.chat.id)
        try:
            await m.delete()
        except:
           pass
        if await immutable(client, m, chat_id, user_id) is True:
            if str(user_id).startswith('-1'):
                await m.reply_text(
                    text="Your group/channel can't be warned !")
            else:
                await m.reply_text(
                    text="Admins can't be warned !")
            return
        else:
            if len(str(add_reason)) < 1:
                add_reason = None
            with open(f"db/X{chat_id}_db.txt", 'r') as f:
                obj = json.load(f)
            y = obj[f"{bot_id}"]['max_warns']
            with open("db/warns.txt", "r") as se:
               wob = json.load(se)
            try:
                reasons = wob["warns"][f"{chat_id}_{user_id}"]
            except KeyError:
                reasons = ""
            if len(str(reasons)) > 0 and reasons:
                reason_lists = reasons.split('[%%%]')
                warn_numbers = len(reason_lists) - 1
                reasons += f"""{add_reason}[%%%]"""
            else:
                warn_numbers = 0
                reasons = f"""{add_reason}[%%%]"""
            wants = warn_numbers+1
            fnames = await client.get_chat(user_id)
    
            if not fnames.title:
                fname = html.escape(fnames.first_name)
                user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
            else:
               user = f"@{fnames.username}"
            if str(wants) >= str(y):
                await warn_damage(client, m, user_id, chat_id)
                del wob["warns"][f"{chat_id}_{user_id}"]
                with open("db/warns.txt", "w+") as se:
                    json.dump(wob, se, indent=6, sort_keys=True)
            else:
                warn_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text=f"Remove warn (Admin only)", callback_data=f"{user_id}_unwarn")]
                ])
                try:
                    await m.reply_text(reply_markup=warn_keyboard,
                                      text=f"{user} has {wants}/{y} warnings!  watch out Retard;\n<b>Reason:</b> {add_reason}", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                except Exception as cs:
                    await m.reply_text(text=str(cs))
                finally:
                    wob["warns"][f"{chat_id}_{user_id}"] = reasons
                    with open("db/warns.txt", "w+") as se:
                        json.dump(wob, se, indent=6, sort_keys=True)

async def ssave_warns(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
            return
        i_t = await return_id(client, m)
        if not i_t or not i_t[0]:
            await m.reply_text("seems like you're not referring to any user !")
            return
        user_id = i_t[0]
        add_reason = i_t[1]
        chat_id = str(m.chat.id)
        try:
            await m.delete()
        except:
           pass
        if await immutable(client, m, chat_id, user_id) is True:
            if str(user_id).startswith('-1'):
                await m.reply_text(
                    text="Your group/channel can't be warned !")
            else:
                await m.reply_text(
                    text="Admins can't be warned !")
            return
        else:
            if len(str(add_reason)) < 1:
                add_reason = None   
            y = obj[f"{bot_id}"]['max_warns']
            with open("db/warns.txt", "r") as se:
               wob = json.load(se)
            try:
                reasons = wob["warns"][f"{chat_id}_{user_id}"]
            except KeyError:
                reasons = ""         
            if len(str(reasons)) >= 1 and reasons:
                reason_lists = reasons.split('[%%%]')
                warn_numbers = len(reason_lists) - 1
                reasons += f"""{add_reason}[%%%]"""
            else:
                warn_numbers = 0
                reasons = f"""{add_reason}[%%%]"""
           
            wants = warn_numbers+1
            fnames = await client.get_chat(user_id)
    
            if not fnames.title:
                fname = html.escape(fnames.first_name)
                user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
            else:
               user = f"@{fnames.username}"
            if str(wants) >= str(y):                
                await warn_damage(client, m, user_id, chat_id)      
                with open("db/warns.txt", "w+") as se:
                    json.dump(wob, se, indent=6, sort_keys=True)
            else:
                warn_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text=f"Remove warn ", callback_data=f"{user_id}_unwarn")]
                ])
                try:
                    await m.reply_text(reply_markup=warn_keyboard,
                                      text=f"{user} has {wants}/{y} warnings! watch out Retard;\n<b>Reason:</b> {add_reason}", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                except Exception as cs:
                    await m.reply_text(text=str(cs))
                finally:
                    wob["warns"][f"{chat_id}_{user_id}"] = reasons
                    with open("db/warns.txt", "w+") as se:
                        json.dump(wob, se, indent=6, sort_keys=True)

async def rmwarns(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
            return
        if " " in m.text or m.reply_to_message:            
            i_t = await return_id(client, m)
            user_id = i_t[0]
            add_reason = i_t[1]
            if not i_t or not i_t[0]:
                await m.reply_text("seems like you're not referring to any user !")
                return
            if await immutable(client, m, chat_id, user_id) is True:
                if str(user_id).startswith('-1'):
                    await m.reply_text(
                        text="Your group/channel can't be warned !")
                else:
                    await m.reply_text(
                        text="Admins can't be warned !")
                return
            else:
                if m.sender_chat:
                    ok_user = html.escape(m.sender_chat.title)
                else:
                    ok_id = m.from_user.id
                    ok_fname = html.escape(m.from_user.first_name)
                    ok_user = f"""<a href="tg://user?id={ok_id}">{ok_fname}</a>"""
                fnames = await client.get_chat(user_id)              
                
                if not fnames.title:
                    fname = html.escape(fnames.first_name)
                    user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
                else:
                    user = f"@{fnames.username}"
           
            
                with open("db/warns.txt", "r") as se:
                    wob = json.load(se)
                try:
                     reasons = wob["warns"][f"{chat_id}_{user_id}"]
                except KeyError:
                     reasons = ""
                if len(str(reasons)) > 1 and reasons:
                    reasons = ''                    
                    del wob["warns"][f"{chat_id}_{user_id}"]
                    with open("db/warns.txt", "w+") as se:
                         json.dump(wob, se, indent=6, sort_keys=True)
                
                    await m.reply_text(
                              text=f"Admin {ok_user} removed {user}'s warnings !", parse_mode=enums.ParseMode.HTML)
                    
                else:
          
                    await m.reply_text(
                        text=f"{user} hadn't any warnings !")
        else:
            await m.reply_text("seems like you're not referring to any user !")


async def unwarn(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
            return
        if " " in m.text or m.reply_to_message:            
            i_t = await return_id(client, m)
            user_id = i_t[0]
            add_reason = i_t[1]
            if not i_t or not i_t[0]:
                await m.reply_text("seems like you're not referring to any user !")
                return
            if await immutable(client, m, chat_id, user_id) is True:
                if str(user_id).startswith('-1'):
                    await m.reply_text(
                        text="Your group/channel can't be warned !")
                else:
                    await m.reply_text(
                        text="Admins can't be warned !")
                return
            else:
                if m.sender_chat:
                    ok_user = html.escape(m.sender_chat.title)
                else:
                    ok_id = m.from_user.id
                    ok_fname = html.escape(m.from_user.first_name)
                    ok_user = f"""<a href="tg://user?id={ok_id}">{ok_fname}</a>"""
                fnames = await client.get_chat(user_id)          
                
                if not fnames.title:
                    fname = html.escape(fnames.first_name)
                    user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
                else:
                    user = f"@{fnames.username}"
                with open("db/warns.txt", "r") as se:
                    wob = json.load(se)
                try:
                     reasons = wob["warns"][f"{chat_id}_{user_id}"]
                except KeyError:
                     reasons = ""
                if len(str(reasons)) > 1 and reasons:
                    fst = str(reasons[:-5]).rfind("[%%%]")
                    reasons = reasons[:(fst+5)]
                    await m.reply_text(
                        text=f"Admin {ok_user} removed {user}'s last warning !", parse_mode=enums.ParseMode.HTML)                      
                    with open("db/warns.txt", "w+") as se:
                         json.dump(wob, se, indent=6, sort_keys=True)
                else:
                    await m.reply_text(
                        text=f"{user} hadn't any warnings !")
        else:
            await m.reply_text("seems like you're not referring to any user !")


async def set_warn_limit(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
            return
        chat_id = m.chat.id
        if " " in m.text:
            inpt = m.text.split()[1]
        else:
            await m.reply_text("What value to set ?")
            return
        if str(inpt).isdigit:
            try:
                obj[f"{bot_id}"]["max_warns"] = int(inpt)
                with open(f"db/X{chat_id}_db.txt", 'w+') as f:
                    json.dump(obj, f, indent=4)
                await m.reply_text(
                    f"Successfully changed warning limit to {inpt} !")
            except Exception as e:
                await m.reply_text(str(e))
        else:
            await m.reply_text('Please give a valid integer !')


blocklist_actions = ['ban', 'kick', 'tban']


async def set_warn_mode(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["warn"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id

    if await is_admin(client, m, m.chat.id, user_id) is True:
        chat_id = m.chat.id
        if " " in m.text:
            if str(m.text.split()[1]) in blocklist_actions:
                action = m.text.split(' ', 1)[1]
        else:
            await m.reply_text(
                f'Give a warn mode to set !\n {blocklist_actions}')
            return
        try:
            obj[f"{bot_id}"]["warn_action"] = str(action)
            with open(f"db/X{chat_id}_db.txt", 'w+') as f:
                json.dump(obj, f, indent=4)
            await m.reply_text(
                f"Successfully updated warn mode .\n**action**: `{action}` !", quote=True)
        except Exception as e:
            await m.reply_text(str(e))


# callback warn damage

async def warn_damage(client, m, user_id, chat_id):
    try:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
            warn_action = obj[f'{bot_id}']['warn_action']
        send_keyboard = None
        text = 'Warning limit crossed !'
        fnames = await client.get_chat(user_id)
        fname = fnames.title
        user = f"@{fnames.username}"
        if not fname:
            fname = fnames.first_name
            user = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
        show_msg = True
        if warn_action == 'ban':
            await ban(client, m, chat_id, user_id, text, user, show_msg, send_keyboard)
        elif warn_action == 'kick':
            await kick_member(
                client, m, chat_id, user_id, text, user, show_msg)
        elif 'tban' in warn_action:
            await tban(client, m, chat_id, user_id, str(
                warn_action).split()[1], text, user, show_msg, send_keyboard)

    except Exception as e:
        print(e)
