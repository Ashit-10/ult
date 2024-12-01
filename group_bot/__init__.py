import os
import sys
import logging
import json

async def ran(o, t):
   return list(range(int(o), int(t)))

#from group_bot.modules.runner import afkdb    
import logging
#logging.basicConfig(level=logging.DEBUG)
afkdb = {}
import requests

    
import time    




from pyrogram import Client, filters

from config import *
import asyncio
import html

async def mention_html(id, nam):
  name = html.escape(nam)
  mention = f"""<a href="tg://user?id={id}">{name}</a>"""
  return mention

import psycopg2

db = {} #psycopg2.connect("postgres://kvsdcasu:hnK9n_WjIhOtvngYHLIKKb-NaABCjOwY@jelani.db.elephantsql.com/kvsdcasu")
sql = {} # db.cursor()


bot_token = TELEGRAM_TOKEN # "2029656180:AAHMJeb7Mwz-0ROTqQhu2ZEKWjv3Nm-FCGA"
api_id = '6810439'
api_hash = '66ac3b67cce1771ce129819a42efe02e'

plugins = dict(
root="group_bot/modules/helpers"
)

# pyrogram client setup
bot = Client(
    'pyro-test-bot_ult',
    bot_token=bot_token,
    api_id= 2613713,
    api_hash="f615f10d7410ce9ba757f211cf1fb84b"
 #   plugins=plugins
)


bot2 = Client(
    'fban_shits_def',
    api_id=2613713,
    api_hash="f615f10d7410ce9ba757f211cf1fb84b"
)



def mention_html_sync(id, nam):
  name = html.escape(nam)
  mention = f"""<a href="tg://user?id={id}">{name}</a>"""
  return mention

OWNER = 1602293216

def mention_html_sync(id, name):
  mention = f"""<a href="tg://user?id={id}">{name}</a>"""
  return mention

def on_welcome_raw(chat_id, uid, fname, lname, uname):
    ct = time.time()
    time.sleep(10)
    with open("db/infos.txt", "r") as red:
        hh = json.load(red)
    id = uid
    username = uname
    if not username:
        username = ""
    fname = fname
    if not fname:
        fname = ""
    lname = lname
    if not lname:
        lname = ""
    cobj = {f"{id}": {
        "id": f"{id}",
        "username": f"{username}",
        "fname": fname,
        "lname": lname
    }}
    try:
       hh["chats"][str(chat_id)].update(cobj)
    except KeyError:
       return
    with open("db/infos.txt", "w+") as rit:
        json.dump(hh, rit, indent=6, sort_keys=True)
    tt = time.time() - ct
#    print(f"Added new user to infos in {tt:.5f} sec .")


@bot.on_message(filters.command('sync') & filters.user(OWNER))
def syncInfos(client, m, *args):
    chat_id = []    
    if not os.path.isfile("db/infos.txt"):
       creObj = {"chats": {}}
       with open("db/infos.txt", "w+") as cre:
          json.dump(creObj, cre, indent=6, sort_keys=True)
    if args:
        with open("db/infos.txt", "r") as red:
            hh = json.load(red)
            for i in hh["chats"]:
                chat_id.append(i)
    else:
    #    jst = m.reply_text("Processing ...")
        chat_id.append(m.chat.id)
        with open("db/infos.txt", 'r') as red:
            hh = json.load(red)
    ct = time.time()       
    fullChat = {}
    for u in chat_id:
        if str(u)[1:].isdigit():        
            allmems = {}
            for member in bot.iter_chat_members(int(u)):
                id = member.user.id
                username = member.user.username
                if not username:
                    username = ""
                fname = member.user.first_name
                if not fname:
                    fname = ""
                lname = member.user.last_name
                if not lname:
                    lname = ""
                cobj = {f"{id}": {
                        "id": f"{id}",
                        "username": f"{username}",
                        "fname": f"{fname}",
                        "lname": f"{lname}"
                        }}
                allmems.update(cobj)       
            fullChat.update({str(u): allmems})
    hh["chats"].update(fullChat)        
    with open("db/infos.txt", 'w+') as rit:
        json.dump(hh, rit, indent=6, sort_keys=True)
    ttt = time.time() - ct
    print(f"Synchronised {chat_id} in {ttt:.5f} sec")
    try:
        jst.edit(f"Synchronised in {ttt:.5f} sec.")
    except:
        pass
    
def storeChats(FullInfo):
   cchats = []
   ct = time.time()
   uid = FullInfo.user_id
   fname = FullInfo.first_name
   lname = FullInfo.last_name
   uname = FullInfo.username
   if not fname:
     fname = ""
   if not lname:
      lname = ""
   if not uname:
      uname = "(No Username)"
   else:
      uname = f"@{uname}"
   fullname = str(fname) + " " + str(lname)
   with open("db/infos.txt", 'r') as red:
      info = json.load(red)
   for chat in info["chats"]:   
     if str(chat)[1:].isdigit():
      try:
         infos = info["chats"][str(chat)][str(uid)]
         cchats.append(chat)
      except KeyError as key:
         pass
   if len(cchats) > 0:
      olduname = f"@{infos['username']}"
      if len(olduname) < 4:
          olduname = "(No Username)"
      if olduname.startswith("@@"):
          olduname = olduname[1:]
      user = mention_html_sync(uid, fullname)
      if olduname != uname:
            fstr = "{} (`{}`) changed username from {} to {} .".format(user, uid, olduname, uname)
            for c in cchats:
                try:
                    with open(f"db/X{c}_db.txt", 'r') as f:
                        obj = json.load(f)
                    if obj[f"{bot_id}"]["enable_disable"]["sg"] is True:           
                         bot.send_message(chat_id=c, text=fstr)
                except Exception as e:
                    print(e)        
            SyncOne(info, uid, fname, lname, uname)
   

