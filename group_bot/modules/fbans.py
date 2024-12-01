import secrets
from pyrogram import Client, filters
from config import *
from group_bot import bot, bot2, mention_html
from group_bot.modules.give_id import return_id
from group_bot.modules.admin_check import is_admin, immutable, can_delete, can_restrict, can_promote, can_edit, can_pin
import asyncio
import json
import time


fed_admins = [1602293216, 5042954820,
              809293242, 19371046, 937038648, 319956169]

chats = [-1001235354108, -1001349019437, -1001353037906, -1001466266928,
         -1001542320014, -1001574127754, -1001605236910, -1001612215346,
         -1001716284663, -1001205981587, -1001797765388, -1001275077034,
         -1001309442997, -1001451186510, -1001889767694]

fdb = {}


@bot.on_message(filters.command(["createfed", 'createfederation'], ['!', '/']))
async def create_fed(client, m):
    chat_id = m.chat.id
    if m.from_user.id:
        user_id = m.from_user.id
        new_fed_id = secrets.token_hex(nbytes=20)
        with open(f"db/fed.txt", "r") as fr:
            finfos = json.load(fr)
        try:
            fed_id = finfos["feds"][str(user_id)]["fed_id"]
            fname = finfos["feds"][str(user_id)]["fed_name"]
        except KeyError:
            fed_id = None
        if fed_id:
            await m.reply_text(f"You already have a federation named `{fname}`\nID `{fed_id}`.")
        else:
            if " " in m.text:
                fname = m.text.split(' ', 1)[1]
                finfos["feds"][str(user_id)] = {"fed_id": str(new_fed_id),
                                                "fed_name": str(fname)
                                                }
                finfos['allfeds'].update(
                    {str(new_fed_id): {"name": str(fname), "admins": {str(user_id): {"name": m.from_user.first_name}}}})

                with open(f"db/fed.txt", "w+") as fr:
                    json.dump(finfos, fr, indent=4)
                await m.reply_text(f"Successfully created a new federation named `{fname}`\nID is `{new_fed_id}`")
            else:
                await m.reply_text("Give a fed name along with command !")


@bot.on_message(filters.command(["renamefed"], ['!', '/']))
async def rename_fed(client, m):
    chat_id = m.chat.id
    if m.from_user.id:
        user_id = m.from_user.id
        with open(f"db/fed.txt", "r") as fr:
            finfos = json.load(fr)
        try:
            fed_id = finfos["feds"][str(user_id)]["fed_id"]
            fname = finfos["feds"][str(user_id)]["fed_name"]
        except KeyError:
            fed_id = None
        if not fed_id:
            await m.reply_text(f"You don't have any federation.")
        else:
            if " " in m.text:
                fname = m.text.split(' ', 1)[1]
                finfos["feds"][str(user_id)] = {"fed_id": str(fed_id),
                                                "fed_name": str(fname)
                                                }
                finfos['allfeds'][str(fed_id)]["name"] = str(fname)
                with open(f"db/fed.txt", "w+") as fr:
                    json.dump(finfos, fr, indent=4)
                await m.reply_text(f"Successfully changed fed name to `{fname}`")
            else:
                await m.reply_text("Give new fed name along with command !")


@bot.on_message(filters.command(["myfeds"], ['!', '/']))
async def myfed(client, m):
    chat_id = m.chat.id
    if m.from_user.id:
        user_id = m.from_user.id
        with open(f"db/fed.txt", "r") as fr:
            finfos = json.load(fr)
        try:
            achhi = finfos["feds"][str(user_id)]["fed_id"]
            fname = finfos["feds"][str(user_id)]["fed_name"]
        except KeyError:
            achhi = None
        if achhi:
            await m.reply_text(f"You already have a federation named `{fname}`\nID `{achhi}`.")
        else:
            await m.reply_text("You don't have any federation.")


