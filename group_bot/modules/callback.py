import os
import json
import re
from pyrogram import *
from pyrogram.types import *
from config import *
import asyncio
import random
import string
from group_bot import bot, mention_html
from group_bot.modules.helpers.db import create_db
from group_bot.modules.helpers.decode_btns import decode_btns
from group_bot.modules.helpers.filter_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.notes import group_notes, private_notes
from group_bot.modules.admin_check import is_admin, admins_col, can_restrict
from group_bot.modules.give_id import return_id
import time
from group_bot.modules.blocklist import ban, mute, tmute, kick_member, tban, tmute, warn

from group_bot.modules.warnings import warn_damage
from group_bot.modules.help import helpKey
from group_bot.modules.admin import vpromote, vdemote
from group_bot.modules.ban import (
    vmute,
    vunmute,
    vsmute,
    vdmute,
    vtmute,
    vunmute,
    vban,
    vdban,
    vsban,
    vtban,
    vunban,
    vkick,
    vdkick,
    vskick,
    verified
)

from group_bot.modules.fbans import fed_admins, ben, send_log
import html

backKey = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="BACK",
            callback_data="BACK_HELP")]])


calls = {}


@bot.on_callback_query()
async def m_buttons(client, m):
    if str(m.data).endswith('_delete'):
        user_id = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
            try:
                await client.delete_messages(chat_id=chat_id,
                                             ids=m.message.id)
            finally:
                try:
                    await client.delete_messages(chat_id=chat_id,
                                                 ids=m.message.reply_to_message.id)
                except:
                    pass
        else:
            await m.answer(text="You aren't admin !", show_alert=True)

    elif str(m.data).endswith('_mute'):
        user_id = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
            try:
                await client.restrict_chat_member(chat_id=chat_id,
                                                  user_id=user_id,
                                                  permissions=ChatPermissions()

                                                  )
            except Exception as cm:
                await m.message.edit(str(cm))
            finally:
                fname = (await client.get_chat(user_id)).first_name
                user = await mention_html(user_id, fname)
                await m.message.edit(f"Muted {user} !")
            try:
                await client.delete_messages(chat_id=chat_id,
                                             ids=m.message.reply_to_message.id)
            except:
                pass
        else:
            await m.answer(text="You aren't admin !", show_alert=True)
    elif str(m.data).endswith('_unmute'):
        user_id = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
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
            except Exception as cm:
                await m.message.edit(str(cm))
            finally:
                fname = (await client.get_chat(user_id)).first_name
                user = await mention_html(user_id, fname)
                ok_user = (await client.get_users(m.from_user.id)).mention
                await m.message.edit(f"Admin {ok_user} unmuted {user} !")
        else:
            await m.answer(text="You aren't admin !", show_alert=True)
    elif str(m.data).endswith('_unban'):
        user_id = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
            try:
                await client.unban_chat_member(chat_id=chat_id,
                                               user_id=user_id
                                               )
            except Exception as cm:
                await m.message.edit(str(cm))
            finally:
                fname = (await client.get_chat(user_id)).first_name
                user = await mention_html(user_id, fname)
                ok_user = (await client.get_users(m.from_user.id)).mention
                await m.message.edit(f"Admin {ok_user} unbanned {user} !")
        else:
            await m.answer(text="You aren't admin !", show_alert=True)
            
    elif str(m.data).endswith('_rban'):
        user_id = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
            if await can_restrict(client, m, chat_id, m.from_user.id):
                try:
                    await client.ban_chat_member(chat_id=chat_id,
                                               user_id=user_id
                                               )
                except Exception as cm:
                    await m.message.edit(str(cm))
                finally:
                    fname = (await client.get_chat(user_id)).first_name
                    user = await mention_html(user_id, fname)
                    ok_user = (await client.get_users(m.from_user.id)).mention
                    await m.message.edit(f"banned {user} !/n**Reason: Reported by user.")
            else:
                await m.answer(text="You don't have permission to ban users !", show_alert=True)
        else:
            await m.answer(text="You aren't admin !", show_alert=True)

    elif str(m.data).endswith('_rfban'):
        userid = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        user_id = m.from_user.id
        fadmin = m.from_user.mention
        if await is_admin(client, m, chat_id, user_id) is True:
            with open(f"db/fed.txt", "r") as fr:
                fcons = json.load(fr)
            try:
                cfed = fcons["per_group"][str(chat_id)]
            except KeyError:
                await m.answer("This group doesn't have any federation connected !", show_alert=True)
                return
            fadms = fcons['allfeds'][str(cfed)]["admins"]   
            reason = "spammer"
            if fadms:
                if int(user_id) in fadms or int(user_id) in fed_admins:
                    try:
                        await client.ban_chat_member(chat_id=chat_id,
                                                     user_id=userid)
                    except Exception as e:
                        if '[400 USER_ADMIN_INVAID]' in str(e):
                            try:
                                await m.chat.promote_member(
                                    user_id=userid,
                                    can_change_info=False,
                                    can_invite_users=False,
                                    can_delete_messages=False,
                                    can_restrict_members=False,
                                    can_pin_messages=False,
                                    can_promote_members=False,
                                    can_manage_chat=False,
                                    can_manage_voice_chats=False,
                                )
                            except:
                                await m.message.edit('I can not ban that admin !')
                                return
                        else:
                            await m.message.edit(str(e))
                            return
                    ulink = f"[Link](tg://openmessage?user_id={userid})"
                    user = (await client.get_users(userid)).mention
                    fedname = fcons['allfeds'][str(cfed)]["name"]
                    with open("db/fedbans.txt", "r") as red:
                        fbanned = json.load(red)
                    try:
                        reason = fbanned[str(cfed)][str(userid)]
                        await m.message.edit(f"{user} is already fbanned in current federation {fedname}\n**Reason:** {reason}")
                        return
                    except KeyError:
                        try:
                            fbanned[str(cfed)][str(userid)] = str(reason)
                        except:
                            fbanned.update(
                                {str(cfed): {str(userid): str(reason)}})
                    fban_text = f"""
**New FedBan**
**Fed:** {fedname}
**FedAdmin:** {fadmin}
**User:** {user}
**User ID:** `{userid}`
**permanent link:** {ulink}
**Reason:** {reason}              
""" 
                    await m.message.edit(fban_text)
                    asyncio.create_task(ben(client, m, cfed, userid))
                    try:
                       cid = fcons["allfeds"][str(cfed)]["log_chat"]
                       if int(chat_id) != int(cid):
                           asyncio.create_task(send_log(cid, fban_text))
                    except:
                       pass
                    with open("db/fedbans.txt", "w+") as rit:
                        json.dump(fbanned, rit, indent=4)
                else:
                    await m.answer(text="You aren't a fed admin !", show_alert=True)
        else:
            await m.answer(text="You aren't a admin !", show_alert=True)

    elif str(m.data).endswith('_ignore'):
        user_id = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
            try:
                await client.delete_messages(chat_id=chat_id,
                                             ids=m.message.id)
            except Exception as e:
                print(e)
                pass
        else:
            await m.answer(text="You aren't admin !", show_alert=True)

    elif str(m.data).endswith('_warn'):
        user_id = str(m.data).split('_')[0]
        chat_id = m.message.chat.id
        reason = "Spamming"
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
            try:
                with open(f"db/X{chat_id}_db.txt", 'r') as f:
                    obj = json.load(f)
                y = obj[f"{bot_id}"]['max_warns']
                with open("db/warns.txt", "r") as se:
                    wob = json.load(se)
                try:
                     reasons = wob["warns"][f"{chat_id}_{user_id}"]
                except KeyError:
                     reasons = ""
                if len(str(reasons)) > 3 and reasons is not None:
                    reason_lists = reasons.split('[%%%]')
                    warn_numbers = len(reason_lists) - 1
                else:
                    warn_numbers = 0
                reasons += f"""{reason}[%%%]"""
                wants = warn_numbers+1
                if str(wants) == str(y):
                    await warn_damage(client, m, user_id, chat_id)
                    return
            except Exception as cw:
                await m.message.edit(str(cw))
            fname = (await client.get_chat(user_id)).first_name
            user = await mention_html(user_id, fname)
            warn_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text=f"Remove warn", callback_data=f"{user_id}_unwarn")]
            ])
            await m.message.edit(
                f"{user} has {wants}/{y} warnings !\n<b>Reason:</b> {reason}", reply_markup=warn_keyboard)
            wob["warns"][f"{chat_id}_{user_id}"] = reasons
            with open("db/warns.txt", "w+") as se:
                 json.dump(wob, se, indent=6, sort_keys=True)
        else:
            await m.answer(text="You aren't admin !", show_alert=True)

    elif str(m.data).endswith("_unwarn"):
        user_id = str(m.data).split('_')[0]
        fname = (await client.get_chat(user_id)).first_name
        user = await mention_html(user_id, fname)
        chat_id = m.message.chat.id
        if await is_admin(client, m, chat_id, m.from_user.id) is True:
            ok_user = (await client.get_users(m.from_user.id)).mention
            with open("db/warns.txt", "r") as se:
                 wob = json.load(se)
            try:
                 reasons = wob["warns"][f"{chat_id}_{user_id}"]
            except KeyError:
                reasons = ""
            if len(str(reasons)) > 1 and reasons:
                fst = str(reasons[:-5]).rfind("[%%%]")
                reasons = reasons[:(fst+5)]
                await m.message.edit(
                    f"Admin {ok_user} Removed {user}'s warning. ")
                wob["warns"][f"{chat_id}_{user_id}"] = reasons
                with open("db/warns.txt", "w+") as se:
                    json.dump(wob, se, indent=6, sort_keys=True)
            else:
                await m.message.edit(f"{user} hadn't any warning !")
        else:
            await m.answer(text="You aren't admin !", show_alert=True)
            
    elif str(m.data).startswith("verifyanonadmin_"):
         user_id = m.from_user.id
         userid = m.data.split('_')[1]
         chat_id = m.message.chat.id
         if await is_admin(client, m, chat_id, user_id):
               asyncio.create_task(verified(client, m.message, user_id, True))
         await m.message.delete()
               
    elif "verifyadmin_" in str(m.data):
        what_to_do = m.data.split('_')[1]
        user_id = m.from_user.id
        userid = m.data.split('_')[2]
        chat_id = m.message.chat.id

        # promote demote
        if what_to_do == "promote":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vpromote(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "demote":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vdemote(client, m, user_id, userid))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)

        # mute things
        elif what_to_do == "vmutev":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vmute(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vdmutev":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vdmute(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vsmutev":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vsmute(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vtmutev":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vtmute(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vunmutev":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vunmute(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)

        # ban things
        elif what_to_do == "vbanv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vban(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vdbanv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(
                    vdban(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vsbanv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vsban(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vtbanv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vtban(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vunbanv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vunban(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)

        # kick things
        elif what_to_do == "vkickv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vkick(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vskickv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vskick(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
        elif what_to_do == "vdkickv":
            if await is_admin(client, m, chat_id, user_id) is True:
                asyncio.create_task(vdkick(client, m, user_id, userid, None))
            else:
                await m.answer(text="You aren't admin !", show_alert=True)
    elif "_givecaptcha" in str(m.data):
        user_id = m.data.split('_')[0]
        if int(user_id) == m.from_user.id:
            if m.message.sticker:
                await m.message.delete()
                gen = await client.send_message(text="`Generating captcha ...`", chat_id=m.message.chat.id)
            else:
                gen = await m.message.edit("`Generating captcha ...`")
            capinfo = await makecall(client, m, user_id)
            newbtn = capinfo[0]
            mt = capinfo[1]
            await asyncio.sleep(1)
            userp = await client.get_chat(user_id)
            user = await mention_html(userp.id, userp.first_name)
            await gen.edit(text=f"""Hey {user}, press the word "**{mt}**" from the below buttons. You will be kicked if you loose 3 chances !""", reply_markup=newbtn)
        else:
            await m.answer(text="❌ This message isn't for you !", show_alert=True)
    elif "_vericap_" in str(m.data):
        detas = m.data.split('_')
        chat_id = m.message.chat.id
        user_id = detas[0]
        deta = detas[2]
        main_text = detas[3]
        if int(user_id) == m.from_user.id:
            if deta == main_text:
                with open(f"db/X{chat_id}_db.txt", 'r') as f:
                    obj = json.load(f)
                if obj[f"{bot_id}"]["on_off"]["captcharules"] is True:
                    rules = obj[f"{bot_id}"]["rules"]
                    chat = (await client.get_chat(chat_id)).title
                    rulk = InlineKeyboardMarkup([[InlineKeyboardButton(
                        text=f"I have read and accept the rules", callback_data=f"{chat_id}_{user_id}_unmuteme")]])
                    await m.message.edit(f"Rules in `{chat}` are:\n\n{rules}", reply_markup=rulk)
                else:
                    try:
                        await m.message.delete()
                    except:
                        pass
                    try:
                        await client.restrict_chat_member(chat_id=m.message.chat.id,
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
                    except Exception as fr:
                        await m.message.edit(str(fr))
                    finally:
                        with open(f"db/mem/X{chat_id}.txt", "r") as rd:
                            nob = json.load(rd)
                        nob[f"{chat_id}"].append(int(user_id))
                        with open(f"db/mem/X{chat_id}.txt", 'w+') as f:
                            json.dump(nob, f, indent=4)

            else:
                block = f"{chat_id}_{user_id}"
                ci1 = calls.get(block)
                maxcn = 3
                if not ci1:
                    calls.update({block: 1})
                    hcnp = maxcn - 1
                    hcn = f"{hcnp} chances"
                else:
                    calls.update({block: (ci1 + 1)})
                    hcnp = maxcn - (ci1 + 1)
                    hcn = f"{hcnp} chances"
                if hcnp == 1:
                    hcn = "1 chance"
                if hcnp == 0:
                    userp = await client.get_chat(user_id)
                    user = await mention_html(userp.id, userp.first_name)
                    await m.message.delete()
                    await m.message.reply_text(f"❌ {user} failed to verify the captcha, they can try again later !")
                    try:
                        await client.ban_chat_member(chat_id=chat_id,
                                                     user_id=user_id, until_date = int(time.time()+ 35))                   
                    finally:
                        calls.pop(block)
                        await client.unban_chat_member(chat_id=chat_id,
                                                       user_id=user_id)
                    return
                await m.answer(text=f"Incorrect ! You have {hcn} left !", show_alert=True)
        else:
            await m.answer(text="❌ This message isn't for you !", show_alert=True)
    elif "_unmuteme" in str(m.data):
        detas = m.data.split('_')
        chat_id = detas[0]
        user_id = detas[1]
        if int(user_id) == m.from_user.id:
            try:
                await client.restrict_chat_member(chat_id=m.message.chat.id,
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
                try:
                    await m.message.delete()
                except:
                    pass
            except Exception as fr:
                await m.message.edit(str(fr))
            finally:
                with open(f"db/mem/X{chat_id}.txt", "r") as rd:
                      nob = json.load(rd)
                nob[f"{chat_id}"].append(int(user_id))
                with open(f"db/mem/X{chat_id}.txt", 'w+') as f:
                      json.dump(nob, f, indent=4)
        else:
            await m.answer(text="❌ This message isn't for you !", show_alert=True)
            
    elif "_iaccept" in str(m.data):
        detas = m.data.split('_')
        chat_id = detas[0]
        user_id = detas[1]
        with open(f"db/mem/X{chat_id}.txt", 'r') as f:
            obj = json.load(f)
        if int(user_id) in obj[str(chat_id)]:
            await m.message.edit(f"You have already completed the captcha !")
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
                cha = await client.get_chat(chat_id)
                chat = cha.title
                rke = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text=f"Back to support group", url=f"{cha.invite_link}")]
                ])
                await m.message.edit(f"Fine, you are unmuted in `{chat}` !", reply_markup=rke)
            except Exception as fr:
                await m.message.edit(str(fr))
            finally:                
                obj[f"{chat_id}"].append(int(user_id))
                with open(f"db/mem/X{chat_id}.txt", 'w+') as f:
                      json.dump(obj, f, indent=4)


    elif str(m.data) == 'BACK_HELP':
        await m.message.edit("""
**HELP MENU**

This is just an on-point lists for all functions, all commands can be used with '/' and '!' .

__To mention users in messages you can write:__
`{id}` : user's id,
`{first}` : first name of user,
`{last}` : last name of user,
`{mention}` : mentioned a user,
`{username}` : username of user,
`{group}` : name of the group.
""", reply_markup=helpKey)

    elif str(m.data) == 'ADMINSCMD_HELP':
        await m.message.edit(f"""
**ADMIN**

-/promote <reply/username/mention/userid> : Promotes a user
-/demote <reply/username/mention/userid> : Demotes a admin
-/admincache : Refreshes admincache(useless though, cause Ultron updates those on respective events)
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == "ANTIFLOOD_HELP":
        await m.message.edit(f"""
**ANTIFLOOD**

-/flood : Get the current antiflood settings
-/setflood <number>(must me greater than 1) : Set the number of messages of messages after which to take action on a user
-/setfloodmode <action> : Choose the action to take on user who overcomes flood. (ban/kick/mute/tmute/tban)
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == "APPROVAL_HELP":
        await m.message.edit(f"""
**APPROVAL**

-/approve : Approves a user, they will be ignored by blocklists, advanced-blocklists, antiflood and locks
-/disapprove : disapproves a user, Approves user will be now a normal user.
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == "BANS_HELP":
        await m.message.edit(f"""
**BANS**

-/ban : bans a user
-/unban : unbans a user
-/tban : Temporarily bans a user
-/dban : Ban and deletes user's message
-/sban : Silently bans a user without showing the ban message

-/kick : Kicks a user
-/skick : Silently kicks a user
-/dkick : detele replied message and kicks the user
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == "MUTE_HELP":
        await m.message.edit(f"""
**MUTES**

-/mute : Mutes a user
-/unmute : Unmutes a user
-/tmute : Temporarily mute a user
-/dmute : Detele reply to message of the user and mutes him
-/smute : Siletly mutes a user without showing mute message
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == "BLOCKLIST_HELP":
        await m.message.edit(f"""
**BLOCKLISTS**

-/addblocklist <trigger> <reason> <{{true}}> <{{mute | tmute | ban | tban | kick | warn}} : Add blocklist word
-/rmblocklist : removes the trigger from blocklist
-/blocklist : Shows all blocklisted triggers with fillings

--filling can be used:--
{{true}} : Weather to show up the warning message
{{mute | tmute | ban | tban | kick | warn}} : These can be the actions when user trigges the blocklist (Bydefault it will just deletes th emessage) 

""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == "CAPTCHA_HELP":
        await m.message.edit(f"""
**CAPTCHA**

-/captcha <on | off>
-/captchamode <button | text> : set the captcha mode
-/captcharules <on | off> : Force the users to read and accept the rules

""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)
    elif str(m.data) == 'AFK_HELP':
        await m.message.edit("""
**AFK**
(Only for admins)

-/afk <reason> : Set your status as "Away From Keyboard". Adding a reason in optional
""", reply_markup=backKey)

    elif str(m.data) == 'ANTI_HELP':
        await m.message.edit("""
**ANTI**

-/antiservice : Delete services messages sent by Telegram (example: "User joined the group", "User has left the group")
-/antichannelpin : Unpin every message pinned automatically in a group due to be connected to a channel
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'EN_DIS_ABLE_HELP':
        await m.message.edit(f"""
**DISABLE/ENABLE**

-/disable <command> : Disable that command from the bot
-/enable <command> : Re-enable a disabled command
-/disableable or /enableable : Check list of functions which can be disbled
-/disabledcmds : Get the list of currently disabled commands
-/enabledcmds : Get the list of currently enabled commands
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'FED_HELP':
        await m.message.edit("""
**FEDERATIONS**


-/fban : Ban an user from the federation of the group
-/unfban : Un ban an user from the federation of the group
-/chatfed : Get connected fed info
-/createfed (in pm): Create a new federation
-/fstat : get fban info of a user
-/renamefed : rename a fed name
-/setlogchat : set the same group for fed logs
-/fedinfo : Get fed's info
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'FILTER_HELP':
        await m.message.edit("""
**FILTERS**

-/filter <trigger> <text> : Set "text" to be sent when a message containts "trigger"
-/stop <trigger> : Stop the filter linked to "trigger"
-/filters : Retrieve the list of current filters in a group

**Fillings can be used while adding/saving a filter :(optional)**

i) `{admins}` | `{members}` :
 __ To specify filter should trigger on users only or admins only, bydefault it will trigger for both.__

ii) `{text}` | `{stickers}` | `{gif}` | `{document}` | `{photo}` | `{video}` | `{audio}` :
__ to specify type of message filter should action on, by default it's 'text'.__

iii) `{full_match}` :
 __ only triggers if filtered text == user',s message__

iv) `{preview}` : 
__ To show message with preview, by default link preview is off. __

v) `{protect}` :
__users can't forward that message.__
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'LOCKS_HELP':
        await m.message.edit("""
**LOCKS**

-/locktypes : Retrieves the list of lockeable items
-/lock <locktype> : Locks "locktype"
-/unlock <locktype> : Unlocks "locktype"
-/locks : Retrieve the list of currently locked items in a group
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'WARNING_HELP':
        await m.message.edit("""
**WARNINGS**

-/warn <reason> : Warns an user by reply. Adding a reason is optional
-/dwarn : Deletes the replied message warns the user
-/swarn : Silently warns the user
-/warns : Reply to someone to check him/her warns
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == "GREETING_HELP":
        await m.message.edit(f"""
**WELCOMES/GOODBYES**

-/setwelcome <text> : Set the given text as the welcome text. Also works as a reply (without "text argument")
-/resetwelcome : Resets the welcome message to the default one
-/welcome : Shows the welcome message without formatting
-/setgoodbye <text> : Set the given text as the goodbye text. Also works as a reply (without "text argument")
-/resetgoodbye : Resets the goodbye message to the default one
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'REPORT_HELP':
        await m.message.edit(f"""
**REPORTS**

-/report : Reports an user to the admins. Works as a reply
-/dont_mention_me : As an admin, remove yourself from the pinged admins when an user uses the report command
-/mention_me : As an admin, add yourself back to the pinged admins when an user uses the report command 
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'MISC_HELP':
        await m.message.edit(f"""
**MISC**

-/info : Retrieves the user's information. Works by reply
-/id : Retrieves the user's ID. Works by reply
-/ping : Check's the bot ping
-/noformat or /nof : Retrieves the replied message as a text with the formatting kept in markdown symbols
-/nsfw : Check the nsfw safety from a photo/image 
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'RULES_HELP':
        await m.message.edit(f"""
**RULES**

-/private_rules <on | off> : Off to show the rules on the group itself.
-/setrules <text> : Set "text" as the rules for the group. Also works as a reply (without "text argument")
-/rules : Retrieves the group's rules
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'PURGE_HELP':
        await m.message.edit(f"""
**PURGE**

-/purge : Deletes every message sent after the replied message
-/purgefrom : Sets the replied message as the starting point to purge
-/purgeto : Sets the replied message as the end point to purge, after another message has been set with the purgefrom command
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'ANTIRAID_HELP':
        await m.message.edit(f"""
**ANTI-RAIDMODE**

-/raid : Enables/disable antiraid
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'PIN_UNPIN_HELP':
        await m.message.edit(f"""
**PINS**

-/pin : Pins the replied message
-/unpin : Unpins the replied message
-/pinned : Shows the pinned message of the group
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

    elif str(m.data) == 'IMPORT_EXPORT_HELP':
        await m.message.edit(f"""
**EXPORT/IMPORT**

-/export : Generates a file with the group's settings
-/import : Add the group's settings from an export file. Must be used as a reply to the file
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)


    elif str(m.data) == 'TR_HELP':
        await m.message.edit(f"""
**Translations**
(for admins only)

- /tr <lang code>: Translates any language to custom language
""", reply_markup=backKey, parse_mode=enums.ParseMode.MARKDOWN)

async def makecall(client, m, user_id):
    mt = ''.join(random.sample(string.ascii_uppercase, 6))
    t1 = ''.join(random.sample(string.ascii_uppercase, 6))
    t2 = ''.join(random.sample(string.ascii_uppercase, 6))
    t3 = ''.join(random.sample(string.ascii_uppercase, 6))
    t4 = ''.join(random.sample(string.ascii_uppercase, 6))
    t5 = ''.join(random.sample(string.ascii_uppercase, 6))
    t6 = ''.join(random.sample(string.ascii_uppercase, 6))
    t7 = ''.join(random.sample(string.ascii_uppercase, 6))
    t8 = ''.join(random.sample(string.ascii_uppercase, 6))

    ct = [mt, t1, t2, t3, t4, t5, t6, t7, t8]
    random.shuffle(ct)

    ckey = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=f"{ct[0]}",
            callback_data=f"{user_id}_vericap_{ct[0]}_{mt}"),
         InlineKeyboardButton(
            text=f"{ct[1]}",
            callback_data=f"{user_id}_vericap_{ct[1]}_{mt}"),
         InlineKeyboardButton(
            text=f"{ct[2]}",
            callback_data=f"{user_id}_vericap_{ct[2]}_{mt}")],

        [InlineKeyboardButton(
            text=f"{ct[3]}",
            callback_data=f"{user_id}_vericap_{ct[3]}_{mt}"),
         InlineKeyboardButton(
            text=f"{ct[4]}",
            callback_data=f"{user_id}_vericap_{ct[4]}_{mt}"),
         InlineKeyboardButton(
            text=f"{ct[5]}",
            callback_data=f"{user_id}_vericap_{ct[5]}_{mt}")],

        [InlineKeyboardButton(
            text=f"{ct[6]}",
            callback_data=f"{user_id}_vericap_{ct[6]}_{mt}"),
         InlineKeyboardButton(
            text=f"{ct[7]}",
            callback_data=f"{user_id}_vericap_{ct[7]}_{mt}"),
         InlineKeyboardButton(
            text=f"{ct[8]}",
            callback_data=f"{user_id}_vericap_{ct[8]}_{mt}")
         ]
    ])
    return ckey, mt
