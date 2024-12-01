import os
import json
from pyrogram import *
from pyrogram.types import *
import re
from group_bot import bot
from config import *
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
import time

# @bot.on_message(filters.command(['pinned'], ['!', '/']) & ~filters.private)
async def pinned(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["pin_unpin"] is not True:
        return
    if m.reply_to_message:
        trying = await client.send_message(text='`searching ...`', chat_id=chat_id, reply_to_id = m.reply_to_message.id)
    else:
        trying = await m.reply_text('`searching ...`')
    if m:
        try:
            chat_id = m.chat.id
            chat = m.chat
            chat_name = m.chat.title
            mes = await client.get_chat(chat_id)
            message_link = mes.pinned_message.link
            await trying.edit(
                f"The pinned message in {chat_name} [can be found here]({message_link}) .", disable_web_page_preview=True)
        except Exception as n:
            await trying.edit(f"No pinned message in {chat_name} !")


async def pin(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, chat_id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["pin_unpin"] is not True:
        return
    if not await is_admin(client, m, m.chat.id, my_bot_id):
        await m.reply_text("Make me admin to do these stuffs !")
        return
    if await can_pin(client, m, chat_id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_PIN_MESSAGES]")
        return    
    if m.reply_to_message and m.text:
        if "loud" in m.text or "l" in str(m.command[0]):
          if await can_pin(client, m, chat_id, my_bot_id):                 
            try:
                await client.pin_chat_message(chat_id=chat_id,
                                              disable_notification=False,
                                              id=m.reply_to_message.id)     
                await m.reply_text(
                    f"Pinned [this message]({m.reply_to_message.link}) and notified to all members !", disable_web_page_preview=True)                                      
            except Exception as e:
                await m.reply_text(str(e))
        elif "silent" in m.text or "s" in str(m.command[0]):
            try:
                await m.delete()
            except:
                pass
            try:
                await client.pin_chat_message(chat_id=chat_id,
                                              disable_notification=True,
                                              id=m.reply_to_message.id)
            except Exception as e:
                await m.reply_text(str(e))
   
        else:
          if await can_pin(client, m, chat_id, my_bot_id):                 
            try:
                await client.pin_chat_message(chat_id=chat_id,                                           
                                              id=m.reply_to_message.id)
                await m.reply_text(
                    f"Pinned [this message]({m.reply_to_message.link}) successfully !", disable_web_page_preview=True)                             
            except Exception as e:
                await m.reply_text(str(e))
    else:
        await m.reply_text("Reply to a message to pin !")


## service message delete
    return
    if obj[f"{bot_id}"]["on_off"]["antiservice"] is True or obj[f"{bot_id}"]["raid"]["status"] == "on":
     
        SVM = True
        k = 1
        await asyncio.sleep(2)
        while SVM:             
             mid = m.id + k
             mes = await client.get_messages(m.chat.id, mid)
             print(mes.service)
             print(mid)
             if mes.service:
                 try:
                     print("del")
                     await client.delete_messages(m.chat.id, mid)
                 except Exception as e:
                     print(e)
                 finally:
                     SVM = False
             k += 1
             if k == 20:
                 SVM = False
                 break
        

async def unpin(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, chat_id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["pin_unpin"] is not True:
        return
    if await can_pin(client, m, chat_id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_PIN_MESSAGES]")
        return
    if "all" in m.text.split(' '):
        try:
            await client.unpin_all_chat_messages(chat_id)
            await m.reply_text(
                f"`Successfully unpinned all pinned messages !`")
        except Exception as e:
            await m.reply_text(str(e))
    else:
        try:
            await client.unpin_chat_message(chat_id=m.chat.id,
                                            id=m.reply_to_message.id)
            await m.reply_text(
                f"`Successfully unpinned the message !`")
        except Exception as e:
            if str(e) == "'NoneType' object has no attribute 'id'":
                await m.reply_text("Message to unpin not found !")
            else:
                await m.reply_text(str(e))




async def botpin(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, chat_id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["pin_unpin"] is not True:
        return
    if not await is_admin(client, m, m.chat.id, my_bot_id):
        await m.reply_text("Make me admin to do these stuffs !")
        return
    if await can_pin(client, m, chat_id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_PIN_MESSAGES]")
        return    
    if m.reply_to_message and m.text:
        if await can_pin(client, m, chat_id, my_bot_id):                 
            try:
                botfwd = await m.reply_to_message.copy(chat_id)
                await client.pin_chat_message(chat_id=chat_id,
                                              disable_notification=False,
                                              id=botfwd.id)     
                await m.reply_to_message.delete()
                await m.delete()
            except Exception as e:
                await m.reply_text(str(e))
        
    else:
        await m.reply_text("Reply to a message to pin !")






