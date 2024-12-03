from pyrogram import *
from config import *
from group_bot import bot, mention_html, bot2
from group_bot.modules.give_id import return_id
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
import json
import asyncio
#from convopyro import Conversation
#Conversation(bot)

qwait = {}

async def quote1(client, m):
    if m.reply_to_message:
         if " " in m.text:
              msg_ids = []
              noms = int(m.command[1])
              msgr = m.reply_to_message.id
              if noms == 0:
                   msgs = m.reply_to_message.id
                   msg_ids.append(msgs)
                   oke = await client.forward_messages(-1001617540462, m.chat.id, msg_ids)
              else:
                   for i in range(noms):
                        msg_ids.append(msgr + i)
                  # print(msg_ids)
                   oke = await client.forward_messages(-1001617540462, m.chat.id, msg_ids[0])
                   msg_ids = msg_ids[1:]
                   await client.forward_messages(-1001617540462, m.chat.id, msg_ids)
                   
              hmm = await m.reply_text("processing..")              
              qwait.update({"qote": {
                        "msg_id": m.id,
                        "chat": m.chat.id,
                        "del_id": hmm.id,
                        "q_id": oke.id,
                        "msg": m.text
                          }})
              await client.send_message(-1001617540462, text=m.text, reply_to_id=oke.id)
              await quo(client, m, oke.id, noms)
         else:
              msgr = m.reply_to_message.id              
              oke = await client.forward_messages(-1001617540462, m.chat.id, msgr)
              hmm = await m.reply_text("processing..")
              qwait.update({"qote": {
                        "msg_id": m.id,
                        "chat": m.chat.id,
                        "del_id": hmm.id,
                        "q_id": oke.id,
                        "msg": m.text
                          }})
              await client.send_message(-1001617540462, text=m.text, reply_to_id=oke.id)
              await quo(client, m, oke.id, 0)
        # client.send_message(-1001617540462, reply_to_id=oke.id, text=m.text)
         



#@bot2.on_message(filters.command('q') & filters.chat(-1001617540462) & filters.user(5214279030))


async def quo(client, m, rid, noms):
     msg_ids = []
     if noms:
        for i in range(noms):
            msg_ids.append(rid + i)
        ids = qwait.get("qote")     
     else:
          msg_ids.append(rid)
     oke = await bot2.forward_messages(-1001617540462, -1001617540462, msg_ids[0])
     msg_ids = msg_ids[1:]
     if msg_ids:
        await bot2.forward_messages(-1001617540462, -1001617540462, msg_ids)
     ids = qwait.get("qote")
     await asyncio.sleep(0.4)
     await bot2.send_message(-1001617540462, text=ids["msg"], reply_to_id=oke.id)
 #    if ids:
      #  await bot2.send_message(chat_id=-1001617540462, text=ids["msg"], reply_to_id=ids["q_id"])
       

@bot2.on_message(filters.chat(-1001617540462) & filters.user([2014342964, 1031952739]))
def quo1(client, m):
     if m.from_user.id == 2014342964:
         m.copy(-1001617540462)
  #   else:
     #    m.copy(-1001617540462)
     
@bot.on_message(filters.chat(-1001617540462) & filters.user(740538095) & ~filters.forwarded)
def quo2(client, m):
   if m.sticker:
     sid = m.sticker.file_id
     id = qwait.get("qote")
     if id:
        chat_id = id["chat"]
        msg_id = id["msg_id"]
        del_id = id["del_id"]
        try:
           client.send_sticker(int(chat_id), sticker=sid, reply_to_id=msg_id)
        finally:
           qwait.clear()
           client.delete_messages(chat_id, del_id)
     
     
     