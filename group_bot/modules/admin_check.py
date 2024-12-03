from group_bot import bot
from pyrogram import *
from pyrogram.types import *
import time
import json
import os
import asyncio
from config import log_chat
immune = {}
admins = {}
admin_perms = {}


async def admins_coll(client, m):
    if not m.sender_chat:
        if m.from_user.id in admins:
            await admins_col(client, m, m.chat.id)
            await m.reply_text("Refreshed admin cache !")


async def immutable_col(client, m, chat_id: int):
    chat_imm = admins.get(int(chat_id))
    if not chat_imm:
       await admins_col(client, m, chat_id)
       chat_imm = admins.get(int(chat_id))
    try:
        my_ch = (await client.get_chat(chat_id)).linked_chat.id
        chat_imm.append(my_ch)
    except:
        pass
    finally:
        immune.update({int(chat_id): chat_imm})


async def immutable(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    my_chat_imm = immune.get(chat_id)
    if not my_chat_imm:
        await immutable_col(client, m, chat_id)
        my_chat_imm = immune.get(chat_id)
    if user_id in my_chat_imm:
        return True
    else:
        return False

# del cmd


async def admins_col(client, msg, chat_id):
    chat_admins = []
    perms = {}
    try:
        all_admins = []
        async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            all_admins.append(m)
    except Exception as e:
        print(e)
        await bot.send_message(log_chat, f"admin_check.py, line 55, {e}")
        return
    for a in all_admins:
        chat_admins.append(a.user.id)
        perms.update({a.user.id: {
            "is_anonymous": a.privileges.is_anonymous,
            "can_delete_messages": a.privileges.can_delete_messages,
            "can_restrict_members": a.privileges.can_restrict_members,
            "can_promote_members": a.privileges.can_promote_members,
            "can_change_info": a.privileges.can_change_info,
            "can_pin_messages": a.privileges.can_pin_messages,
            "can_manage_voice_chats": a.privileges.can_manage_video_chats,
            "can_invite_users": a.privileges.can_invite_users,
            "can_manage_chat": a.privileges.can_manage_chat

        }
        })
    chat_admins.append(int(chat_id))
    admin_perms.update({int(chat_id): perms})
    admins.update({int(chat_id): chat_admins})
    chat_link = ""
    # try:
    #     chat_link = bot.get_chat_invite_link(chat_id)
    # except Exception as e:
    #     print(e)
    print(f"Admin list updated for async list.  {chat_id} {msg.chat.title}  {chat_link}")
    asyncio.create_task(immutable_col(client, m, chat_id))


async def is_admin(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    my_chat_admins = admins.get(chat_id)
    if not my_chat_admins:
        await admins_col(client, m, chat_id)
    my_chat_admins = admins.get(chat_id)
    if user_id in my_chat_admins:
        return True
    else:
        return False

# non async

def admins_col_sync(client, m, chat_id):
    chat_admins = []
    perms = {}
    try:
        all_admins = []
        for m in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            all_admins.append(m)
    except Exception as e:
        client.send_message(log_chat, f"admin-check.py line 104, {e}")
        return
    for a in all_admins:
        chat_admins.append(a.user.id)
        perms.update({a.user.id: {
            "is_anonymous": a.privileges.is_anonymous,
            "can_delete_messages": a.privileges.can_delete_messages,
            "can_restrict_members": a.privileges.can_restrict_members,
            "can_promote_members": a.privileges.can_promote_members,
            "can_change_info": a.privileges.can_change_info,
            "can_pin_messages": a.privileges.can_pin_messages,
            "can_manage_voice_chats": a.privileges.can_manage_video_chats,
            "can_invite_users": a.privileges.can_invite_users,
            "can_manage_chat": a.privileges.can_manage_chat

        }
        })
    chat_admins.append(int(chat_id))
    admin_perms.update({int(chat_id): perms})
    print("Admin list updated for sync list.")

    admins.update({int(chat_id): chat_admins})
    

def is_admin_sync(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    if not admins.get(chat_id):
        admins_col_sync(client, m, chat_id)
    my_chat_admins = admins.get(chat_id)
    if user_id in my_chat_admins:
        return True
    else:
        return False


# Other permissions


async def can_pin(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    if chat_id == user_id:
        can_or_not = True
        return can_or_not
    
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]['can_pin_messages']
    except KeyError:
        can_or_not = False
        # await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_edit(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    if chat_id == user_id:
        can_or_not = True
        return can_or_not
        
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]['can_change_info']
    except KeyError:
       can_or_not = False
       # await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_restrict(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
   

    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]["can_restrict_members"]
    except KeyError:
        can_or_not = False
       # await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_delete(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    if chat_id == user_id:
        return True

    he = admin_perms.get(chat_id)
    print(user_id)
    try:
        can_or_not = he[user_id]['can_delete_messages']
    except KeyError:
       can_or_not = False
       # await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_promote(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]['can_promote_members']
    except KeyError:
       can_or_not = False
       # await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def adminlist(client, m, chat_id):
    chat_id = int(chat_id)
    my_admeme = []
    if not admins.get(chat_id):
        await admins_col(client, m, chat_id)
    my_chat_admins = admins.get(chat_id)
    for ih in my_chat_admins:
        if not str(ih).startswith('-1'):
            my_admeme.append(ih)
    return my_admeme
