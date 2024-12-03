from time import time as timenow
import json
from pyrogram import *
from pyrogram.types import *
import re
from datetime import datetime, timedelta
from config import *
from group_bot import bot
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
from group_bot.modules.give_id import return_id
from group_bot import bot, mention_html
import asyncio 
rdb = {}


async def check_my_channel(chat_id):
    my_channel_id = 69
    my_ch = await client.get_chat(chat_id)
    try:
        my_channel_id = my_ch.linked_chat.id
    except:
        my_channel_id = 69
    return my_channel_id

let = {}
# @bot.on_message(filters.command([
   # 'mute', 'dmute', 'smute', 'tmute', 'unmute',
 #   'ban', 'dban', 'sban', 'tban', 'unban',
  #  'kick', 'dkick', 'skick'],
#    ['!', '/']) & ~filters.private & ~filters.edited & filters.text)
async def mute(client, m):
    chat_id = m.chat.id
    verify_sender = None
    if m.sender_chat:
        user_id = m.sender_chat.id
        verify_sender = True
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    do_mute = obj[f"{bot_id}"]["enable_disable"]["mute"]
    do_ban = obj[f"{bot_id}"]["enable_disable"]["ban"]
    do_kick = obj[f"{bot_id}"]["enable_disable"]["kick"]
 
    if not await is_admin(client, m, m.chat.id, my_bot_id):
        await m.reply_text("Make me admin to do these stuffs !")
        return
    if "mute" in str(m.text.split()[0])[1:] and do_mute is not True:
        return
    elif "ban" in str(m.text.split()[0])[1:] and do_ban is not True:
        return
    elif "kick" in str(m.text.split()[0])[1:] and do_kick is not True:
        return
    if (m.text and " " not in m.text and not m.reply_to_message) or (m.caption and " " not in m.caption and not m.reply_to_message):
        await m.reply_text("You aren't refering to any user !")
        return
    if verify_sender:
       vbtn = await m.reply_text(text="It looks like you're anonymous, Tap this button to confirm your identity !", reply_markup=InlineKeyboardMarkup([
             [InlineKeyboardButton(text=f"verify admin", callback_data=f"verifyanonadmin_{user_id}")]]))
       let.update({int(chat_id): m})
    else:
        asyncio.create_task(
            verified(client, m, user_id, verify_sender))
    
    
    
async def verified(client, m, user_id, verify_sender):
    if verify_sender:
        m = let.get(int(m.chat.id))
    if await can_restrict(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_RESTRICT_MEMBERS]")
        return
    if ' ' in m.text or m.reply_to_message:
        user_id = None
        statv = await return_id(client, m)
        userid = statv[0]
        reason = statv[1]
        print(userid)
        if not userid and len(str(userid)) < 5:
            await m.reply_text(
                "seems like you're not referring to any user !", quote=True)
            return
        if str(m.text.split()[0])[1:] == "mute":
            if verify_sender:
                tellme = "vmutev"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vmute(client, m, user_id, userid, reason))

        elif str(m.text.split()[0])[1:] == "dmute":
            if verify_sender:
                tellme = "vdmutev"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vdmute(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "smute":
            if verify_sender:
                tellme = "vsmutev"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vsmute(client, m, user_id, userid, reason))

        elif str(m.text.split()[0])[1:] == "tmute":
            if verify_sender:
                tellme = "vtmutev"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vtmute(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "unmute":
            if verify_sender:
                tellme = "vunmutev"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vunmute(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "ban":
            if verify_sender:
                tellme = "vbanv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vban(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "dban":
            if m.reply_to_message:
                mid = m.reply_to_message.id
            else:
                mid = None
            if verify_sender:
                tellme = "vdbanv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vdban(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "sban":
            if verify_sender:
                tellme = "vsbanv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vsban(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "tban":
            if verify_sender:
                tellme = "vtbanv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vtban(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "unban":
            if verify_sender:
                tellme = "vunbanv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vunban(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "kick":
            if verify_sender:
                tellme = "vkickv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vkick(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "dkick":
            if verify_sender:
                tellme = "vdkickv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vdkick(client, m, user_id, userid, reason))
        elif str(m.text.split()[0])[1:] == "skick":
            if verify_sender:
                tellme = "vskickv"
                asyncio.create_task(
                    send_vbtn(client, m, tellme, userid, reason))
            else:
                asyncio.create_task(
                    vskick(client, m, user_id, userid, reason))

    else:
        await m.reply_text(
            "seems like you're not referring to any user !", quote=False)


async def send_vbtn(client, m, tellme, userid, reason):
    vbtn = await m.reply_text(text="It looks like you're anonymous, Tap this button to confirm your identity !", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text=f"verify admin", callback_data=f"verifyadmin_{tellme}_{userid}")]]))
    if m.reply_to_message:
        rdb.update({f"{m.chat.id}_{vbtn.id}": {
                   "id": m.id, "reason": reason, "rtm": m.reply_to_message.id}})
    else:
        rdb.update({f"{m.chat.id}_{vbtn.id}": {
                   "id": m.id, "reason": reason}})