@bot.on_message(filters.command(["joinfed"], ['!', '/']))
async def joinfed(client, m):
    chat_id = m.chat.id
    if m.from_user.id:
        user_id = m.from_user.id
        if " " in m.text:
            fid = m.text.split(' ', 1)[1]
            if int(user_id) in sudo_users or (await client.get_chat_member(chat_id=chat_id, user_id=user_id)).status == "creator":
                with open(f"db/fed.txt", "r") as fr:
                    fids = json.load(fr)
                try:
                    fed_name = fids['allfeds'][str(fid)]["name"]
                except KeyError:
                    await m.reply_text(f"No such federation found for this fed ID")
                    return
                fids["per_group"].update({str(chat_id): str(fid)})
                try:
                    allchats = fids["per_fed"][str(fid)]["chats"]
                except KeyError:
                    fids["per_fed"].update(
                        {str(fid): {"chats": [], "subs": []}})
                    allchats = []
                if int(chat_id) not in allchats:
                    fids["per_fed"][str(fid)]["chats"].append(int(chat_id))

                with open(f"db/fed.txt", "w+") as fr:
                    json.dump(fids, fr, indent=4)
                await m.reply_text(f"Successfully joined a new federation `{fed_name}`")
            else:
                await m.reply_text("Only groups owner can join new feds !")
        else:
            await m.reply_text("Give a fed id to join in !")

@bot.on_message(filters.command(["leaveallfeds"], ['!', '/']))
async def joinfed(client, m):
      chat_id = m.chat.id
      if m.from_user.id:
            user_id = m.from_user.id
            if int(user_id) in sudo_users or (await client.get_chat_member(chat_id=chat_id, user_id=user_id)).status == "creator":
                with open(f"db/fed.txt", "r") as fr:
                    fids = json.load(fr)
                try:
                    imin = fids['per_group'][str(chat_id)]
                    del fids['per_group'][str(chat_id)]
                    fids["per_fed"][str(imin)]["chats"].remove(int(chat_id))
                    await m.reply_text(f"Successfully left all feds !")                 
                except KeyError:
                    await m.reply_text(f"This group doesn't have any fed connected !")
                    return
                           
                with open(f"db/fed.txt", "w+") as fr:
                    json.dump(fids, fr, indent=4)
                
            else:
                await m.reply_text("Only groups owner can join new feds !")
        

@bot.on_message(filters.command(["subfed"], ['!', '/']))
async def joinfed(client, m):
    chat_id = m.chat.id
    if m.from_user.id:
        user_id = m.from_user.id
        if " " in m.text:
            fid = m.text.split(' ', 1)[1]
            if int(user_id) in sudo_users or (await client.get_chat_member(chat_id=chat_id, user_id=user_id)).status == "creator":
                with open(f"db/fed.txt", "r") as fr:
                    finfos = json.load(fr)
                try:
                    achhi = finfos["feds"][str(user_id)]["fed_id"]
                    fname = finfos["feds"][str(user_id)]["fed_name"]
                except KeyError:
                    achhi = None
                if not achhi:
                    await m.reply_text("You don't have any federation connected with this group.")
                    return
                try:
                    fed_name = finfos['allfeds'][str(fid)]
                except KeyError:
                    await m.reply_text(f"No such federation found for this fed ID")
                    return
                if int(chat_id) not in finfos["per_fed"][str(fid)]["chats"]:
                    finfos["per_fed"][str(fid)]["chats"].append(int(chat_id))
                if str(achhi) not in finfos["per_fed"][str(fid)]["subs"]:
                    finfos["per_fed"][str(fid)]["subs"].append(str(achhi))
                with open(f"db/fed_cons.txt", "w+") as fr:
                    json.dump(finfos, fr, indent=4)
                await m.reply_text(f"Successfully subscribed a new federation `{fed_name}`")
            else:
                await m.reply_text("Only groups owner can join new feds !")


