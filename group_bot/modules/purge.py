from config import *
import json
from pyrogram import *
from pyrogram.types import *
from group_bot import bot, ran
import asyncio
from group_bot.modules.admin_check import is_admin, can_delete, can_restrict, adminlist
import time

ptf = {}


async def purgeyfrom(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["purge"] is not True:
            return
        if await can_delete(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_DELETE_MESSAGES]")
            return
        if m.reply_to_message:
            msg_id = m.reply_to_message.id
            ptt = await m.reply_text("Now reply with `/purgeto` to delete all messages in between.")
            ptf.update({int(chat_id): f"{msg_id}_{ptt.id}"})
            await m.delete()
        else:
            await m.reply_text("Reply to message to delete from !")


async def purgeyto(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["purge"] is not True:
            return
        if await can_delete(client, m, m.chat.id, user_id) is not True:
            await m.reply_text("You don't have sufficient permissions; caused by [CAN_DELETE_MESSAGES]")
            return
        if m.reply_to_message:
            tom = m.reply_to_message.id
            frm = ptf.get(int(chat_id))
            if frm:
                frmm = frm.split('_')[0]
                todel = frm.split('_')[1]
                ptf.pop(int(chat_id))
                asyncio.create_task(pt(client, m, int(frmm), int(tom)))
                await m.delete()
                await client.delete_messages(chat_id=chat_id, ids=int(todel))
            else:
                await m.reply_text("First command should be `/purgefrom` !")
        else:
            await m.reply_text("Reply to message to purge to !")

async def dele(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    if await can_delete(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_DELETE_MESSAGES]")
        return
    if m.reply_to_message:
        try:
            await m.reply_to_message.delete()
        except Exception as e:
            await m.reply_text(str(e))
            return
        try:
            await m.delete()
        except Exception as e:
            await m.reply_text(str(e))
    else:
        await m.reply_text("Reply to message to delete it !")
        
async def purgey(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["purge"] is not True:
        return
    if await can_delete(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_DELETE_MESSAGES]")
        return
    if m.reply_to_message:
        asyncio.create_task(pt(client, m))
    else:
        await m.reply_text("Reply to message to purge !")


async def pt(client, m, *args):
    chat_id = m.chat.id
    tm = 0
    ty = await m.reply_text("`Purging ...`")
    frm = int(m.reply_to_message.id)
    tom = int(m.id)
    # msgids = await ran(frm, tom)
    # ml = len(msgids)
    if args:
        frm = args[0]
        tom = args[1]
    while int(frm) <= int(tom):
        try:
            justDoIt = await client.delete_messages(
                chat_id, frm)
            frm += 1
            if justDoIt:
                tm += 1
        except Exception as p:
            frm += 1
    ped = await ty.edit("Fast purged {} messages !".format(tm))
    await asyncio.sleep(3)
    await ped.delete()


async def pas(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    if " " in m.text:
        try:
            with open(f"db/X{chat_id}_db.txt", 'r') as f:
                obj = json.load(f)
            password = obj[f"{bot_id}"]["pass_words"]
            if str(m.text.split()[1]) in password:
                await m.reply_text("Already in !")
            else:
                obj[f"{bot_id}"]["pass_words"].append(
                    str(m.text.split()[1]).lower())
                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                    json.dump(obj, wf, indent=4)
                await m.reply_text(f"Successfully added `{m.text.split()[1]}` !")
        except Exception as rf:
            await m.reply_text(str(rf))
    else:
        await m.reply_text("Text not found !")


async def rm(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    if " " in m.text:
        try:
            with open(f"db/X{chat_id}_db.txt", 'r') as f:
                obj = json.load(f)
            password = obj[f"{bot_id}"]["pass_words"]
            if str(m.text.split()[1]) not in password:
                await m.reply_text("Wasn't there !")
            else:
                obj[f"{bot_id}"]["pass_words"].remove(
                    str(m.text.split()[1]).lower())
                with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                    json.dump(obj, wf, indent=4)
                await m.reply_text(f"Successfully removed `{m.text.split()[1]}` !")
        except Exception as rf:
            await m.reply_text(str(rf))
    else:
        await m.reply_text("Text not found !")


async def ping(_, m: Message):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["ping"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    start = time.time()
    replymsg = await m.reply_text("....", quote=True)
    delta_ping = time.time() - start
    await replymsg.edit_text(f"<b>Pong!</b>\n{delta_ping * 1000:.3f} ms")
    return
