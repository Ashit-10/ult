from group_bot.modules.welcome import welcome, setwelcome, resetwelcome, setgoodbye, resetgoodbye
from group_bot.modules.rules import rules, setrules
from group_bot.modules.report import reports, dreport, mreport
from group_bot.modules.purge import pas, rm, ping, purgey, purgeyfrom, purgeyto, dele
from group_bot.modules.pin_unpin import pinned, pin, unpin, botpin
from group_bot.modules.notes import addnotes, pvt_notes, delnotes
from group_bot.modules.lovk import lock, unlock, locked, locks, lock_sizes, locks_list
from group_bot.modules.filters import (filters_yo, noteslist_callback, lang_detection, verify_captcha, check_rules_cb, antipin,
                                       delfilter, addfilter, filterslist, raid_go, notes, getnotes, exp, imp)
from group_bot.modules.execute import exece, down, up
from group_bot.modules.evall import eval
from group_bot.modules.db import create_db
from group_bot.modules.enable_disable import (enable, disable, enabled, disabled, en_dis_able,
                                              antiservice, cmode)
from group_bot.modules.admin_check import is_admin, admins_col, immutable_col, immutable
from group_bot.modules.notes import group_notes, private_notes
from group_bot.modules.warnings import save_warns, warns_check, dsave_warns, ssave_warns, rmwarns, unwarn, set_warn_limit, set_warn_mode, sdsave_warns
from group_bot.modules.blocklist import (blocklist, delblocklist, addblocklist, ablocklist, addablocklist,
                                         delablocklist, roll_blocklist, callback_spam, resend_file)
from group_bot.modules.ban import mute
from group_bot.modules.nsfw import nchek
from group_bot.modules.approve import approve, disapprove
from group_bot.modules.admin import promote, demote
from group_bot.modules.antiflood import antiflood_go, flood, anticount, antimode
import datetime
from datetime import timedelta
from group_bot.modules.helpers.send import filter_helper
from group_bot.modules.give_id import users_id
from group_bot.modules.afky import afk, menafk
from group_bot import bot, mention_html, syncInfos, on_welcome_raw
from pyrogram import *
from pyrogram.types import *
import asyncio
import time
import os
import random
from group_bot.modules.admin_check import admins_coll
from group_bot.modules.fbans import fban1, unfban1
from group_bot.modules.whois import info
from group_bot.modules.helpers.welcome_sender import welcome_sender, sj
from config import *
import json
import pytz
from group_bot.modules.nof import noformat
from group_bot.modules.quote import quote1
from group_bot.modules.translate import trt, langs
import csv
from group_bot.modules.ship import shipp
from langdetect import detect, DetectorFactory
from group_bot.modules.fbans import fed_admins, ben, send_log
DetectorFactory.seed = 0
tz = pytz.timezone("Asia/kolkata")

OWNER = 1602293216

ch = ['!', '/']

bcmds = ['ban', 'dban', 'sban', 'tban',
         'unban', 
         'mute', 'unmute', 'dmute', 'smute', 'tmute',
         'kick', 'dkick', 'skick'
]


# set slow mode
#

@bot.on_message(filters.command(['ship', 'shipping'], ['!', '/']))
async def filter_shipp(client, m):
    asyncio.create_task(shipp(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['tr', 'translate'], ['!', '/']))
def filter_trt(client, m):
    trt(client, m)
    
@bot.on_message(filters.command(['q']) &~filters.chat(-1001617540462))
async def filter_q(client, m):
    asyncio.create_task(quote1(client, m))
    asyncio.create_task(filters_go(client, m))
    
@bot.on_message(filters.command(['getlangs'], ['!', '/']))
def filter_langs(client, m):
    langs(client, m)
    
            