async def vmute(client, m, auser, user_id, reason):
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to mute ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Muting an admin !?")
        return
    else:
        if str(user_id).startswith('-1'):
            await m.edit("I can't mute Channels !")
            return
        try:
            statsz = await client.get_chat_member(
                m.chat.id, user_id)
            stat = statsz
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        except Exception as fg:
            if str(fg) == "list index out of range":
                await m.edit("I can't mute Channels !")
            else:
                fg = str(fg).split('-')[0]
                await m.edit(str(fg))
            return

        ct = int(timenow())
        till_d = ct + 1
        status = str(stat.status)
        if status != "ChatMemberStatus.MEMBER" and stat.permissions.can_send_messages is False:
            till_d = stat.until_date.strftime("%Y%m%d%H%M%S")
        if int(till_d) - ct > 25920000:
            await m.edit(
                text=f"{user} was already permanently muted !")
        else:
            if len(str(reason)) < 1:
                reason = None
            try:
                await client.restrict_chat_member(chat_id=chat_id,
                                                  user_id=user_id,
                                                  permissions=ChatPermissions()

                                                  )

                await m.edit(
                    text=f"""Muted {user} forever !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)

            except Exception as f:
                f = str(f).split('-')[0]
                await m.edit(text=str(f))
            finally:
                try:
                    rdb.pop(f"{m.chat.id}_{m.id}")
                except:
                    pass


async def vunmute(client, m, auser, user_id, reason):
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to unmute ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Unmuting an admin !?")
    else:
        if str(user_id).startswith('-1'):
            await m.edit("I can't mute Channels !")
            return
        try:
            statsz = await client.get_chat_member(
                m.chat.id, user_id)
            stat = statsz
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        except Exception as fg:
            if str(fg) == "list index out of range":
                await m.edit("I wouldn't mute that Channel !")
            else:
                fg = str(fg).split('-')[0]
                await m.edit(str(fg))
            return
        if str(stat.status) == "ChatMemberStatus.MEMBER" or stat.permissions.can_send_messages is True:
            await m.edit(
                text=f"{user} can already speak freely !")
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

                await m.edit(
                    text=f"""Unmuted {user} !""")
            except Exception as f:
                f = str(f).split('-')[0]
                await m.edit(text=str(f))
            finally:
                try:
                    rdb.pop(f"{m.chat.id}_{m.id}")
                except:
                    pass


async def vsmute(client, m, auser, user_id, reason):
    try:
        m = m.message
        await m.delete()
        await m.reply_to_message.delete()
    except:
        pass
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
        rtm = rm['rtm']
    else:
        mid = m.id
        rtm = m.reply_to_message.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await client.send_message(text="Unmuting an admin !?", chat_id=chat_id)
        return
    else:
        asyncio.create_task(dm(client, m, rtm))
        if str(user_id).startswith('-1'):
            await client.send_message("I can't mute Channels !", chat_id=chat_id)
            return
        try:
            statsz = await client.get_chat_member(
                m.chat.id, user_id)
            stat = statsz
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        except Exception as fg:
            if str(fg) == "list index out of range":
                await client.send_message("I can't mute Channels !", chat_id=chat_id)
            else:
                fg = str(fg).split('-')[0]
                await client.send_message(text=str(fg), chat_id=chat_id)
            return
        ct = int(timenow())
        till_d = ct + 1
        if str(stat.status) != "ChatMemberStatus.MEMBER" and stat.permissions.can_send_messages is False:
            till_d = stat.until_date.strftime("%Y%m%d%H%M%S")
        if int(till_d) - ct > 25920000:
            await m.edit(
                text=f"{user} was already muted permanently !", chat_id=chat_id)
        else:
            try:
                await client.restrict_chat_member(chat_id=chat_id,
                                                  user_id=user_id,
                                                  permissions=ChatPermissions()

                                                  )

            except Exception as e:
                e = str(e).split('-')[0]
                await client.send_message(
                    text=str(e), chat_id=chat_id)
            finally:
                try:
                    rdb.pop(f"{m.chat.id}_{m.id}")
                except:
                    pass


async def dm(client, m, mid):
    try:
        await client.delete_messages(chat_id=m.chat.id, ids=mid)
    except:
        pass


async def vdmute(client, mes, auser, user_id, reason):
    rtm = None
    try:
        m = mes.message
    except:
        m = await mes.reply_text("`Trying to mute ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
        rtm = rm['rtm']
    else:
        mid = m.id
        rtm = mes.reply_to_message.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Muting an admin !?")
        return
    else:
        asyncio.create_task(dm(client, m, rtm))
        if str(user_id).startswith('-1'):
            await m.edit("I can't mute Channels !")
            return
        try:
            statsz = await client.get_chat_member(
                m.chat.id, user_id)
            stat = statsz
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        except Exception as fg:
            if str(fg) == "list index out of range":
                await m.edit("I can't mute Channels !")
            else:
                fg = str(fg).split('-')[0]
                await m.edit(str(fg))
            return
        
        ct = int(timenow())
        till_d = ct + 1
        if str(stat.status) != "ChatMemberStatus.MEMBER" and stat.permissions.can_send_messages is False:
            till_d = stat.until_date.strftime("%Y%m%d%H%M%S")
        if int(till_d) - ct > 25920000:
            await m.edit(
                text=f"{user} was already muted permanently !")
        else:
            if len(str(reason)) < 1:
                reason = None
            try:
                await client.restrict_chat_member(chat_id=chat_id,
                                                  user_id=user_id,
                                                  permissions=ChatPermissions()

                                                  )

                await m.edit(
                    text=f"""Muted {user} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
            except Exception as f:
                f = str(f).split('-')[0]
                await m.edit(text=str(f))
            finally:
                try:
                    rdb.pop(f"{m.chat.id}_{m.id}")
                except:
                    pass


async def vtmute(client, m, auser, user_id, reason):
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to mute ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Muting an admin !?")
    else:
        if str(user_id).startswith('-1'):
            await m.edit("I can't mute Channels !")
            return
        try:
            statsz = await client.get_chat_member(
                m.chat.id, user_id)
            stat = statsz
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        except Exception as fg:
            if str(fg) == "list index out of range":
                await m.edit("I can't mute Channels !")
            else:
                fg = str(fg).split('-')[0]
                await m.edit(str(fg))
            return
        if_el = f"Muted {user}"
        if str(stat.status) != "ChatMemberStatus.MEMBER" and stat.permissions.can_send_messages is False:
            if_el = f"{user} was already muted, anyways Muted him"
        try:
            if len(str(reason)) < 1 or not reason:
                reason = None
                action_mode = ""
            else:
                action_mode = reason.split()[0]
                reason = reason[(len(action_mode) + 1):]
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
            elif 'w' in action_mode:
                dtime = int(str(action_mode).replace(
                    'w', '')) * 3600 * 24 * 7
                if dtime == 604800:
                    action_mode = action_mode.replace('w', ' week')
                else:
                    action_mode = action_mode.replace('w', ' weeks')
            else:
                await m.edit(
                    text="Time is not specified !")
                return
            if dtime:
                try:
                    if len(str(reason)) < 1:
                        reason = None
                    await client.restrict_chat_member(chat_id=chat_id,
                                                      user_id=user_id,
                                                      until_date=datetime.now() + timedelta(seconds=dtime),
                                                      permissions=ChatPermissions()

                                                      )

                    await m.edit(text=f"""{if_el} for {action_mode} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
                except Exception as ctm:
                    ctm = str(ctm).split('-')[0]
                    await m.edit(text=str(ctm))
                finally:
                    try:
                        rdb.pop(f"{m.chat.id}_{m.id}")
                    except:
                        pass
        except Exception as r:
            await m.edit(str(r))


async def vban(client, m, auser, user_id, reason):
    stb = ""
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to ban ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Banning an admin !?")
    else:
        if str(user_id).startswith('-1'):
            print(user_id)
            pu = await client.get_chat(user_id)
            print(pu)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(int(user_id)))
                user = await mention_html(userw.id, userw.first_name)
            except Exception as er:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = (await client.get_chat_member(chat_id, user_id)).status
            except Exception as cf:
                if "user is not a member of this chat" in str(cf) and str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "channel "
                elif "user is not a member of this chat" in str(cf) and not str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "a non-member "
                else:
                    cf = str(cf).split('-')[0]
                    await m.edit(str(cf))
                    return
            if str(stat) == "ChatMemberStatus.BANNED" and str(stat) != "ChatMemberStatus.MEMBER":
                await m.edit(
                    text=f"{user} is already banned !")
            else:
                if len(str(reason)) < 1:
                    reason = None
                try:
                    await client.ban_chat_member(chat_id=chat_id,
                                                 user_id=user_id)
                    await m.edit(
                        text=f"""Banned {stb}{user} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
                except Exception as cb:
                    cb = str(cb).split('-')[0]
                    await m.edit(str(cb))
        else:
            await m.edit("You are trying to ban your own chat 🤨 !")


async def vtban(client, m, auser, user_id, reason):
    stb = ""
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to ban ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Banning an admin !?")
    else:
        if str(user_id).startswith('-1'):
            pu = await client.get_chat(user_id)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = (await client.get_chat_member(chat_id, user_id)).status
            except Exception as cf:
                if "user is not a member of this chat" in str(cf) and str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "channel "
                elif "user is not a member of this chat" in str(cf) and not str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "a non-member "
                else:
                    cf = str(cf).split('-')[0]
                    await m.edit(str(cf))
                    return
            if str(stat) == "ChatMemberStatus.BANNED" and str(stat) != "ChatMemberStatus.MEMBER":
                await m.edit(
                    text=f"{user} is already banned !")
                return
            else:
                if len(str(reason)) < 1 or not reason:
                    reason = None
                    action_mode = ""
                else:
                    action_mode = reason.split()[0]
                    reason = reason[(len(action_mode) + 1):]
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
                elif 'w' in action_mode:
                    dtime = int(str(action_mode).replace(
                        'w', '')) * 3600 * 24 * 7
                    if dtime == 604800:
                        action_mode = action_mode.replace('w', ' week')
                    else:
                        action_mode = action_mode.replace('w', ' weeks')
                else:
                    await m.edit(
                        text="Time is not specified !")
                    return
                if dtime:
                    if len(str(reason)) < 1:
                        reason = None
                    try:                    
                        await client.ban_chat_member(chat_id=chat_id,
                                                     until_date=datetime.now() + timedelta(seconds=dtime),
                                                     user_id=user_id)
                        await m.edit(
                            text=f"""Banned {stb}{user} for {action_mode} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
                    except Exception as cb:
                        cb = str(cb).split('-')[0]
                        await m.edit(str(cb))
        else:
            await m.edit("You are trying to ban your own chat 🤨 !")


async def vunban(client, m, auser, user_id, reason):
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to unban ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Unbanning an admin !?")
    else:
        if str(user_id).startswith('-1'):
            pu = await client.get_chat(user_id)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = await client.get_chat_member(chat_id, user_id)
            except Exception as cf:
                if "caused by" in str(cf):
                    cf = str(cf).split('-')[0]
                    await m.edit(str(cf))
                else:
                    cf = str(cf).split('-')[0]
                    await m.edit(str(cf))
                return
            if str(stat.status) != "ChatMemberStatus.BANNED":
                await m.edit(
                    text=f"{user} is not banned yet !")
            else:
                if len(str(reason)) < 1:
                    reason = None
                try:
                    await client.unban_chat_member(chat_id=chat_id,
                                                   user_id=user_id)
                    await m.edit(
                        text=f"""Unbanned {user} !""")
                except Exception as cb:
                    cb = str(cb).split('-')[0]
                    await m.edit(text=str(cb))
        else:
            await m.edit("You are trying to Unban your own chat 🤨 !")


async def vdban(client, mes, auser, user_id, reason):
    stb = ""
    try:
        m = mes.message
    except:
       # rtm = m.reply_to_message.id
        m = await mes.reply_text("`Trying to ban ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
        rtm = rm['rtm']
    else:
        mid = m.id
        rtm = mes.reply_to_message.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Banning an admin !?")
    else:
        if str(user_id).startswith('-1'):
            pu = await client.get_chat(user_id)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = (await client.get_chat_member(chat_id, user_id)).status
            except Exception as cf:
                if "user is not a member of this chat" in str(cf) and str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "channel "
                elif "user is not a member of this chat" in str(cf) and not str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "a non-member "
                else:
                    cf = str(cf).split('-')[0]
                    await m.edit(str(cf))
                    return
            if str(stat) == "ChatMemberStatus.BANNED" and str(stat) != "ChatMemberStatus.MEMBER":
                await m.edit(
                    text=f"{user} is already banned !")
            else:
                if len(str(reason)) < 1:
                    reason = None
                asyncio.create_task(dm(client, m, rtm))
                try:
                    await client.ban_chat_member(chat_id=chat_id,
                                                 user_id=user_id)
                    await m.edit(
                        text=f"""Banned {stb}{user} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
                except Exception as cb:
                    cb = str(cb).split('-')[0]
                    await m.edit(str(cb))
        else:
            await m.edit("You are trying to ban your own chat 🤨 !")


async def vsban(client, m, auser, user_id, reason):
    stb = ""
    try:
        m = m.message
        await m.delete()
    except:
        pass
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
        rtm = rm['rtm']
    else:
        mid = m.id
        rtm = m.reply_to_message.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await client.send_message(chat_id=chat_id, text="Banning an admin !?")
    else:
        if str(user_id).startswith('-1'):
            pu = await client.get_chat(user_id)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = (await client.get_chat_member(chat_id, user_id)).status
            except Exception as cf:
                if "user is not a member of this chat" in str(cf) and str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "channel "
                elif "user is not a member of this chat" in str(cf) and not str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "a non-member "
                else:
                    cf = str(cf).split('-')[0]
                    await client.send_message(chat_id=chat_id, text=str(cf))
                    return
            if str(stat) == "ChatMemberStatus.BANNED" and str(stat) != "ChatMemberStatus.MEMBER":
                await client.send_message(chat_id=chat_id,
                                          text=f"{user} is already banned !")
            else:
                if len(str(reason)) < 1:
                    reason = None
                asyncio.create_task(dm(client, m, rtm))
                try:
                    await client.ban_chat_member(chat_id=chat_id,
                                                 user_id=user_id)
                    await client.send_message(chat_id=chat_id, text=f"""Banned {stb}{user} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
                except Exception as cb:
                    cb = str(cb).split('-')[0]
                    await client.send_message(chat_id=chat_id, text=str(cb))
        else:
            await client.send_message(chat_id=chat_id, text="You are trying to ban your own chat 🤨 !")


async def vkick(client, m, auser, user_id, reason):
    stb = ""
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to Kick ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Kicking an admin !?")
    else:
        if str(user_id).startswith('-1'):
            pu = await client.get_chat(user_id)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = (await client.get_chat_member(chat_id, user_id)).status
            except Exception as cf:
                if "user is not a member of this chat" in str(cf) and str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "channel "
                elif "user is not a member of this chat" in str(cf) and not str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "a non-member "
                else:
                    cf = str(cf).split('-')[0]
                    await m.edit(str(cf))
                    return
            if str(stat) != "ChatMemberStatus.MEMBER" and str(stat) != "ChatMemberStatus.RESTRICTED":
                await m.edit(
                    text=f"{user} is not a member of this chat !")
            else:
                if len(str(reason)) < 1:
                    reason = None
                try:
                    await client.ban_chat_member(chat_id=chat_id,
                                                 user_id=user_id, until_date= datetime.now() + timedelta(seconds=35))
                    await m.edit(
                        text=f"""Kicked {stb}{user} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
                except Exception as cb:
                    cb = str(cb).split('-')[0]
                    await m.edit(str(cb))
                finally:
                    await client.unban_chat_member(chat_id=chat_id,
                                                   user_id=user_id)
        else:
            await m.edit("You are trying to kick your own chat 🤨 !")


async def vdkick(client, mes, auser, user_id, reason):
    stb = ""
    try:
        m = mes.message
    except:
        m = await mes.reply_text("`Trying to Kick ...`")
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
        rtm = rm['rtm']
    else:
        mid = m.id
        rtm = mes.reply_to_message.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await m.edit(text="Banning an admin !?")
    else:
        if str(user_id).startswith('-1'):
            pu = await client.get_chat(user_id)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = (await client.get_chat_member(chat_id, user_id)).status
            except Exception as cf:
                if "user is not a member of this chat" in str(cf) and str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "channel "
                elif "user is not a member of this chat" in str(cf) and not str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "a non-member "
                else:
                    cf = str(cf).split('-')[0]
                    await m.edit(str(cf))
                    return
            if str(stat) != "ChatMemberStatus.MEMBER" and str(stat) != "ChatMemberStatus.RESTRICTED":
                await m.edit(
                    text=f"{user} is not a member of this chat !")
            else:
                if len(str(reason)) < 1:
                    reason = None
                asyncio.create_task(dm(client, m, rtm))
                try:
    
                    await client.ban_chat_member(chat_id=chat_id,
                                                 user_id=user_id, until_date= datetime.now() + timedelta(seconds=35))             
                    await m.edit(
                        text=f"""Kicked {stb}{user} !\n<b>Reason:</b> {reason}""", disable_web_page_preview=True)
                except Exception as cb:
                    cb = str(cb).split('-')[0]
                    await m.edit(str(cb))
                finally:
                    await client.unban_chat_member(chat_id=chat_id,
                                                   user_id=user_id)
        else:
            await m.edit("You are trying to kick your own chat 🤨 !")


async def vskick(client, m, auser, user_id, reason):
    stb = ""
    try:
        m = m.message
        await m.delete()
    except:
        pass
    chat_id = m.chat.id
    rm = rdb.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
        rtm = rm['rtm']
    else:
        mid = m.id
        rtm = m.reply_to_message.id
    if await is_admin(client, m, chat_id, user_id) is True:
        await client.send_message(chat_id=chat_id, text="Kicking an admin !?")
    else:
        if str(user_id).startswith('-1'):
            pu = await client.get_chat(user_id)
            pus = pu.username
            if not pus:
                user = pu.title
            else:
                user = f"@{pu.username}"
        else:
            try:
                userw = (await client.get_chat(user_id))
                user = await mention_html(userw.id, userw.first_name)
            except:
                user = await mention_html(user_id, "user")
        if await immutable(client, m, chat_id, user_id) is not True:
            try:
                stat = (await client.get_chat_member(chat_id, user_id)).status
            except Exception as cf:
                if "user is not a member of this chat" in str(cf) and str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "channel "
                elif "user is not a member of this chat" in str(cf) and not str(user_id).startswith('-1'):
                    stat = "preban"
                    stb = "a non-member "
                else:
                    cf = str(cf).split('-')[0]
                    await client.send_message(chat_id=chat_id, text=str(cf))
                    return
            if str(stat) != "ChatMemberStatus.MEMBER" and str(stat) != "ChatMemberStatus.RESTRICTED":
                await m.edit(
                    text=f"{user} is not a member of this chat !")
            else:
                if len(str(reason)) < 1:
                    reason = None
                asyncio.create_task(dm(client, m, rtm))
                try:
                    await client.ban_chat_member(chat_id=chat_id,
                                                 user_id=user_id, until_date= datetime.now() + timedelta(seconds=35))                            
                except Exception as cb:
                    cb = str(cb).split('-')[0]
                    await client.send_message(chat_id=chat_id, text=str(cb))
                finally:
                    await client.unban_chat_member(chat_id=chat_id,
                                                   user_id=user_id)
        else:
            await client.send_message(chat_id=chat_id, text="You are trying to kick your own chat 🤨 !")
