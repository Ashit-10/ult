from pyrogram import Client, filters
from group_bot import bot
from pyrogram.types import *
from group_bot.modules.admin_check import is_admin, can_delete, can_restrict, adminlist
import time
import json

helpKey = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=f"Admin",
            callback_data=f"ADMINSCMD_HELP"),
         InlineKeyboardButton(
            text=f"Antiflood",
            callback_data=f"ANTIFLOOD_HELP"),
         InlineKeyboardButton(
            text=f"Antiraid",
            callback_data=f"ANTIRAID_HELP")],
[InlineKeyboardButton(
            text=f"Afk",
            callback_data=f"AFK_HELP"),
         InlineKeyboardButton(
            text=f"Filters",
            callback_data=f"FILTER_HELP"),
         InlineKeyboardButton(
            text=f"Anti things",
            callback_data=f"ANTI_HELP")],
            
        [InlineKeyboardButton(
            text=f"Approval",
            callback_data=f"APPROVAL_HELP"),
         InlineKeyboardButton(
            text=f"Bans",
            callback_data=f"BANS_HELP"),
         InlineKeyboardButton(
            text=f"Blocklists",
            callback_data=f"BLOCKLIST_HELP")],
                    

        [InlineKeyboardButton(
            text=f"Captcha",
            callback_data=f"CAPTCHA_HELP"),
         InlineKeyboardButton(
            text=f"Disable/enable",
            callback_data=f"EN_DIS_ABLE_HELP"),
         InlineKeyboardButton(
            text=f"Federations",
            callback_data=f"FED_HELP")
         ],

         [InlineKeyboardButton(
            text=f"Greetings",
            callback_data=f"GREETING_HELP"),
         InlineKeyboardButton(
            text=f"Import/Export",
            callback_data=f"IMPORT_EXPORT_HELP"),
         InlineKeyboardButton(
            text=f"Locks",
            callback_data=f"LOCKS_HELP")
         ],

         [InlineKeyboardButton(
            text=f"Misc",
            callback_data=f"MISC_HELP"),
         InlineKeyboardButton(
            text=f"pin",
            callback_data=f"PIN_UNPIN_HELP"),
         InlineKeyboardButton(
            text=f"Purges",
            callback_data=f"PURGE_HELP")
         ],
         [InlineKeyboardButton(
            text=f"Reports",
            callback_data=f"REPORT_HELP"),
         InlineKeyboardButton(
            text=f"Rules",
            callback_data=f"RULES_HELP"),
         InlineKeyboardButton(
            text=f"Warnings",
            callback_data=f"WARNING_HELP")
         ],
                  [InlineKeyboardButton(
            text=f"Translation",
            callback_data=f"TR_HELP")]
    ])

@bot.on_message(filters.command('help') & ~filters.private)
async def helpp(client, m):
    chat_id = m.chat.id
    if m.sender_chat:
        user_id = m.sender_chat.id
    else:
        user_id = m.from_user.id
    if not await is_admin(client, m, chat_id, user_id):
        return
    await m.reply("""**HELP MENU**
This is just an on-point lists for all functions, all commands can be used with '/' and '!' .

--To mention users in messages you can write: --
`{id}` : user's id,
`{first}` : first name of user,
`{last}` : last name of user,
`{mention}` : mentioned a user,
`{username}` : username of user,
`{group}` : name of the group.

**All commands can be only used in groups.**
""", reply_markup=helpKey)