@bot.on_message(filters.command('export'))
async def filter_exp(client, m):
    asyncio.create_task(exp(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command('import'))
async def filter_imp(client, m):
    asyncio.create_task(imp(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['exec']) & filters.private & filters.user(OWNER))
async def filter_exec(client, m):
    asyncio.create_task(exece(client, m))
   # asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['down']) & filters.private & filters.user(OWNER))
async def filter_down(client, m):
    asyncio.create_task(down(client, m))
   # asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['up']) & filters.private & filters.user(OWNER))
async def filter_up(client, m):
    asyncio.create_task(up(client, m))
  #  asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command("eval") & filters.user(1602293216))
async def filter_eval(client, m):
    asyncio.create_task(eval(client, m))
  #  asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['notes', 'saved'], ['!', '/']))
async def filter_notes(client, m):
    asyncio.create_task(notes(client, m))
    asyncio.create_task(filters_go(client, m))

@bot.on_message(filters.command(['get'], ['!', '/']))
async def filter_notes(client, m):
    asyncio.create_task(getnotes(client, m))
    asyncio.create_task(filters_go(client, m))
    
@bot.on_message(filters.command(['fban'], ['/', '!']))
async def filter_fban(client, m):
    asyncio.create_task(fban1(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['unfban'], ['/', '!']))
async def filter_unfbab(client, m):
    asyncio.create_task(unfban1(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['del'], ['/', '!']))
async def filter_del(client, m):
    asyncio.create_task(dele(client, m))
    asyncio.create_task(filters_go(client, m))

@bot.on_message(filters.command(['admincache'], ['!', '/']))
async def filter_col(client, m):
    asyncio.create_task(admins_coll(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['nof', 'noformat'], ['!', '/']))
async def filter_nof(client, m):
    asyncio.create_task(noformat(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['purgeto'], ['/', '!']))
async def filter_purgeyto(client, m):
    asyncio.create_task(purgeyto(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['purgefrom'], ['!', '/']))
async def filter_purgeyfrom(client, m):
    asyncio.create_task(purgeyfrom(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['info'], ['/', '!']))
async def filter_info(client, m):
    asyncio.create_task(info(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['filter'], ['/', '!']))
async def filter_addfilter(client, m):
    asyncio.create_task(addfilter(client, m))
 #   asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['stop'], ['!', '/']))
async def filter_dfilter(client, m):
    asyncio.create_task(delfilter(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['filters'], ['!', '/']))
async def filter_filterslist(client, m):
    asyncio.create_task(filterslist(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['raid'], ['!', '/']))
async def filter_raid_go(client, m):
    asyncio.create_task(raid_go(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['setwelcome'], ['!', '/']))
async def filter_setwelcome(client, m):
    asyncio.create_task(setwelcome(client, m))
    asyncio.create_task(filters_go(client, m))

@bot.on_message(filters.command(['set2ndwelcome'], ['!', '/']))
async def filter_2ndsetwelcome(client, m):
    asyncio.create_task(setwelcome(client, m, "yeh he boi"))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['ping'], ['!', '/']))
async def filter_ping(client, m):
    asyncio.create_task(ping(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['setgoodbye'], ['!', '/']))
async def filter_setgoodbye(client, m):
    asyncio.create_task(setgoodbye(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['welcome'], ['!', '/']))
async def filter_welcome(client, m):
    asyncio.create_task(welcome(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['resetwelcome'], ['!', '/']))
async def filter_resetwelcome(client, m):
    asyncio.create_task(resetwelcome(client, m))
    asyncio.create_task(filters_go(client, m))

@bot.on_message(filters.command(['reset2ndwelcome'], ['!', '/']))
async def filter_reset2ndwelcome(client, m):
    asyncio.create_task(resetwelcome(client, m, "yeh he boi"))
    asyncio.create_task(filters_go(client, m))
    
    
@bot.on_message(filters.command(['resetgoodbye'], ['!', '/']))
async def filter_resetgoodbye(client, m):
    asyncio.create_task(resetgoodbye(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['warns'], ['!', '/']))
async def filter_warns_check(client, m):
    asyncio.create_task(warns_check(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['warn'], ['!', '/']))
async def filter_save_warns(client, m):
    asyncio.create_task(save_warns(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['dswarn', 'sdwarn'], ['!', '/']))
async def filter_save_warns(client, m):
    asyncio.create_task(save_warns(client, m))
    asyncio.create_task(filters_go(client, m))
    
    
