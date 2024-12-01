import json
from group_bot import bot
from pyrogram import Client, filters
from googletrans import Translator
import re
from group_bot.modules.admin_check import is_admin_sync as is_admin

translator = Translator()




def trt(client, m):   
   chat_id = m.chat.id
   if m.sender_chat:
        user_id = m.sender_chat.id
   else:
        user_id = m.from_user.id
   if not is_admin(client, m, m.chat.id, user_id):
       return
   if m.text and m.reply_to_message:
       if " " in m.text:
           try:             
              oke = m.reply_text("`Processing..`")
              lang_code = str(m.command[1])   
              if m.reply_to_message.text:
                  input_text = str(m.reply_to_message.text)
              elif m.reply_to_message.caption:
                  input_text = str(m.reply_to_message.caption)
              elif not m.reply_to_message.text and not m.reply_to_message.caption:
                  oke.edit("Reply to texts or captions to translate !")
                  return
              result = translator.translate(input_text, dest=lang_code)
              # print(result.src)
              with open("lang_codes.txt", "r") as red:
                  langs = json.load(red)
              try:
                  lang_name = langs[lang_code]
                  try:            
                      from_lang_name = langs[str(result.src).lower()]                  
                  except KeyError:
                      from_lang_name = "unknown lang"
              finally:
                  translated_text = result.text
                  print(translated_text)
                  original_text = result.origin
                  if "dsb" in original_text.lower():                  
                     translated_text = re.sub("etc", "DSB", translated_text, re.IGNORECASE)                     
                  oke.edit(f"**__--Translated {from_lang_name} to {lang_name}:--__**\n`{translated_text}`")
           except ValueError:               
               oke.edit("Enter a valid lang code !\n/getlangs to get list of all language codes .")
           except Exception as wat:
               oke.edit(str(wat))
       else:
           m.reply_text("You need to give language code too !")
   else:
       m.reply_text("Reply to text or captions to translate it !")



def langs(client, m):   
    try:
       m.reply_document("lang_codes.txt")
    except Exception as e:
       m.reply_text(str(e))
       
