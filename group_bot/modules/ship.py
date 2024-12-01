from pyrogram import Client, filters
from config import *
from group_bot import bot, mention_html_sync
from group_bot.modules.give_id import return_id
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
import json
import random
import datetime
import time

uti = time.time()

couples = {}


async def shipp(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if not await is_admin(client, m, m.chat.id, user_id):
        return
    if couples.get(chat_id):
        maintime= await give_time() 
        mainstr = f"{couples.get(chat_id)} {maintime}"
        await m.reply_text(mainstr)
        return
    with open(f"db/infos.txt", 'r') as fi:
            users = json.load(fi)
    userslist = list(users["chats"][str(chat_id)])
    st_user = random.choice(userslist)
    user1 = mention_html_sync(st_user, users["chats"][str(chat_id)][str(st_user)]["fname"])
    userslist.remove(st_user)
    nd_user = random.choice(userslist)
    if len(str(users["chats"][str(chat_id)][str(nd_user)]["fname"])) < 1:
         nd_user = random.choice(userslist)
    user2 = mention_html_sync(nd_user, users["chats"][str(chat_id)][str(nd_user)]["fname"])   
    
    maintime = await give_time()
    couple_choosen = f"""
New couple of the day:
{user1} + {user2} = ❤️

New couple of the day may be chosen in """   
    await m.reply_text(f"{couple_choosen} {maintime}")
    couples.update({chat_id: couple_choosen})



async def give_time():
    ctimee = 86400 - (time.time() - uti)
    intime = str(datetime.timedelta(seconds = ctimee))
    atime = str(intime)[: -str(intime).rfind('.')]
    ptime = str(atime).split(":")
    maintime = f"{ptime[0]} hour {ptime[1]} minutes {ptime[2]} seconds"    
    
    return maintime