def SyncOne(hh, uid, fname, lname, username):
    ct = time.time()
    chat_id = []
    cobj = {
              "id": f"{uid}",
              "username": f"{username}",
              "fname": f"{fname}",
              "lname": f"{lname}"
           }
    for i in hh["chats"]:
        chat_id.append(i)
    for u in chat_id:
        if str(u)[1:].isdigit():       
          try: 
             if hh["chats"][str(u)][str(uid)]:
                 hh["chats"][str(u)][str(uid)] = cobj                           
          except KeyError:
             pass          
          except Exception as e:
             print(e)
    with open("db/infos.txt", 'w+') as rit:
        json.dump(hh, rit, indent=6, sort_keys=True)
    ttt = time.time() - ct
 #   print(f"Updated New Info {uid} in {ttt:.5f} sec")



   

@bot.on_message(filters.command(["backup"]) & filters.user(1602293216))
def takebkup(client, m):    
    try:
       fst = m.reply_text("`Initiating process ..`")
       if ' ' in m.text:
            security_push(m, fst)
    except Exception as e:
       m.reply_text(str(e))

@bot.on_message(filters.command(["restore"]) & filters.user(1602293216))
def restore(client, m):    
    try:
       link = m.command[1]
       if "blob" in link:
          link = link.replace("blob", "raw")
       fir = m.reply_text("`Processing ...`")
       r = requests.get(str(link))
       open("db_git.zip", 'wb').write(r.content)
       try:
          m.delete()
       except:
           pass
       tnd = fir.edit("Files downloaded ..")
       os.system("mkdir -p db")
       os.system("mv -f db_git.zip db/")
       os.system("cd db && unzip -oP 91144ashit db_git.zip")
       os.system("cd db && rm db_git.zip")
       tnd.edit("All files loaded successfully !")
    except Exception as e:
       m.reply_text(str(e))
       
       

async def redb():
    try:
        with open("afkdb.txt", "w+") as deb:
            json.dump(afkdb, deb, indent=4)
    except Exception as e:
         print(e)
         pass

def redbs():
    try:
        with open("afkdb.txt", "w+") as deb:
            json.dump(afkdb, deb, indent=4)
    except Exception as e:
         print(e)
         pass    
from os import environ, execle, path, remove

@bot.on_message(filters.command(["restart"]))
async def restart(client, message):
    if message.sender_chat:
        user_id = message.sender_chat.id
    else:
        user_id = message.from_user.id
    if int(user_id) == 1602293216:
      ht = await message.reply_text(f"`ʀᴇsᴛᴀʀᴛɪɴɢ 🔁`")
      mid = ht.id
      chat_id = message.chat.id
      with open("re.txt", "w+") as rd:
        rd.write(f"{chat_id}_{mid}")
      await redb()
      args = [sys.executable, "-m", "group_bot"]
      execle(sys.executable, *args, environ)  
      exit()
      return


import github
import datetime
import base64
from github import Github
from github import InputGitTreeElement

def gitpush(m: str = 'Updated !', repo_token: str = "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", branch: str = "main"):
    
   # return
    ct = time.time()
    now = datetime.datetime.now(tz)
    nowfile = str(now).replace(' ', '_')
    os.system(f"cd db && zip -rP 91144ashit json.db_{nowfile}_{bot_username}.zip *")
    gh = github.Github(repo_token)
    repository = "Hrushikesh69/backup_db"
    elements = []
    remote_repo = gh.get_repo(repository)
    file = f"json.db_{nowfile}_{bot_username}.zip"
    file_to_update = f"db/{file}"
    print(file)
    data = base64.b64encode(open(file_to_update, "rb").read())
    blob = remote_repo.create_git_blob(data.decode("utf-8"), "base64")
    element = github.InputGitTreeElement(
        path=file_to_update, mode='100644', type='blob', sha=blob.sha)
    elements.append(element)
    try:
       commit_message = m.text.split(' ',1)[1]
    except:
        commit_message = f'Updated files at {now}'

    branch_sha = remote_repo.get_branch(branch).commit.sha

    base_tree = remote_repo.get_git_tree(sha=branch_sha)

    tree = remote_repo.create_git_tree(elements, base_tree)

    parent = remote_repo.get_git_commit(sha=branch_sha)

    commit = remote_repo.create_git_commit(commit_message, tree, [parent])

    branch_refs = remote_repo.get_git_ref(f'heads/{branch}')

    branch_refs.edit(sha=commit.sha)
    print(time.time() - ct)
    try:
        os.remove(f"db/{file}")
    except:
        pass

def secure_me():
    det = datetime.datetime.now(tz)+timedelta(hours=24)
    sj.add_job(security_push, "date", run_date=det)
    if os.path.isfile("afkdb.txt"):
        with open("afkdb.txt", "r") as res:
           afkdb1 = json.load(res)
        print(afkdb1)
        afkdb.update(afkdb1)
    print("update has been scheduled !")

def security_push(m: str = 'Updated !', *args):
    print("Starting process...")
    gitpush(m)
    redbs()
    try:
       if args:
          fmt = args[0]
          fmt.edit("Succesfully backed up all files !")
    except Exception as ed:
        print(ed)
    args = [sys.executable, "-m", "group_bot"]
    execle(sys.executable, *args, environ)  
    exit()
    return



from group_bot.modules.help import helpp


from group_bot.modules.runner import *

from group_bot.modules.callback import m_buttons
from group_bot.modules.inline import ianswer

    
    
@bot.on_raw_update()
def _raw(client, m, users, chats):
   NewUp = type(m).__name__
   if NewUp == "UpdateUserName":   
      storeChats(m)
    
        
