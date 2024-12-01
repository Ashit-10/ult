import json
import os
from config import *


def create_db(chat_id):
    if not os.path.isfile(f"db/X{chat_id}_db.txt"):
        try:
            obj = {
                f"{bot_id}": {
                    "advancedblocklist": [],
                    "approved_channels_and_users": [],
                    "blocklist": [],
                    "chat_members": [],
                    "dont_mention_admins": [],
                    "enable_disable": {
                        "ablocklists": True,
                        "antiflood": True,
                        "approve": True,
                        "ban": True,
                        "blocklists": True,
                        "fban": False,
                        "filters": True,
                        "id": True,
                        "info": True,
                        "greetings": True,
                        "kick": True,
                        "locks": True,
                        "mute": True,
                        "notes": True,
                        "nsfw_check": True,
                        "pin_unpin": True,
                        "ping": True,
                        "promote_demote": True,
                        "purge": True,
                        "raid": True,
                        "sg": False,
                        "report": True,
                        "rules": True,
                        "warn": True
                    },
                    "filters": {
                        "filters": []
                    },
                    "raid": {
                        "status": "off",
                        "started_time": 0,
                        "duration": "6h",
                        "kick_for": "1h"
                    },
                    "captchamode": "text",
                    "flood": {
                        "action": "tmute 2h",
                        "messages": 5
                    },
                    "goodbye": [
                        {
                            "btn_url": None,
                            "disable_link_preview": True,
                            "file_id": None,
                            "text": "Nice knowing you !",
                            "typee": 0,
                            "is_protected": False
                        }
                    ],
                    "locks": {
                        "all": False,
                        "contact": False,
                        "document": False,
                        "sticker": False,
                        "gif": False,
                        "photo": False,
                        "poll": False,
                        "location": False,
                        "video": False,
                        "audio": False,
                        "media": False,
                        "anon_channel": False,
                        "forward_from_channel": True,
                        "forward_from_user": False,
                        "invite_link": False
                    },
                    "lock_sizes": {
                        "document": 0,
                        "video": 0,                   
                    },
                    "max_warns": 3,
                    "notes": [],
                    "pass_words": [],
                    "on_off": {
                        "antichannelpin": False,
                        "antiservice": False,
                        "captcha": False,
                        "cleanwelcome": False,
                        "lang_detect": False,
                        "private_notes": False,
                        "privaterules": False,
                        "captcharules": False,
                        "captchakick": False,
                        "noteshash": True
                    },
                    "rules": None,
                    "warn_action": "kick",
                    "welcome": [
                        {
                            "btn_url": None,
                            "disable_link_preview": True,
                            "file_id": None,
                            "text": "Hey {mention} !\nWelcome to {group} . Have a nice day :)",
                            "typee": 0
                        }
                    ],
                    "2nd_welcome": [
                        {
                            "btn_url": None,
                            "disable_link_preview": True,
                            "file_id": None,
                            "text": "Hey {mention} !\nWelcome to {group} . Have a nice day :)",
                            "typee": 0
                        }
                    ]
                }
            }

            with open(f"db/X{chat_id}_db.txt", 'w+') as f:
                json.dump(obj, f, indent=4, sort_keys=True)
        except Exception as e:
            print(e)