@bot.on_message(filters.command(["fpromote"], ['!', '/']))
async def fpromote(client, m):
    chat_id = m.chat.id
    if m.from_user.id:
        user_id = m.from_user.id
        with open(f"db/fed.txt", "r") as fr:
            finfos = json.load(fr)
        try:
            fed_id = finfos["feds"][str(user_id)]["fed_id"]
            fname = finfos["feds"][str(user_id)]["fed_name"]
        except KeyError:
            fed_id = None
        if not fed_id:
            await m.reply_text(f"You don't have a federation !")
        else:
            uidr = await return_id(client, m)
            uid = uidr[0]
            useri = await client.get_users(int(uid))
            usn = useri.first_name
            user = useri.mention
            if str(uid) not in finfos['allfeds'][str(fed_id)]["admins"]:

                #  await m.reply_text("confirm promotion !", reply_markup=
                finfos['allfeds'][str(fed_id)]["admins"][str(uid)] = {"name": usn}                   
                with open(f"db/fed.txt", "w+") as frd:
                    json.dump(finfos, frd, indent=4)
                await m.reply_text(f"{user} is now a fed-admin in {fname} !", quote=False)
            else:
                await m.reply_text(f"{user} is already a admin in {fname} !", quote=False)


@bot.on_message(filters.command(["fdemote"], ['!', '/']))
async def fpromote(client, m):
    chat_id = m.chat.id
    if m.from_user.id:
        user_id = m.from_user.id
        with open(f"db/fed.txt", "r") as fr:
            finfos = json.load(fr)
        try:
            fed_id = finfos["feds"][str(user_id)]["fed_id"]
            fname = finfos["feds"][str(user_id)]["fed_name"]
        except KeyError:
            fed_id = None
        if not fed_id:
            await m.reply_text(f"You don't have a federation !")
        else:
            uidr = await return_id(client, m)
            uid = uidr[0]
            user = (await client.get_users(int(uid))).mention
            
            if str(uid) in finfos['allfeds'][str(fed_id)]["admins"]:
                del finfos['allfeds'][str(fed_id)]["admins"][str(uid)]
                with open(f"db/fed.txt", "w+") as frd:
                    json.dump(finfos, frd, indent=4)                
                await m.reply_text(f"{user} has been demoted from {fname} fed !", quote=False)
            else:
                await m.reply_text(f"{user} was not a admin in this fed !", quote=False)


