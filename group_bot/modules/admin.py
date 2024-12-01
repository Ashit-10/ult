import json
from pyrogram import *
from pyrogram.types import *
from group_bot import bot
from config import my_bot_id
from group_bot.modules.admin_check import is_admin, can_delete, can_restrict, can_promote, can_edit, can_pin
from group_bot.modules.give_id import return_id
import asyncio
from config import *

reason_db = {}


async def promote(client, m):
    verify_sender = None
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["promote_demote"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
        verify_sender = True
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        if " " in m.text or m.reply_to_message:
            user_id = None
            statv = await return_id(client, m)
            userid = statv[0]
            custom_title = statv[1]
            if not userid or len(str(userid)) < 3: 
                await m.reply_text(
                    "seems like you're not referring to any user !", quote=True)
                return
            if verify_sender:
                vbtn = await m.reply_text(text="It looks like you're anonymous, Tap this button to confirm your identity !", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=f"verify admin", callback_data=f"verifyadmin_promote_{userid}")]]))
                reason_db.update({f"{m.chat.id}_{vbtn.id}": {
                                 "id": m.id, "reason": custom_title}})
            else:
                asyncio.create_task(
                    vpromote(client, m, m.from_user.id, userid, custom_title))
        else:
            await m.reply_text(
                "seems like you're not referring to any user !", quote=True)


async def vpromote(client, m, auser_id, user_id, ct):
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to promote ..")
    chat_id = m.chat.id
    rm = reason_db.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
        reason = rm['reason']
    else:
        mid = m.id
        reason = ct
    if await can_promote(client, m, m.chat.id, auser_id) is True:
        bot_member = my_bot_id
        try:
            statsz = await client.get_chat_member(
                m.chat.id, user_id)
            stat = str(statsz.status)
        except Exception as fg:
            await m.edit(str(fg))
            return
        if stat == "ChatMemberStatus.OWNER":
            await m.edit(
                "promoting The chat Owner ? so funny !")
        elif stat == "ChatMemberStatus.ADMINISTRATOR":
            await m.edit(
                "Promoting a admin ?")
        elif stat == "ChatMemberStatus.LEFT":
            await m.edit(
                "Promoting a outsider bitch?")
        elif user_id == my_bot_id:
            await m.edit("Bitch, you really wanna do that ?")    
        else:
            try:
                bot = await client.get_chat_member(m.chat.id, my_bot_id)
                await client.promote_chat_member(
                    chat_id=m.chat.id,
                    user_id=user_id,
                    can_change_info=bot.can_change_info,
                    can_invite_users=bot.can_invite_users,
                    can_delete_messages=bot.can_delete_messages,
                    can_restrict_members=bot.can_restrict_members,
                    can_pin_messages=bot.can_pin_messages,
                    can_promote_members=False,
                    can_manage_chat=bot.can_manage_chat,
                    can_manage_voice_chats=bot.can_manage_voice_chats,
                )
                try:
                    reason_db.pop(f"{m.chat.id}_{m.id}")
                except:
                    pass
                await m.edit(text="Promoted !")
                try:
                    await client.set_administrator_title(
                        chat_id=m.chat.id, user_id=user_id, title=reason)
                except Exception as rt:
                    print(rt)
            except Exception as cp:
                if "channels.EditAdmin" in str(cp):
                    await m.edit("I haven't got sufficient permissions to promote members [CAN_ADD_ADMINS] !")
                else:
                    await m.edit(str(cp))
    else:
        await m.edit(
            'you dont have permission to promote members !')


async def demote(client, m):
    chat_id = m.chat.id
    verify_sender = None
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["promote_demote"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
        verify_sender = True
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        if " " in m.text or m.reply_to_message:
            user_id = None
            statv = await return_id(client, m)
            userid = statv[0]
            if not userid or len(str(userid)) < 3:
                await m.reply_text(
                    "seems like you're not referring to any user !", quote=True)
                return
            if verify_sender:
                vbtn = await m.reply_text(text="It looks like you're anonymous, Tap this button to confirm your identity !", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=f"verify admin", callback_data=f"verifyadmin_demote_{userid}")]]))
            else:
                asyncio.create_task(vdemote(client, m, m.from_user.id, userid))
        else:
            await m.reply_text(
                "seems like you're not referring to any user !")


async def vdemote(client, m, auser_id, user_id):
    try:
        m = m.message
    except:
        m = await m.reply_text("`Trying to demote ..")
    chat_id = m.chat.id
    rm = reason_db.get(f"{m.chat.id}_{m.id}")
    if rm:
        mid = rm['id']
    else:
        mid = m.id

    if await can_promote(client, m, m.chat.id, auser_id) is True:
        bot_member = my_bot_id
        try:
            statsz = await client.get_chat_member(
                m.chat.id, user_id)
            stat = str(statsz.status)
            if statsz.user.is_bot:
                await m.edit("Due to Telegram restrictions I can't demote bots, demote them manually !")
                return
        except Exception as fg:
            fg = str(fg).split('-')[0]
            await m.edit(str(fg))
            return
        if stat == "ChatMemberStatus.OWNER":
            await m.edit(
                "Demoting The chat Owner ? so funny !")
        elif stat == "ChatMemberStatus.MEMBER":
            await m.edit(
                "Was he a admin before ?")
        elif stat == "ChatMemberStatus.LEFT":
            await m.edit(
                "Demoting a outsider ?")
        else:
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
                await m.edit('demoted !')
            except Exception as p:
                if "400 CHAT_ADMIN_REQUIRED" in str(p):
                    await m.edit(
                        "He was promoted by someone else, demote him manually !")
                else:
                    p = str(p).split('-')[0]
                    await m.edit(str(p))
    else:
        await m.edit(
            'you dont have permission to demote members !')
