from pyrogram import Client, filters
from group_bot import bot
import requests
import json
import os
import random, string
import asyncio
#from group_bot.modules.admin_check import is_admin
users = [809293242, 19371046, 319956169, 740538095, 1845525834, 1602293216]

#@bot.on_message(filters.command(["check"]) & ~filters.edited)
def nchek(client, m):
   if m.from_user:
      if m.from_user.id in users:          
          if m.reply_to_message.photo or m.reply_to_message.sticker:
              aws = m.reply_text("`Processing...`")
              req3(client, m, aws)


def req3(client, m, aws):
   try:
     mt = ''.join(random.sample(string.ascii_uppercase, 6))
     client.download_media(m.reply_to_message, file_name=f"downloads/{mt}.jpg")
   except Exception as rf:
      aws.edit(str+rf)
      return
     
   params = {
   'models': 'nudity',
  'api_user': '1259479556',
  'api_secret': '9f3nsyfMmJMcUB5fnU6p'
}
   files = {'media': open(f'downloads/{mt}.jpg', 'rb')}
   try:
      r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params) 
      ees = json.loads(r.text)
   except:
      aws.edit("Error due to unexpected file format !")
      return
   try:
       afe = ees["nudity"]
       raw = float(ees["nudity"]["raw"]) * 100
       safe = float(ees["nudity"]["safe"]) * 100
       par = float(ees["nudity"]["partial"]) * 100
   except KeyError:
       aws.edit("Error..")
       return
   try:
      aws.edit(f"""--NSFW RESULT:--
**Raw nudity:** `{raw}%`
**Partially nudity:** `{int(par)}%`
**Safe:** `{int(safe)}%`
""")   
   except Exception as ed:
       aws.edit(str(ed))
   finally:
       os.remove(f"downloads/{mt}.jpg")