@bot.on_message(filters.command(['dwarn'], ['!', '/']))
async def filter_dsave_warns(client, m):
    asyncio.create_task(dsave_warns(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['swarn'], ['!', '/']))
async def filter_ssave_warns(client, m):
    asyncio.create_task(ssave_warns(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['rmwarns'], ['!', '/']))
async def filter_rmwarns(client, m):
    asyncio.create_task(rmwarns(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['unwarn'], ['!', '/']))
async def filter_unwarn(client, m):
    asyncio.create_task(unwarn(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['setwarnlimit'], ['!', '/']))
async def filter_set_warn_limit(client, m):
    asyncio.create_task(set_warn_limit(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['setwarnmode'], ['!', '/']))
async def filter_set_warn_mode(client, m):
    asyncio.create_task(set_warn_mode(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['rules'], ['!', '/']))
async def filter_rules(client, m):
    asyncio.create_task(rules(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['setrules'], ['!', '/']))
async def filter_setrules(client, m):
    asyncio.create_task(setrules(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['report'], ['!', '/']))
async def filter_reports(client, m):
    asyncio.create_task(reports(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['dont_mention_me'], ['!', '/']))
async def filter_dreport(client, m):
    asyncio.create_task(dreport(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['mention_me'], ['!', '/']))
async def filter_mreport(client, m):
    asyncio.create_task(mreport(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['purge'], ['/', '!']))
async def filter_purge(client, m):
    asyncio.create_task(purgey(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['pass'], ['/', '!']))
async def filter_pass(client, m):
    asyncio.create_task(pas(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['rm'], ['/', '!']))
async def filter_rm(client, m):
    asyncio.create_task(rm(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['pinned'], ['!', '/']))
async def filter_pinned(client, m):
    asyncio.create_task(pinned(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['unpin'], ['!', '/']))
async def filter_unpin(client, m):
    asyncio.create_task(unpin(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['pin', 'spin', 'lpin'], ['!', '/']))
async def filter_pin(client, m):
    asyncio.create_task(pin(client, m))
    asyncio.create_task(filters_go(client, m))

@bot.on_message(filters.command(['botpin'], ['!', '/']))
async def filter_pin(client, m):
    asyncio.create_task(botpin(client, m))
    asyncio.create_task(filters_go(client, m))

@bot.on_message(filters.command(['save'], ['/', '!']))
async def filter_adddn(client, m):
    asyncio.create_task(addnotes(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['private_notes'], ['!', '/']))
async def filter_pvtn(client, m):
    asyncio.create_task(pvt_notes(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['clear'], ['!', '/']))
async def filter_delnotes(client, m):
    asyncio.create_task(delnotes(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['lock'], ['/', '!']))
async def filter_lock(client, m):
    asyncio.create_task(lock(client, m))
    asyncio.create_task(filters_go(client, m))

@bot.on_message(filters.command(['locks'], ['/', '!']))
async def filter_lock(client, m):
    await m.reply_text(locks_list)
    asyncio.create_task(filters_go(client, m))
    
@bot.on_message(filters.command(['setlocksize'], ['!', '/']))
async def filter_lock_sizes(client, m):
    asyncio.create_task(lock_sizes(client, m))
    asyncio.create_task(filters_go(client, m))
    
    
@bot.on_message(filters.command(['unlock'], ['/', '!']))
async def filter_unlock(client, m):
    asyncio.create_task(unlock(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['locked'], ['/', '!']))
async def filter_locked(client, m):
    asyncio.create_task(locked(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['id'], ['/', '!']))
async def filter_uid(client, m):
    asyncio.create_task(users_id(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['promote'], ['!', '/']))
async def filter_promote(client, m):
    asyncio.create_task(promote(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['demote'], ['!', '/']))
async def filter_demote(client, m):
    asyncio.create_task(demote(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['afk'], ['!', '/']))
async def filter_afk(client, m):
    asyncio.create_task(afk(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['flood', 'antiflood'], ['/', '!']))
