from group_bot import bot
from pyrogram import *
from pyrogram.types import *
from config import *
import json
from group_bot.modules.helpers.db import create_db
from group_bot.modules.helpers.decode_btns import decode_btns
from group_bot.modules.helpers.filter_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.notes import group_notes, private_notes
from group_bot.modules.admin_check import is_admin, immutable, can_restrict, can_delete

locks_list = ["invite_link", "sticker", "gif", "document", "photo", "video", "audio", "poll", "contact",
             "anon_channel", "media", "forward_from_channel", "forward_from_user", "all"]


async def locks(client, m, obj):

    stickers = obj[f"{bot_id}"]["locks"]["sticker"]
    gifs = obj[f"{bot_id}"]["locks"]["gif"]
    photo = obj[f"{bot_id}"]["locks"]["photo"]
    video = obj[f"{bot_id}"]["locks"]["video"]
    audio = obj[f"{bot_id}"]["locks"]["audio"]
    media = obj[f"{bot_id}"]["locks"]["media"]
    document = obj[f"{bot_id}"]["locks"]["document"]
    poll = obj[f"{bot_id}"]["locks"]["poll"]
    location = obj[f"{bot_id}"]["locks"]["location"]
    contact = obj[f"{bot_id}"]["locks"]["contact"]

    invite_link = obj[f"{bot_id}"]["locks"]["invite_link"]
    lock_forward_channel = obj[f"{bot_id}"]['locks']["forward_from_channel"]
    lock_forward_user = obj[f"{bot_id}"]['locks']["forward_from_user"]
    anon_channel = obj[f"{bot_id}"]["locks"]["anon_channel"]
    approvers = obj[f"{bot_id}"]["approved_channels_and_users"]

    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await immutable(client, m, m.chat.id, user_id) is not True:
     # group/chat LINK detection
        try:
            # forward from channel
            if m.forward_from_chat and lock_forward_channel is True:
                await m.delete()
            if m.sender_chat and anon_channel is True:
                await m.delete()
            if m.forward_from and lock_forward_user is True:
                await m.delete()
            if invite_link is True:
                if m.text or m.caption:
                    if m.text:
                        txt = m.text
                    elif m.caption:
                        txt = m.caption
                    if "t.me/" in txt.markdown.lower():
                        await m.delete()
                    spam_group = None
                    if m.entities:
                        for ih in m.entities:
                            if ih.type == "mention":
                                if ih.offset != 0:
                                    mt = str(m.text)[ih.offset:(
                                        ih.offset + ih.length)]
                                else:
                                    mt = str(m.text)[:ih.length]
                                if mt.startswith('@'):
                                    print(mt)
                                    ksk = await client.get_chat(mt)
                                    if ksk.type == "supergroup" or ksk.type == "channel":
                                        spam_group = True
                                        break
                        if spam_group:
                            await m.delete()

    # stickers
            if m.document and document:
                size = int(m.document.file_size) / 1024
                but_size = obj[f"{bot_id}"]["lock_sizes"]["document"]                
                if int(size) > int(but_size):
                    print("y")
                    await m.delete()
                elif int(but_size) == 0:
                    print("f")
                    await m.delete()
                    
            if m.video and video:
                size = int(m.video.file_size) / 1024
                but_size = obj[f"{bot_id}"]["lock_sizes"]["video"]
                if int(size) > int(but_size):
                    await m.delete()
                elif int(but_size) == 0:
                    await m.delete()        
           
            if m.sticker and stickers:
                await m.delete()
            if m.animation and gifs:
                await m.delete()
            if m.contact and contact:
                await m.delete()
            if m.location and location:
                await m.delete()
            if m.poll and poll:
                await m.delete()
            
        except Exception as wtf:
            print(f"Error in Locks:\n{wtf}")

