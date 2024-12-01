import os
import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, User
from pyrogram.errors import UserNotParticipant
from group_bot.modules.admin_check import is_admin
from group_bot.modules.give_id import return_id
from config import *
from group_bot import bot
import json

# @bot.on_message(filters.command(["whois", "info"], ['/','!']))


async def info(client: Client, message: Message):
    """ extract user information """
    chat_id = message.chat.id
    with open(f"db/X{chat_id}_db.txt", 'r') as f:
        obj = json.load(f)
    if obj[f"{bot_id}"]["enable_disable"]["info"] is not True:
        return
    status_message = await message.reply_text("`Gathering infos ..`")
    from_user = None
    from_user_id = (await return_id(client, message))[0]
    try:
        from_user = await client.get_chat(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("no valid user_id / message specified")
        return

    first_name = from_user.first_name or ""
    username = from_user.username or ""

    message_out_str = (
        "<b>Name:</b> "
        f"<a href='tg://user?id={from_user.id}'>{first_name}</a>\n"
        f"<b>Username:</b> @{username}\n"
        f"<b>User ID:</b> <code>{from_user.id}</code>\n"

    )
    message_out_str += (
        f"<b>User Link:</b> {from_user.mention}\n"
        if isinstance(from_user, User) and from_user.username
        else ""
    )

    if isinstance(from_user, User) and message.chat.type in ["supergroup", "channel"]:
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += "<b>Joined on:</b> <code>" f"{joined_date}" "</code>\n"
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo

    if chat_photo:
        local_user_photo = await client.download_media(message=chat_photo.big_file_id)
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            caption=message_out_str,
            disable_notification=True,
        )
        os.remove(local_user_photo)
    else:
        try:
            await message.reply_text(
            text=message_out_str, quote=True, disable_notification=True, parse_mode="html"
                  )
        except:
             pass
    await status_message.delete()