async def filter_flood(client, m):
    asyncio.create_task(flood(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['setflood', 'floodcount'], ['/', '!']))
async def filter_floodcount(client, m):
    asyncio.create_task(anticount(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['setfloodmode', 'floodmode'], ['/', '!']))
async def filter_floodmode(client, m):
    asyncio.create_task(antimode(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['approve'], ['!', '/']))
async def filter_a(client, m):
    asyncio.create_task(approve(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['disapprove'], ['!', '/']))
async def filter_disa(client, m):
    asyncio.create_task(disapprove(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(bcmds, ['!', '/']))
async def filter_disa(client, m):
    asyncio.create_task(mute(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['blocklist', 'blacklist'], ['!', '/']))
async def filter_blocklist(client, m):
    asyncio.create_task(blocklist(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['rmblocklist', 'rmblacklist'], ['!', '/']))
async def filter_delblocklist(client, m):
    asyncio.create_task(delblocklist(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['addblocklist', 'addblacklist'], ['!', '/']))
async def filter_addblocklist(client, m):
    asyncio.create_task(addblocklist(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['ablocklist', 'ablacklist'], ['!', '/']))
async def filter_ablocklist(client, m):
    asyncio.create_task(ablocklist(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['rmablocklist', 'rmablacklist'], ['!', '/']))
async def filter_delablocklist(client, m):
    asyncio.create_task(delablocklist(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['addablocklist', 'addablacklist'], ['!', '/']))
async def filter_addablocklist(client, m):
    asyncio.create_task(addablocklist(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['enable', 'activate'], ['!', '/']))
async def filter_enable(client, m):
    asyncio.create_task(enable(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['disable', 'deactivate'], ['!', '/']))
async def filter_disable(client, m):
    asyncio.create_task(disable(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['enableable', 'disableable'], ['!', '/']))
async def filter_disEn(client, m):
    asyncio.create_task(en_dis_able(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['disabledcmds'], ['!', '/']))
async def filter_disabled(client, m):
    asyncio.create_task(disabled(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['enabledcmds'], ['!', '/']))
async def filter_enabled(client, m):
    asyncio.create_task(enabled(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['antiservice', 'captcharules', 'antichannelpin', 'privaterules', 'captcha', 'cleanwelcome', 'captchakick', 'lang_detect', 'noteshash'], ['!', '/']) & filters.text)
async def filter_antiser(client, m):
    asyncio.create_task(antiservice(client, m))
    asyncio.create_task(filters_go(client, m))


@bot.on_message(filters.command(['captchamode'], ['!', '/']))
async def filter_cmode(client, m):
    asyncio.create_task(cmode(client, m))
    asyncio.create_task(filters_go(client, m))


# welcome
@bot.on_message(filters.new_chat_members)
async def new_members(client, m, *args):
    chat_id = m.chat.id    
    currentTime = int(time.time())
    if not args:
        memb = m.new_chat_members[0]
        user_id = memb.id
        fname = memb.first_name
        lname = memb.last_name
        uname = memb.username
        is_bot = memb.is_bot
    else:
        memb = m.new_chat_member.user
        user_id = memb.id
        fname = memb.first_name
        lname = memb.last_name
        uname = memb.username
        is_bot = memb.is_bot
    if memb.username == bot_username:
        create_db(m.chat.id)
        det = datetime.datetime.now(
            tz)+timedelta(seconds=0.000001)
        sj.add_job(syncInfos, "date", run_date=det,
                   args=[client, m])
        return
    try:
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
    except:
        create_db(m.chat.id)
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
    if not obj[f"{bot_id}"]["enable_disable"]["greetings"]:
        print("disabled")
        return
    cleanwelcome = obj[f"{bot_id}"]["on_off"]["cleanwelcome"]
    captcha = obj[f"{bot_id}"]["on_off"]["captcha"]
    welcomes = obj[f"{bot_id}"]['welcome']
    welcomes_2nd = obj[f"{bot_id}"]['2nd_welcome']
    capm = obj[f"{bot_id}"]['captchamode']
    
    ## old member
    nob = {str(chat_id): [] }
    if not os.path.isfile(f"db/mem/X{chat_id}.txt"):        
        with open(f"db/mem/X{chat_id}.txt", 'w+') as fm:
            json.dump(nob, fm, indent=4)
    with open(f"db/mem/X{chat_id}.txt", 'r') as fm:
        nobj = json.load(fm)
    oldNew = nobj[f"{chat_id}"]
    
    if obj[f"{bot_id}"]["raid"]["status"] == "on":
        runningFrom = obj[f"{bot_id}"]["raid"]["started_time"]
        kickFor = int((obj[f"{bot_id}"]["raid"]["kick_for"])[:-1]) * 3600
        durationTime = (obj[f"{bot_id}"]["raid"]["duration"])[:-1]
        wholeDuration = int(durationTime) * 3600
        if currentTime - int(runningFrom) <= wholeDuration:
            try:
                await client.ban_chat_member(chat_id=chat_id, user_id=user_id, until_date=datetime.now() + timedelta(seconds=kickFor))
            except Exception as e:
                print(e)
        else:
            obj[f"{bot_id}"]["raid"]["status"] = "off"
            obj[f"{bot_id}"]["raid"]["started_time"] = 0
            with open(f"db/X{chat_id}_db.txt", 'w+') as wf:
                json.dump(obj, wf, indent=4)
        return
    else:
        fbun = []
        cfed = None
        IsFbanned = None
        with open(f"db/fed.txt", "r") as fr:
            fids = json.load(fr)  
        try:
            cfed = fids["per_group"][str(chat_id)]
        except KeyError:
            pass
        if cfed:        
            with open(f"db/fedbans.txt", "r") as fr:
                fcons = json.load(fr)   
            try:
               reason = fcons[str(cfed)][str(user_id)]
               IsFbanned = True
               user_ed = await mention_html(user_id, fname)  
               await client.ban_chat_member(chat_id=chat_id,
                                         user_id=int(user_id))                      
               fedname =  fids["allfeds"][str(cfed)]["name"]               
               await client.send_message(text=f"""{user_ed} is banned in current federation {fedname} , so has been removed !\n\n**Reason**: {reason}""", chat_id=chat_id)
               return
            except Exception as e:
                pass
                
               ### Temp bans
            if str(fname).strip() == "共富国际娱乐":    
                   await client.ban_chat_member(chat_id=chat_id,
                                         user_id=int(user_id))
                   fadmin = await mention_html(my_bot_id, "Ultron")
                   ulink = f"[Link](tg://openmessage?user_id={user_id})"                 
                   fedname = fids['allfeds'][str(cfed)]["name"]     
                   user_ed = await mention_html(user_id, fname)         
                   reason = "potential spammer"
                   fban_text = f"""
**New FedBan**
**Fed:** {fedname}
**FedAdmin:** {fadmin}
**User:** {user_ed}
**User ID:** `{user_id}`
**permanent link:** {ulink}
**Reason:** {reason}              
""" 
                   await client.send_message(chat_id, fban_text)
                   asyncio.create_task(ben(client, m, cfed, user_id))               
                   fcons.update(
                                {str(cfed): {str(user_id): str(reason)}})
                   try:
                       cid = fcons["allfeds"][str(cfed)]["log_chat"]
                       if int(chat_id) != int(cid):
                           asyncio.create_task(send_log(cid, fban_text))
                   except:
                       pass
                   with open("db/fedbans.txt", "w+") as rit:
                        json.dump(fcons, rit, indent=4)        
                        
                   return
               #### 
                              
                
        if IsFbanned:
            return
        else:
            oldMember = None
            if int(user_id) in oldNew:
                oldMember = True
            if captcha and not is_bot and not oldMember:
                await client.restrict_chat_member(chat_id=chat_id,
                                                  user_id=user_id,
                                                  permissions=ChatPermissions()
                                                  )
            if oldMember:              
                x = random.choice(welcomes_2nd)
            else:             
                if not os.path.isfile(f"db/mem/X{chat_id}_joins.txt"):
                   with open(f"db/mem/X{chat_id}_joins.txt", 'w+') as ww:
                       json.dump(nob, ww, indent=4)
                with open(f"db/mem/X{chat_id}_joins.txt", 'r') as see:
                   sobj = json.load(see)                     
                if int(user_id) in sobj[str(chat_id)]:
                    x = random.choice(welcomes_2nd)
                else:                    
                    x = random.choice(welcomes)                    
                    asyncio.create_task(add_retards(chat_id, user_id, sobj))
            asyncio.create_task(welcome_sender(
                client, m, x, chat_id, None, captcha, user_id, is_bot, cleanwelcome, memb, capm, oldMember))
    det = datetime.datetime.now(
        tz)+timedelta(seconds=0.000001)
    sj.add_job(on_welcome_raw, "date", run_date=det,
               args=[chat_id, user_id, fname, lname, uname])


async def add_retards(chat_id, user_id, sobj):
    sobj[str(chat_id)].append(int(user_id))
    with open(f"db/mem/X{chat_id}_joins.txt", 'w+') as see:   
        json.dump(sobj, see, indent=4, sort_keys=True)
        
        
# let chat member    
@bot.on_message(filters.left_chat_member)
async def left_members(client, m):
    chat_id = m.chat.id
    rtm = m.id
    if m.left_chat_member.username == bot_username:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["greetings"] is not True:
        return
    else:
        goodbyes = obj[f"{bot_id}"]['goodbye']
        y = random.choice(goodbyes)
        asyncio.create_task(filter_helper(client, m, y, chat_id, rtm))


# On Updates


@bot.on_chat_member_updated()
async def __(client, m):
    if m.new_chat_member:
        try:
            hmm = m.service
        except:
            mem = m.new_chat_member
            if m.invite_link and m.invite_link.creates_join_request is True:
                if mem.status == "member" or mem.status == "restricted":
                    asyncio.create_task(new_members(client, m, mem))
    chat_id = m.chat.id
    asyncio.create_task(admins_col(client, m, m.chat.id))


# service

@bot.on_message(filters.service & filters.group)
async def service_msgs(client, m):
    chat_id = m.chat.id
    if os.path.isfile(f"db/X{chat_id}_db.txt"):
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["on_off"]["antiservice"] is True or obj[f"{bot_id}"]["raid"]["status"] == "on":
            await m.delete()
    else:
        create_db(m.chat.id)
        asyncio.create_task(service_msgs(client, m))


# private
@bot.on_message(filters.private & ~filters.forwarded)
async def private_filters(client, m):
    if m.text:
        if m.text[1:].startswith('start') or m.text[1:].startswith('help'):
            try:
                hmm = str(m.text).split('/start ', 1)[1]
                chat_id = hmm.split('_')[0]
                catagory = hmm.split('_')[1]

                if str(catagory) == "PRIVATE-NOTES-LIST":
                    await noteslist_callback(client, m, chat_id)

                elif str(catagory) == "NOTES":
                    note_name = hmm.split('_', 2)[2]
                    await private_notes(client, m, chat_id, note_name)

                elif str(catagory) == "RULES":
                    await check_rules_cb(client, m, chat_id)

                elif str(catagory) == "CAPTCHA":
                    user_id = hmm.split('_')[2]
                    await verify_captcha(client, m, chat_id)

                elif str(catagory) == "resendfile":
                    user_id = m.from_user.id
                    msgid = hmm.split('_')[2]
                    if await is_admin(client, m, chat_id, user_id) is True:
                        await resend_file(client, m, chat_id, msgid)
                    else:
                        await m.reply_text("You aren't admin !", quote=True)
            except Exception as d:
                pass


ch = ['!', '/']
save_me = {}
spam_chats = {}

# Filters


@bot.on_message(filters.group)
async def filters_go(client, m):
    try:
        qq = int(time.time())
        chat_id = m.chat.id
        sabe = save_me.get(chat_id)
        is_spammed = spam_chats.get(chat_id)
        if is_spammed:
            if (qq - is_spammed) < 300:
                return
        if not sabe:
            nums = 1
            times = int(qq)
            save_me.update({chat_id: f"{nums}_{times}"})
        else:
            nums = int(sabe.split('_')[0]) + 1
            times = int(sabe.split('_')[1])
            if nums >= 13:  # times
                if (int(qq) - times) <= 5:  # Seconds
                    spam_chats.update({chat_id: qq})
                    save_me.pop(chat_id)
                    print(
                        f"ignoring = {chat_id} - {m.chat.title} - @{m.chat.username}")
                  #  await client.send_message(chat_id, "spamming detected.\nLet me sleep for 5 minutes 😴.")
                else:
                    save_me.update({chat_id: f"1_{qq}"})
            else:
                save_me.update({chat_id: f"{nums}_{times}"})

        if m.sender_chat:
            user_id = m.sender_chat.id
        else:
            user_id = m.from_user.id

        # begin()
        chat_id = m.chat.id
        if os.path.isfile(f"db/X{chat_id}_db.txt"):
            with open(f"db/X{chat_id}_db.txt", 'rb') as f:
                obj = json.load(f)
            is_notes = obj[f"{bot_id}"]["enable_disable"]["notes"]
            is_filters = obj[f"{bot_id}"]["enable_disable"]["filters"]
            is_blocklist = obj[f"{bot_id}"]["enable_disable"]["blocklists"]
            is_locks = obj[f"{bot_id}"]["enable_disable"]["locks"]
            is_advanced_blocklist = obj[f"{bot_id}"]["enable_disable"]["ablocklists"]
            is_anti = obj[f"{bot_id}"]["enable_disable"]["antiflood"]
            lang_detect = obj[f"{bot_id}"]["on_off"]["lang_detect"]
            captcha = obj[f"{bot_id}"]["on_off"]["captcha"]
            approvers = obj[f"{bot_id}"]["approved_channels_and_users"]
            antichannelpin = obj[f"{bot_id}"]["on_off"]["antichannelpin"]

            #### starts ####

            newAfk = None
            if m.text and str(m.text)[0] in ch:
                if await is_admin(client, m, m.chat.id, user_id) is True:
                    wart = str(m.text).split()[0]
                    if f"{wart}" == "!nsfw" or f"{wart}" == "/nsfw":
                        await m.reply_text("Quota exceeded !")
                        return
                        if m.reply_to_message:
                            det = datetime.datetime.now(
                                tz)+timedelta(seconds=0.00000001)
                            sj.add_job(nchek, "date", run_date=det,
                                       args=[client, m])

            # antiflood
            if is_anti and not m.edit_date:
                asyncio.create_task(antiflood_go(client, m, obj))

            # notes
            if m.text and m.text.startswith('#') and is_notes is True and not m.edit_date:
                asyncio.create_task(group_notes(client, m))

            # filters
            if is_filters is True and not m.edit_date:
                asyncio.create_task(filters_yo(client, m, obj, user_id))

            # antichannel pin
            if antichannelpin is True:
                asyncio.create_task(antipin(client, m))

            # Blocklists
            if is_blocklist is True:
                if await immutable(client, m, m.chat.id, user_id) is not True:
                    if int(user_id) not in approvers:
                        asyncio.create_task(roll_blocklist(client, m, obj))

            if is_advanced_blocklist is True and not m.edit_date:
                if await immutable(client, m, m.chat.id, user_id) is not True:
                    if int(user_id) not in approvers:
                        asyncio.create_task(callback_spam(client, m, obj))

            if is_locks is True:
                if await immutable(client, m, m.chat.id, user_id) is not True:
                    if int(user_id) not in approvers:
                        asyncio.create_task(locks(client, m, obj))
            if not newAfk:
                asyncio.create_task(menafk(client, m))

            if lang_detect is True:
                if await immutable(client, m, m.chat.id, user_id) is not True:
                    if int(user_id) not in approvers:
                        asyncio.create_task(lang_detection(client, m, obj))
        else:
            create_db(chat_id)
            await filters_go(client, m)
    except:
        pass
