import time

from . import StartTime, get_readable_time, reply_id

DEFAULTUSER = "ππ€π ππ€ΛΌΰΌΰΏ"
CAT_IMG = "https://telegra.ph/file/967209504b62689f5f770.jpg"
CUSTOM_ALIVE_TEXT = "π© ππ€πͺπ§ππ-ΛΉππ€π ππ€ΛΌΰΌΰΏ - π«π¬π½π¬π³πΆπ·π¬πΉ πͺ"
EMOJI = "  πβ  "


@bot.on(admin_cmd(outgoing=True, pattern="ΩΨ΅Ψ·ΩΩ$"))
@bot.on(sudo_cmd(pattern="ΩΨ΅Ψ·ΩΩ$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = await reply_id(alive)
    await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if CAT_IMG:
        cat_caption = f"**{CUSTOM_ALIVE_TEXT}**\n"
        cat_caption += f"Ω΄βΆββββββΊα΄α΄α΄Κα΄β»ββββββ·\n"
        cat_caption += f"**{EMOJI}** π«π¬π½ πΌπΊπ¬πΉ β¬ @MFMVIP ΰΌ\n"
        cat_caption += f"**{EMOJI}** π«π¬π½ π°π« β¬ 911945965 ΰΌ\n"
        cat_caption += f"Ω΄βΆββββββΊα΄α΄α΄Κα΄β»ββββββ·"
        await alive.client.send_file(
            alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id
        )
        await alive.delete()
    else:
        await edit_or_reply(
            alive,
            f"**{CUSTOM_ALIVE_TEXT}**\n"
            f"Ω΄βΆββββββΊα΄α΄α΄Κα΄β»ββββββ·\n"
            f"**{EMOJI}** π«π¬π½ πΌπΊπ¬πΉ β¬ @MFMVIP ΰΌ\n"
            f"**{EMOJI}** π«π¬π½ π°π« β¬ 911945965 ΰΌ\n"
            f"Ω΄βΆββββββΊα΄α΄α΄Κα΄β»ββββββ·",
        )


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "βΎ"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"β {str(e)}"
        is_database_working = False
    else:
        output = "β« "
        is_database_working = True
    return is_database_working, output