async def lock_sizes(client, m):
    chat_id = m.chat.id    
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["locks"] is not True:
        return
    if await can_delete(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_DELETE_MESSAGES]")
        return
    if await can_restrict(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_RESTRICT_MESSAGES]")
        return
    if " " in m.text:
        wat = m.command[1]
        if wat.lower() in ['document', 'media', 'video']:
           wat = wat.lower()           
           try:
              size = str(m.command[2])
           except:
               await m.reply_text("You have to specific size too followed by `kb` or `mb` !")
               return
           if len(str(size)) > 2:
               isize = size[:-2]                                 
           else:
               await m.reply_text("You haven't entered values in correct way !\nEg: `69kb` or `69mb` !")
               return          
           main_size = 0
           try:
               asize = int(isize)         
               if "kb" in str(size).lower():                 
                   main_size = asize * 1024
                   sss = f"{asize} Kb"
               elif "mb" in str(size).lower():
                   main_size = asize * 1024 * 1024       
                   sss = f"{asize} Mb"        
           except:
                await m.reply_text("You have to specific size in integer followed by `kb` or `mb` !")
                return
           if wat == "media":
                obj[f"{bot_id}"]["lock_sizes"]["document"] = int(main_size)
                obj[f"{bot_id}"]["lock_sizes"]["video"] = int(main_size)
           else:
                obj[f"{bot_id}"]["lock_sizes"][str(wat)] = int(main_size)
           with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
               json.dump(obj, rf, indent=4)
           
           await m.reply_text(f"Successfully added max __{wat}__ size to __{sss}__ ! ")
           
async def lock(client, m):
    chat_id = m.chat.id    
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["locks"] is not True:
        return
    if await can_delete(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_DELETE_MESSAGES]")
        return
    if await can_restrict(client, m, m.chat.id, user_id) is not True:
        await m.reply_text("You don't have sufficient permissions; caused by [CAN_RESTRICT_MESSAGES]")
        return
    if " " in m.text:
        strn = ""
        astrn = ""
        alperms = m.chat.permissions
        texts = str(m.command)
        for yg in locks_list:
            if yg in texts:            
                if obj[f"{bot_id}"]['locks'][f"{yg}"]:
                    astrn += f"`{yg}`, "
                else:
                    print(yg)
                    obj[f"{bot_id}"]['locks'][f"{yg}"] = True
                    strn += f"`{yg}`, "
        if "all" in texts:
            if (alperms.can_send_messages is False
                and alperms.can_send_media_messages is False
                and alperms.can_send_other_messages is False
                and alperms.can_send_polls is False
                and alperms.can_add_web_page_previews is False
                and alperms.can_change_info is False
                    and alperms.can_pin_messages is False):
                await m.reply_text("Everything was already locked !")
                return
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=False,
                        can_send_media_messages=False,
                        can_send_other_messages=False,
                        can_add_web_page_previews=False,
                        can_invite_users=False,
                        can_send_polls=False,
                        can_change_info=False,
                        can_pin_messages=False))
                with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
                    json.dump(obj, rf, indent=4)
                await m.reply_text("Locked `all` !")
                return
        if "media" in texts:
            if (alperms.can_send_media_messages is False):
                pass
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=alperms.can_send_messages,
                        can_send_media_messages=False,
                        can_send_other_messages=alperms.can_send_other_messages,
                        can_add_web_page_previews=alperms.can_add_web_page_previews,
                        can_invite_users=alperms.can_invite_users,
                        can_send_polls=alperms.can_send_polls,
                        can_change_info=alperms.can_change_info,
                        can_pin_messages=alperms.can_pin_messages))
        if "sticker" and "gif" in texts:
            if alperms.can_send_other_messages is False:
                pass
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=alperms.can_send_messages,
                        can_send_media_messages=alperms.can_send_media_messages,
                        can_send_other_messages=False,
                        can_add_web_page_previews=alperms.can_add_web_page_previews,
                        can_invite_users=alperms.can_invite_users,
                        can_send_polls=alperms.can_send_polls,
                        can_change_info=alperms.can_change_info,
                        can_pin_messages=alperms.can_pin_messages))
        if "poll" in texts:
            if alperms.can_send_other_messages is False:
                pass
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=alperms.can_send_messages,
                        can_send_media_messages=alperms.can_send_media_messages,
                        can_send_other_messages=alperms.can_send_other_messages,
                        can_send_polls=False,
                        can_add_web_page_previews=alperms.can_add_web_page_previews,
                        can_invite_users=alperms.can_invite_users,
                        can_change_info=alperms.can_change_info,
                        can_pin_messages=alperms.can_pin_messages))
        with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
            json.dump(obj, rf, indent=4)
        if not len(astrn) < 1:
            astrn = f"{astrn[:-2]} already locked !"
        if not len(strn) < 1:
            strn = f"{strn[:-2]} have been locked !"
        main_str = f"{astrn}\n{strn}"
        if len(main_str) < 3:
            main_str = "This isn't a valid lock-able parameter"
        await m.reply_text(main_str)
    else:
        await m.reply_text("No locks action specified !")


