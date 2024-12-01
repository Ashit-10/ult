from pyrogram import *
from pyrogram.types import *
import re


async def decode_btns(k):
    act_btn = []
    ptrn = re.compile(r'\[(.*?)\]\((.*?)\)')
    ptn = ptrn.finditer(k)
    bln = []
    for y in ptn:
        bln2 = []
        qw = y.group(0)
        btn = qw.split('](buttonurl://')[0][1:]
        link = qw.split('](buttonurl://')[1][:-1]
        if ':same' in link:
            link = link.replace(':same', '')
            bln.append(InlineKeyboardButton(text=f"{btn}", url=f"{link}"))
        else:
            if not len(str(bln)) < 3:
                act_btn.append(bln)
            bln = []
            bln.append(InlineKeyboardButton(text=f"{btn}", url=f"{link}"))
    act_btn.append(bln)
    markup = InlineKeyboardMarkup(act_btn)
    return markup