@bot.on_message(filters.command(["fstat"], ['!', '/'])) 
async def fstat(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        return
    else:
        user_id = m.from_user.id
        fadmin = m.from_user.mention
    if await is_admin(client, m, m.chat.id, user_id):
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["fban"] is not True:
            return
        with open(f"db/fed.txt", "r") as fr:
            fcons = json.load(fr)
        try:
            cfed = fcons["per_group"][str(chat_id)]
        except KeyError:
            await m.reply_text("This group doesn't have any federation connected !")
            return
        
        with open("db/fedbans.txt", "r") as red:
            fbanned = json.load(red)
        if " " in m.text or m.reply_to_message:
            userid = None
            statv = await return_id(client, m)
            userid = statv[0]
            try:
                userf = await client.get_chat(userid)      
                if not userf.first_name:
                    user = await mention_html(userid, userf.title)
                else:
                    user = await mention_html(userid, userf.first_name)
            except:
                user = userid
            if userid:
                fedname = fcons['allfeds'][str(cfed)]["name"]
                try:
                    user_banned = fbanned[str(cfed)][str(userid)]
                    await m.reply_text(f"{user} is banned in the current federation {fedname}.\n**Reason**: {user_banned}", disable_web_page_preview=True)
                except:
                    await m.reply_text(f"{user} is not banned in the current federation {fedname}.")


@bot.on_message(filters.command(["fban", "dfban", "sfban", "dsfban", "sdfban"], ['!', '/']))
async def fban1(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        return
    else:
        user_id = m.from_user.id
        fadmin = m.from_user.mention
    if await is_admin(client, m, m.chat.id, user_id):
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["fban"] is not True:
            return
        with open(f"db/fed.txt", "r") as fr:
            fcons = json.load(fr)
        try:
            cfed = fcons["per_group"][str(chat_id)]
        except KeyError:
            await m.reply_text("This group doesn't have any federation connected !")
            return
        fadms = fcons['allfeds'][str(cfed)]["admins"]
    else:
        return
    if str(user_id) in fadms or int(user_id) in fed_admins:
        if " " in m.text or m.reply_to_message:
            userid = None
            statv = await return_id(client, m)
            userid = statv[0]
            reason = statv[1]
            if userid:
                if int(userid) not in fadms and str(userid) not in fed_admins:
                    mtext = m.text.markdown
                    if reason:
                        reason = reason.strip()
                    fing = await m.reply_text("`Fbanning ...`", quote=False)
                    try:
                        await client.ban_chat_member(chat_id=chat_id,
                                                     user_id=userid)
                    except Exception as e:
                        if str(e) == """Telegram says: [400 USER_ADMIN_INVALID] - The action requires admin privileges. Probably you tried to edit admin privileges on someone you don't have rights to (caused by "channels.EditBanned")""":
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
                                await fing.edit('I can not ban that admin !')
                                return
                        else:
                            await fing.edit(str(e))
                            return
                    ulink = f"[Link](tg://openmessage?user_id={userid})"
                    userf = await client.get_chat(userid)
                    if userf.first_name:
                        user = await mention_html(userid, userf.first_name)
                    else:
                        user = await mention_html(userid, userf.title)
                    fedname = fcons['allfeds'][str(cfed)]["name"]
                    with open("db/fedbans.txt", "r") as red:
                        fbanned = json.load(red)
                    try:
                        reason = fbanned[str(cfed)][str(userid)]
                        await fing.edit(f"{user} is already fbanned in current federation {fedname}\n**Reason:** {reason}")
                        return
                    except KeyError:
                        try:
                            fbanned[str(cfed)][str(userid)] = str(reason)
                        except:
                            fbanned.update(
                                {str(cfed): {str(userid): str(reason)}})
                    fban_text= f"""
**New FedBan**
**Fed:** {fedname}
**FedAdmin:** {fadmin}
**User:** {user}
**User ID:** `{userid}`
**permanent link:** {ulink}
**Reason:** {reason}              
"""
                    await fing.edit(fban_text)
                    try:
                        if "s" in str(m.text.split()[0]).lower():
                             try:
                                 await m.delete()
                             except:
                                 pass
                        elif "d" in str(m.text.split()[0]).lower():
                             try:
                                 await m.reply_to_message.delete()
                             except:
                                 pass
                        elif "d" in str(m.text.split()[0]).lower() and "s" in str(m.text.split()[0]).lower():
                             try:
                                 await m.reply_to_message.delete()
                             finally:
                                 try:
                                     await m.delete()
                                 except:
                                     pass
                    except:
                        pass
                    asyncio.create_task(ben(client, m, cfed, userid))
                    try:
                        cid = fcons["allfeds"][str(cfed)]["log_chat"]
                        if int(chat_id) != int(cid):
                            asyncio.create_task(send_log(cid, fban_text))
                    except:
                       pass
                    with open("db/fedbans.txt", "w+") as rit:
                        json.dump(fbanned, rit, indent=4)        
                    if user_id in fed_admins:
                        await bot2.send_message(-1001554911069, f"/fban {userid} {reason}")
                else:
                    await m.reply_text("I can't ban a fed admin from their own fed !")
            else:
                await m.reply_text("User id not found !")
        else:
            await m.reply_text("Mention a user to fedban him !")


#@bot.on_message(filters.command(["superfban"], ['!', '/']) & ~filters.rivate & ~filters.edited)
async def superfban1(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        return
    else:
        user_id = m.from_user.id
        fadmin = m.from_user.mention
    if int(user_id) in fed_admins:
        asyncio.create_task(ben(client, m, chat_id, user_id))


@bot.on_message(filters.command(["chatfed"], ['!', '/']))
async def fchatfed(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        return
    else:
        user_id = m.from_user.id
        fadmin = m.from_user.mention
    if await is_admin(client, m, m.chat.id, user_id):
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["fban"] is not True:
            return
        with open(f"db/fed.txt", "r") as fr:
            fids = json.load(fr)  
        try:
            cfed = fids["per_group"][str(chat_id)]
        except KeyError:
            await m.reply_text(f"No fed connected with this chat !")
            return
        fedname =  fids["allfeds"][str(cfed)]["name"]
        await m.reply_text(f"**Connected fed name:** {fedname}\n**Fed ID:** `{cfed}`")

@bot.on_message(filters.command(["fedinfo", "finfo"], ['!', '/']))
async def finfo(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        return
    else:
        user_id = m.from_user.id
        fadmin = m.from_user.mention
    if await is_admin(client, m, m.chat.id, user_id):
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["fban"] is not True:
            return
        if not " " in m.text:
            return
        fid = m.command[1]
        with open(f"db/fed.txt", 'r') as f:
            one = json.load(f)
        try:
            fedname = one['allfeds'][str(fid)]["name"]
            fedadms = one['allfeds'][str(fid)]["admins"]
            fd = ""
            for i in fedadms:              
                fn = one['allfeds'][str(fid)]["admins"][str(i)]["name"]                
                fd += f"""\n[{fn}](tg://openmessage?user_id={i}),"""
            fd = fd[:-1]
        except KeyError:
            await m.reply_text("Couldn't find any federation with this ID !")
            return
        conn_chats = one["per_fed"][str(fid)]["chats"]
        
        if len(conn_chats) == 0:
            conn_chats = None
        else:
            conn_chats = str(conn_chats)[1:-1]
        subbed_feds = one["per_fed"][str(fid)]["subs"]
        x = 0
        suf = ""
        for fe in subbed_feds:
             sufn = one['allfeds'][str(fe)]["name"]
             x += 1
             suf += f"\n**{x})** `{fe}` [{sufn}]"
        if len(suf) < 2:
             suf = None
        if len(subbed_feds) == 0:
            subbed_feds = None

        fmes = f"""
**Fed ID:** `{fid}`
**Fed name:** {fedname}
**connected chats:** {conn_chats}
**subscribed feds:** {suf}
**Fed admins:** {fd}
"""
        await m.reply_text(fmes)


async def ben(client, m, fid, user_id):
    with open(f"db/fed.txt", "r") as fr:
        fcons = json.load(fr)
    conn_chats = fcons["per_fed"][str(fid)]["chats"]

    for cb in conn_chats:
        try:
            await client.ban_chat_member(chat_id=cb,
                                         user_id=user_id)
        except:
            pass


async def unben(client, m, fid, user_id):
    with open(f"db/fed.txt", "r") as fr:
        fcons = json.load(fr)
    conn_chats = fcons["per_fed"][str(fid)]["chats"]
    for ub in conn_chats:
        try:
            await client.unban_chat_member(chat_id=ub,
                                           user_id=user_id)
        except:
            pass


@bot.on_message(filters.command(["funban", "unfban"], ['/', '!']))
async def unfban1(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        return
    else:
        user_id = m.from_user.id
        fadmin = m.from_user.mention
    if await is_admin(client, m, m.chat.id, user_id):
        with open(f"db/X{chat_id}_db.txt", 'r') as f:
            obj = json.load(f)
        if obj[f"{bot_id}"]["enable_disable"]["fban"] is not True:
            return
        with open(f"db/fed.txt", "r") as fr:
            fcons = json.load(fr)
        try:
            cfed = fcons["per_group"][str(chat_id)]
        except KeyError:
            await m.reply_text("This group doesn't have any federation connected !")
            return
        fadms = fcons['allfeds'][str(cfed)]["admins"]
    else:
        return
    if str(user_id) in fadms or int(user_id) in fed_admins:
        if " " in m.text or m.reply_to_message:
            userid = None
            statv = await return_id(client, m)
            userid = statv[0]
            reason = statv[1]
            if userid:
                if str(userid) not in fadms and int(userid) not in fed_admins:
                    mtext = m.text.markdown
                    if reason:
                        reason = reason.strip()
                    fing = await m.reply_text("`Un-Fbanning ...`", quote=False)
                    try:
                        await client.unban_chat_member(chat_id=chat_id,
                                                       user_id=userid)
                    except Exception as e:
                        await fing.edit(str(e))
                        return
                    ulink = f"[Link](tg://openmessage?user_id={userid})"
                    user = (await client.get_users(userid)).mention
                    with open(f"db/fed.txt", "r") as fr:
                        fids = json.load(fr)
                    fedname = fids['allfeds'][str(cfed)]["name"]
                    with open("db/fedbans.txt", "r") as red:
                        fbanned = json.load(red)
                    try:
                        del fbanned[str(cfed)][str(userid)]
                        fban_text = f"""
**New Un-FedBan**
**Fed:** {fedname}
**FedAdmin:** {fadmin}
**User:** {user}
**User ID:** `{userid}`
**permanent link:** {ulink}
**Reason:** {reason}              
"""
                        await fing.edit(fban_text)
                        asyncio.create_task(unben(client, m, cfed, userid))                       
                        try:
                            cid = fcons["allfeds"][str(cfed)]["log_chat"]
                            if int(chat_id) != int(cid):
                                asyncio.create_task(send_log(cid, fban_text))
                        except:
                           pass
                        with open("db/fedbans.txt", "w+") as rit:
                            json.dump(fbanned, rit, indent=4)
                        if user_id in fed_admins:
                            await bot2.send_message(-1001554911069, f"/unfban {userid} {reason}")
                        # asyncio.create_task(log_msg(client, m, cfed))
                    except Exception as e:
                        print(e)
                        await fing.edit(f"{user} was not fbanned in current federation {fedname}.")
                        return
                else:
                    await m.reply_text("He is already a fed admin !")
            else:
                await m.reply_text("User id not found !")
        else:
            await m.reply_text("Mention a user to un-fedban him !")


@bot.on_message(filters.command("setlogchat"))
async def setlog(client, m):
    chat_id = m.chat.id
#    print(m)
    if m.from_user:
        user_id = m.from_user.id
        if not await is_admin(client, m, m.chat.id, user_id):
           return
        user_id = m.from_user.id
        with open(f"db/fed.txt", "r") as fr:
            finfos = json.load(fr)
        try:
            fed_id = finfos["feds"][str(user_id)]["fed_id"]
            fname = finfos["feds"][str(user_id)]["fed_name"]
        except KeyError:
            fed_id = None
            await m.reply_text(f"You don't have a federation !")
            return                
        if fed_id:
            finfos["allfeds"][str(fed_id)]["log_chat"] = int(chat_id)
            with open("db/fed.txt", "w+") as rit:
                  json.dump(finfos, rit, indent=4)
            await m.reply_text(f"Successfully added {m.chat.title} to log group for {fname}")
        
async def send_log(chat_id: int, m: str):
    try:
       await bot.send_message(chat_id=chat_id, text=str(m))
    except Exception as e:
     #   print(chat_id, e)
        pass


  
        
async def return_id(client, m):
    user_id = None
    text = None
    if m.reply_to_message:
        if m.reply_to_message.sender_chat:
            user_id = m.reply_to_message.sender_chat.id
        else:
            user_id = m.reply_to_message.from_user.id
        if ' ' in m.text:
            text = m.text.split(' ', 1)[1]
        return user_id, text
    else:
        if ' ' in m.text:                    
            if m.entities:                          
                if len(m.entities) > 0 and str(m.text.split()[1]).startswith("@"):                    
                    uid = m.text.split()[1]
                    pid2 = await client.get_chat(uid)
                    user_id = pid2.id
                    if len(m.text.split()) > 2:              
                        text = str(m.text.split(' ', 2)[2])
                    else:
                        text = None                    
                    return user_id, text
                elif len(m.entities) > 1 and m.entities[1].type == "text_mention":
                    if m.entities[1].offset <= (len(str(m.text.split()[0])) + 2):
                        user_id = m.entities[1].user.id
                        text = m.text[(m.entities[1].offset +
                                       m.entities[1].length):]
                        if len(str(text)) < 1:
                            text = None
                    return user_id, text

                elif len(m.entities) > 1 and m.entities[1].type == "mention":
                    if m.entities[1].offset <= (len(str(m.text.split()[0])) + 2):
                        pid = m.text[(m.entities[1].offset):(
                            m.entities[1].offset + m.entities[1].length)]
                        pid2 = await client.get_chat(pid)
                        user_id = pid2.id
                        text = m.text[(m.entities[1].offset + 1 +
                                       m.entities[1].length):]
                        if len(str(text)) < 1:
                            text = None
                    return user_id, text

            
            if not user_id:
                try:
                    user_id = int(m.text.split()[1])
                    try:
                        text = m.text.split(' ', 2)[2]
                    except:
                        pass
                    return user_id, text
                except:
                    return user_id, text


async def mention_html(id, name):
  mention = f"""<a href="tg://user?id={id}">{name}</a>"""
  return mention