async def unlock(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["locks"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is not True:
        return
    if " " in m.text:
        strn = ""
        astrn = ""
        alperms = m.chat.permissions
      #  print(alperms)
        texts = str(m.command)
        for yg in locks_list:
            if yg in texts:
                if obj[f"{bot_id}"]['locks'][f"{yg}"] is False:
                    astrn += f"`{yg}`, "
                else:
                    obj[f"{bot_id}"]['locks'][f"{yg}"] = False
                    strn += f"`{yg}`, "
        if "all" in texts:
            if (alperms.can_send_messages is True
                    and alperms.can_send_media_messages is True
                    and alperms.can_send_other_messages is True
                    and alperms.can_send_polls is True
                    ):
                await m.reply_text("Everything was already unlocked !")
                return
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True,
                        can_send_polls=True,
                        can_invite_users =True,
                        can_change_info=True,
                        can_pin_messages=True))
                await m.reply_text("Unlocked `all` !")
                return
        if ("media" in texts):
            if (alperms.can_send_media_messages is True):
                pass
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=alperms.can_send_messages,
                        can_send_media_messages=True,
                        can_send_other_messages=alperms.can_send_other_messages,
                        can_add_web_page_previews=alperms.can_add_web_page_previews,
                        can_send_polls=alperms.can_send_polls,
                        can_invite_users =alperms.can_invite_users,
                        can_change_info=alperms.can_change_info,
                        can_pin_messages=alperms.can_pin_messages))
        if "sticker" and "gif" in texts:
            if alperms.can_send_other_messages is True:
                pass
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=alperms.can_send_messages,
                        can_send_media_messages=alperms.can_send_media_messages,
                        can_send_other_messages=True,
                        can_add_web_page_previews=alperms.can_add_web_page_previews,
                        can_send_polls=alperms.can_send_polls,
                        can_invite_users =alperms.can_invite_users,
                        can_change_info=alperms.can_change_info,
                        can_pin_messages=alperms.can_pin_messages))
        if "poll" in texts:
            if alperms.can_send_other_messages is True:
                pass
            else:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=alperms.can_send_messages,
                        can_send_media_messages=alperms.can_send_media_messages,
                        can_send_other_messages=alperms.can_send_other_messages,
                        can_send_polls=True,
                        can_add_web_page_previews=alperms.can_add_web_page_previews,
                        can_invite_users=alperms.can_invite_users,
                        can_change_info=alperms.can_change_info,
                        can_pin_messages=alperms.can_pin_messages))
        with open(f"db/X{chat_id}_db.txt", 'w+') as rf:
            json.dump(obj, rf, indent=4)
        if not len(astrn) < 1:
            astrn = f"{astrn[:-2]} wasn't locked !"
        if not len(strn) < 1:
            strn = f"{strn[:-2]} have been unlocked !"
        main_str = f"{astrn}\n{strn}"
        if len(main_str) < 1:
            main_str = "This isn't a valid lock-able parameter"
        await m.reply_text(main_str)
    else:
        await m.reply_text("No unlock action specified !")


async def locked(client, m):
    chat_id = m.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["locks"] is not True:
        return
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if await is_admin(client, m, m.chat.id, user_id) is True:
        locked = obj[f"{bot_id}"]["locks"]
        chat = m.chat.title
        lockstr = "\n".join(f"- `{i}`" for i in locked if locked[i] is True)
        if len(lockstr) < 1:
            lockstr = f"No permissions are Locked in `{chat}`."
        else:
            lockstr = f"Following permissions are Locked in `{chat}`:\n{lockstr}"
        await m.reply_text(str(lockstr))




