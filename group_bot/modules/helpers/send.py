import os
import json
from pyrogram import *
from pyrogram.types import *
import re
from group_bot.modules.helpers.names import make_answers
from group_bot.modules.helpers.decode_btns import decode_btns
import asyncio
from pyrogram.errors import FloodWait

async def filter_helper(client, m, i, chat_id, rtm):
    text = i['text']
    if text:
        text = await make_answers(client, m, str(text))
    else:
        text = ""
    Markup = i['btn_url']
    protect = i['is_protected']
    if Markup:
        Markup = await decode_btns(Markup)
    file_id = i['file_id']
    typee = i['typee']
    disable_link_preview = i['disable_link_preview']
    if typee == 0:
        try:
            await client.send_message(chat_id=chat_id,
                                      reply_to_message_id=rtm,
                                      disable_web_page_preview=disable_link_preview,
                                      text=text,
                                      reply_markup=Markup,
                                      protect_content = protect,
                                      parse_mode=enums.ParseMode.MARKDOWN
                                      )
        except FloodWait as ee:              
                await asyncio.sleep(ee.x)
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 1:
        try:
            await client.send_sticker(chat_id=chat_id,
                                      reply_to_message_id=rtm,
                                      sticker=file_id,
                                      protect_content = protect,
                                      reply_markup=Markup)
        except FloodWait as ee:
                await asyncio.sleep(ee.x)
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 2:
        try:
            await client.send_photo(chat_id=chat_id,
                                    reply_to_message_id=rtm,
                                    photo=file_id,
                                    caption=text,
                                    protect_content = protect,
                                    reply_markup=Markup)
        except FloodWait as ee:
                await asyncio.sleep(ee.x)
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 3:
        try:
            await client.send_document(chat_id=chat_id,
                                       reply_to_message_id=rtm,
                                       document=file_id,
                                       protect_content = protect,
                                       reply_markup=Markup,
                                       caption=text,

                                       )
        except FloodWait as ee:
                await asyncio.sleep(ee.x)
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 4:
        try:
            await client.send_video(chat_id=chat_id,
                                    reply_to_message_id=rtm,
                                    video=file_id,
                                    thumb="downloads/new_photo.jpg",
                                    protect_content = protect,
                                    reply_markup=Markup,
                                    caption=text
                                    )
        except FloodWait as ee:
                await asyncio.sleep(ee.x)
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 5:
        try:
            await client.send_audio(chat_id=chat_id,
                                    reply_to_message_id=rtm,
                                    audio=file_id,
                                    reply_markup=Markup,
                                    protect_content = protect,
                                    caption=text
                                    )
        except FloodWait as ee:
                await asyncio.sleep(ee.x)
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
    elif typee == 6:
        try:
            await client.send_animation(chat_id=chat_id,
                                        reply_to_message_id=rtm,
                                        animation=file_id,
                                        reply_markup=Markup,
                                        thumb="downloads/new_photo.jpg",
                                        protect_content = protect,
                                        caption=text,
                                        )
        except FloodWait as ee:
                await asyncio.sleep(ee.x)
        except Exception as e:
            await client.send_message(text=str(e), chat_id=chat_id)
        return True
