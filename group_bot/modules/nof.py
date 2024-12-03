from pyrogram.types import *

from group_bot import bot
import re
from config import bot_id
from group_bot.modules.helpers.welcome_helper import _markup, _markup2, tescape
from group_bot.modules.helpers.names import make_answers

from group_bot.modules.admin_check import is_admin


async def noformat(client, m):
    if m.reply_to_message:
        if m.sender_chat:
            user_id = m.sender_chat.id
        else:
            user_id = m.from_user.id
        if await is_admin(client, m, m.chat.id, user_id) is True:
            btns = ""
            rtx = ""
            if m.reply_to_message and m.reply_to_message.reply_markup:
                msg = m.reply_to_message.reply_markup
                yio = len(
                    m.reply_to_message.reply_markup['inline_keyboard']) + 2
                i = 0
                while i < yio:
                    dash = []
                    try:
                        hm1 = msg['inline_keyboard'][i][0]['text']
                        hm2 = msg['inline_keyboard'][i][0]['url']
                        btns += f"""[{hm1}](buttonurl://{hm2})"""
                        leny = len(msg['inline_keyboard'][i])
                        j = 1
                        while j < leny:
                            hm11 = msg['inline_keyboard'][i][j]['text']
                            hm21 = msg['inline_keyboard'][i][j]['url']
                            btns += f"""[{hm11}](buttonurl://{hm21}:same)"""
                            j += 1
                        i += 1
                    except Exception as e:
                        i += 1

            if m.reply_to_message.text:
                rtx = m.reply_to_message.text.markdown
            elif m.reply_to_message.caption:
                rtx = m.reply_to_message.caption.markdown

            await m.reply_text(f"{rtx}\n\n{btns}", parse_mode=pyrogram.enums.ParseMode.DISABLED)
