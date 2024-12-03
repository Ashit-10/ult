from pyrogram import Client
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from group_bot import bot
from group_bot.modules.admin_check import is_admin


@bot.on_inline_query()
async def ianswer(client, inline_query):    
    if inline_query.query == "?xy":
        await inline_query.answer(
            results=[InlineQueryResultArticle(
                title="Xy problem",
                input_message_content=InputTextMessageContent(disable_web_page_preview=True,
                                                              message_text=f"Hey. What exactly do you want this for? This seems like an [xy-problem](https://xyproblem.info/) to me."
                                                              ),
                description="Xy problem !",
            )],
            cache_time=1
        )

    elif inline_query.query == "?how":
        await inline_query.answer(
            results=[InlineQueryResultArticle(
                title="how to send Request apks",
                input_message_content=InputTextMessageContent(disable_web_page_preview=True,
                                                              message_text=f"Hey, It's actually so much easy to find both apks !\n-`MiuiSystemUI.apk` and \n-`AndroidDevicesOverlay.apk`.\n\nUse any Root-explorer ([mt-manager](http://t.me/The_Ultron_Robot?start=-1001542320014_NOTES_mt_manager) recommend) and follow the below guide video !"
                                                              ),
                description="how to send Request apks",
                reply_markup=InlineKeyboardMarkup(
                     [
                         [InlineKeyboardButton(
                             "Guide video !",
                             url="http://t.me/The_Ultron_Robot?start=-1001542320014_NOTES_how_to_send_apk"
                         )]
                     ]
                     )
            )],
            cache_time=1
        )

    elif inline_query.query == "!miui":
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="dualstatusbar for miui",
                    input_message_content=InputTextMessageContent(
                        "Here's how to get Dualstatusbar for any miui rom !"
                    ),
                    url="t.me/dualstatusbar",
                    description="How to get dualstatusbar for miui",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                             "miui dualstatusbar group !",
                             url="t.me/miuidsb_support"
                             )]
                        ]
                    )
                )],
            cache_time=2
        )
    elif inline_query.query == "!aosp":
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="dualstatusbar",
                    input_message_content=InputTextMessageContent(
                        "Here's how to get Dualstatusbar for any rom !"
                    ),
                    url="t.me/dualstatusbar",
                    description="How to get dualstatusbar",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                             "join dualstatusbar !",
                             url="t.me/dualstatusbar"
                             )]
                        ]
                    )
                )],
            cache_time=2
        )
    elif "!nou" in inline_query.query:
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="nouvelle support",
                    input_message_content=InputTextMessageContent(
                        "Nouvelle substratum support group !"
                    ),
                    url="t.me/nouvelle_support",
                    description="Nouvelle substratum support group",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                             "join nouvelle !",
                             url="t.me/nouvelle_support"
                             )]
                        ]
                    )
                )],
            cache_time=2
        )
    elif len(str(inline_query.query)) > 1:
        text = str(inline_query.query)
        if '+device' in text or text == '+device':
            text = text.replace(
                "+device", 'missing device name (NOT codename)')
        if '+name' in text or text == "+name":
            text = text.replace("+name", 'missing rom name')
        if '+version' in text or text == "+version":
            text = text.replace("+version", 'missing rom version')
        if '+date' in text or text == '+date':
            text = text.replace("+date", "missing build date of your rom")
        if '+ui' in text or text == '+ui':
            text = text.replace("+ui", "missing SystemUI.apk")
        if '+mui' in text or text == '+mui':
            text = text.replace("+mui", "missing MiuiSystemUI.apk")
        if '+v' in text or text == "+v":
            text = text.replace(
                "+v", """Please share us a screenshot of the "v" menu from Addons (the one to "view installed mods")""")

        await inline_query.answer(
            results=[InlineQueryResultArticle(
                title="something is missing !",
                input_message_content=InputTextMessageContent(disable_web_page_preview=True,
                                                              message_text=f"{text}"
                                                              ),
                description="missing parts -_- !!",
            )],
            cache_time=1
        )
