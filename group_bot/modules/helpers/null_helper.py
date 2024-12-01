import os
import json
from pyrogram import *
from pyrogram.types import *
import re
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.helpers.decode_btns import decode_btns
from config import *
import random
import string


async def null_sender(client, m, i, chat_id):
    text = i['text']
    if not text:
        text = ""
    Markup = i['btn_url']
    if Markup:
        text += f"\n\n{Markup}"
    file_id = i['file_id']
    typee = i['typee']
    disable_link_preview = i['disable_link_preview']
    if typee == 0:
        try:
            await client.send_message(chat_id=chat_id,
                                      parse_mode=None,
                                      disable_web_page_preview=disable_link_preview,
                                      text=text,
                                      )

        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 1:
        try:
            await client.send_sticker(chat_id=chat_id,
                                      sticker=file_id,
                                      )

        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 2:
        try:
            await client.send_photo(chat_id=chat_id,
                                    photo=file_id,
                                    caption=text,
                                    parse_mode=None,
                                    )

        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 3:
        try:
            await client.send_document(chat_id=chat_id,
                                       document=file_id,
                                       caption=text,
                                       parse_mode=None
                                       )

        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 4:
        try:
            await client.send_video(chat_id=chat_id,
                                    video=file_id,
                                    caption=text,
                                    parse_mode=None
                                    )

        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 5:
        try:
            await client.send_audio(chat_id=chat_id,
                                    audio=file_id,
                                    caption=text,
                                    parse_mode=None
                                    )

        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 6:
        try:
            await client.send_animation(chat_id=chat_id,
                                        animation=file_id,
                                        caption=text,
                                        parse_mode=None
                                        )

        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
