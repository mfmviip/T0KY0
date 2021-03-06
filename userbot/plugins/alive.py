import time
from platform import python_version

from telethon import version

from . import ALIVE_NAME, StartTime, catversion, get_readable_time, mention, reply_id

DEFAULTUSER = ALIVE_NAME or "cat"
CAT_IMG = Config.ALIVE_PIC or "https://telegra.ph/file/967209504b62689f5f770.jpg"
CUSTOM_ALIVE_TEXT = Config.CUSTOM_ALIVE_TEXT or "๐๐ค๐ช๐ง๐๐ ๐๐ค๐ ๐๐ค โ"
EMOJI = Config.CUSTOM_ALIVE_EMOJI or "  โ โซ โซ"


@bot.on(admin_cmd(outgoing=True, pattern="ูุญุต$"))
@bot.on(sudo_cmd(pattern="ูุญุต$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = await reply_id(alive)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if CAT_IMG:
        cat_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        cat_caption += f"ูดโถโโโโโโบแดแดแดสแดโปโโโโโโท\n"
        cat_caption += f"**{EMOJI} ูุงุนุฏุฉ ุงูุจูุงูุงุช :** `{check_sgnirts}`\n"
        cat_caption += f"**{EMOJI} ุงุตุฏุงุฑ ุงูุชููุซูู  :** `{version.__version__}\n`"
        cat_caption += f"**{EMOJI} ุงุตุฏุงุฑ ุณูุงู :** `{catversion}`\n"
        cat_caption += f"**{EMOJI} ุงุตุฏุงุฑ ุงูุจุงูุซูู :** `{python_version()}\n`"
        cat_caption += f"**{EMOJI} ูุฏุฉ ุงูุชุดุบูู :** `{uptime}\n`"
        cat_caption += f"**{EMOJI} ุงููุณุชุฎุฏู:** {mention}\n"
        cat_caption += f"**{EMOJI}**  **[๐๐ค๐ช๐ง๐๐ ๐๐ค๐ ๐๐ค]**(t.me/TOKYO_TEAM)  ๐ฐ .\n"
        cat_caption += f"**{EMOJI}**  **[๐๐๐๐๐ผ๐๐ผ]**(t.me/MFMVIP)  ๐ฐ .\n"
        cat_caption += f"ูดโถโโโโโโบแดแดแดสแดโปโโโโโโท\n"
        await alive.client.send_file(
            alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id
        )
        await alive.delete()
    else:
        await edit_or_reply(
            alive,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{EMOJI} ูุงุนุฏุฉ ุงูุจูุงูุงุช :** `{check_sgnirts}`\n"
            f"**{EMOJI} ุงุตุฏุงุฑ ุงูุชููุซูู :** `{version.__version__}\n`"
            f"**{EMOJI} ุงุตุฏุงุฑ ุณูุงู :** `{catversion}`\n"
            f"**{EMOJI} ุงุตุฏุงุฑ ุงูุจุงูุซูู :** `{python_version()}\n`"
            f"**{EMOJI} ูุฏุฉ ุงูุชุดุบูู :** `{uptime}\n`"
            f"**{EMOJI} ุงููุณุชุฎุฏู:** {mention}\n",
        )


@bot.on(admin_cmd(outgoing=True, pattern="ialive$"))
@bot.on(sudo_cmd(pattern="ialive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    reply_to_id = await reply_id(alive)
    cat_caption = f"**Catuserbot is Up and Running**\n"
    cat_caption += f"**  -Telethon version :** `{version.__version__}\n`"
    cat_caption += f"**  -Catuserbot Version :** `{catversion}`\n"
    cat_caption += f"**  -Python Version :** `{python_version()}\n`"
    cat_caption += f"**  -Master:** {mention}\n"
    results = await bot.inline_query(tgbotusername, cat_caption)  # pylint:disable=E0602
    await results[0].click(alive.chat_id, reply_to=reply_to_id, hide_via=True)
    await alive.delete()


# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
# 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
# เดตเดฟเดตเดฐเดฃเด เดเดเดฟเดเตเดเตเดฎเดพเดฑเตเดฑเดฟเดเตเดเตเดฃเตเดเต เดชเตเดเตเดจเตเดจเดตเตผ
# เดเตเดฐเตเดกเดฟเดฑเตเดฑเต เดตเตเดเตเดเดพเตฝ เดธเดจเตเดคเตเดทเดฎเต เดเดณเตเดณเต..!
# uniborg


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "ูู ูุชู ุชุนููู ูุงุนุฏุฉ ุจูุงูุงุช"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"โ {str(e)}"
        is_database_working = False
    else:
        output = "ุชุนูู ุจูุฌุงุญ โ"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update(
    {
        "alive": "**Plugin :** `alive`\
      \n\n  โข  **Syntax : **`.alive` \
      \n  โข  **Function : **__status of bot will be showed__\
      \n\n  โข  **Syntax : **`.ialive` \
      \n  โข  **Function : **__inline status of bot will be shown.__\
      \nSet `ALIVE_PIC` var for media in alive message"
    }
)
