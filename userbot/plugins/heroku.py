import asyncio
import math
import os

import heroku3
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY

Heroku_cmd = (
    " ๐๐ค๐ช๐ง๐๐ ๐๐ค๐ ๐๐ค - ๐๐๐๐๐๐ ~ ๐๐ผ๐๐ \n"
    "ูดโถโโโโโโบแดแดแดสแดโปโโโโโโท\n"
    "**โ โซ โซ ูุงุฆููู ุงูุงูุฑ ููุฑููู :** \n"
    "โ โซ โซ `.set var` + ุงููุงุฑ + ุงููุชุบูุฑ\n"
    "โ โซ โซ `.get var` + ุงููุงุฑ ูุนุฑุถ ูุง ูู ุงููุชุบูุฑ \n"
    "โ โซ โซ `.del var` + ุงููุงุฑ ูุญุฐู ุงููุงุฑ \n"
    "ูดโถโโโโโโบแดแดแดสแดโปโโโโโโท\n"
    "๐ฉ ๐๐ค๐ช๐ง๐๐ ๐๐ค๐ ๐๐ค - [๐พ๐๐ผ๐๐๐๐](http://t.me/TOKYO_TEAM/342) ๐ช\n"
    "๐ฉ ๐๐๐๐๐ผ๐๐ผ - [๐ฟ๐๐](t.me/MFMVIP) ๐ช"
)


@bot.on(admin_cmd(pattern=r"(ูุถุน|get|del) ุงููุงุฑ (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"(ูุถุน|get|del) ุงููุงุฑ (.*)", allow_sudo=True))
async def variable(var):
    if Config.HEROKU_API_KEY is None:
        return await edit_delete(
            var,
            "โ โซ โซ ุงุถุจุท Var ุงููุทููุจ ูู Heroku ุนูู ูุธููุฉ ูุฐุง ุจุดูู ุทุจูุนู `HEROKU_API_KEY` ุงุฐุง ููุช ูุงุชุนูู ุงูู ููุฌุฏ ููุท ุงุฐูุจ ุงูู ุญุณุงุจู ูู ููุฑููู ุซู ุงูู ุงูุงุนุฏุงุฏุงุช ุณุชุฌุฏู ุจุงูุงุณูู ุงูุณุฎู ูุฏุฎูู ูู ุงููุงุฑ. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit_delete(
            var,
            "โ โซ โซ ุงุถุจุท Var ุงููุทููุจ ูู Heroku ุนูู ูุธููุฉ ูุฐุง ุจุดูู ุทุจูุนู `HEROKU_APP_NAME` ุงุณู ุงูุชุทุจูู ุงุฐุง ููุช ูุงุชุนูู.",
        )
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        ics = await edit_or_reply(var, "**โ โซ โซ ุฌุงุฑู ุงูุญุตูู ุนูู ุงููุนูููุงุช. **")
        await asyncio.sleep(1.0)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await ics.edit(
                    "๐ฉ ๐๐ค๐ช๐ง๐๐ ๐๐ค๐ ๐๐ค - ๐ฎ๐ถ๐ต๐ญ๐ฐ๐ฎ ๐๐ผ๐๐ ๐ช\nูดโถโโโโโโบแดแดแดสแดโปโโโโโโท"
                    f"\n **โ โซ โซ** `{variable} = {heroku_var[variable]}` .\n"
                )
            return await ics.edit(
                "๐ฉ ๐๐ค๐ช๐ง๐๐ ๐๐ค๐ ๐๐ค - ๐ฎ๐ถ๐ต๐ญ๐ฐ๐ฎ ๐๐ผ๐๐ ๐ช\nูดโถโโโโโโบแดแดแดสแดโปโโโโโโท"
                f"\n **โ โซ โซ ุฎุทุง :**\n-> {variable} ุบููุฑ ููุฌูุฏ. "
            )
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await bot.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await ics.edit(
                        "`[HEROKU]` ConfigVars:\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================"
                    )
            os.remove("configs.json")
            return
    elif exe == "ูุถุน":
        variable = "".join(var.text.split(maxsplit=2)[2:])
        ics = await edit_or_reply(var, "**โ โซ โซ ุฌุงุฑู ุงุนุฏุงุฏ ุงููุนูููุงุช**")
        if not variable:
            return await ics.edit("โ โซ โซ .set var `<ConfigVars-name> <value>`")
        value = "".join(variable.split(maxsplit=1)[1:])
        variable = "".join(variable.split(maxsplit=1)[0])
        if not value:
            return await ics.edit("โ โซ โซ .set var `<ConfigVars-name> <value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await ics.edit(
                "**โ โซ โซ ุชู ุชุบููุฑ** `{}` **:**\n **- ุงููุชุบูุฑ :** `{}`".format(
                    variable, value
                )
            )
        else:
            await ics.edit(
                "**โ โซ โซ ุชู ุงุถุงูู** `{}` **:** \n**- ุงููุถุงู ุงููู :** `{}`".format(
                    variable, value
                )
            )
        heroku_var[variable] = value
    elif exe == "del":
        ics = await edit_or_reply(var, "โ โซ โซ ุงูุญุตูู ุนูู ูุนูููุงุช ูุญุฐู ุงููุชุบูุฑ. ")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await ics.edit("โ โซ โซ ูุฑุฌู ุชุญุฏูุฏ `Configvars` ุชุฑูุฏ ุญุฐููุง. ")
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
            return await ics.edit(f"โ โซ โซ `{variable}`**  ุบูุฑ ููุฌูุฏ**")

        await ics.edit(f"**โ โซ โซ** `{variable}`  **ุชู ุญุฐูู ุจูุฌุงุญ. **")
        del heroku_var[variable]


@bot.on(admin_cmd(pattern="ุงุณุชุฎุฏุงูู$", outgoing=True))
@bot.on(sudo_cmd(pattern="ุงุณุชุฎุฏุงูู$", allow_sudo=True))
async def dyno_usage(dyno):
    """
    Get your account Dyno Usage
    """
    if HEROKU_APP_NAME is None:
        return await edit_delete(
            dyno,
            "โ โซ โซ ุงุถุจุท Var ุงููุทููุจ ูู Heroku ุนูู ูุธููุฉ ูุฐุง ุจุดูู ุทุจูุนู `HEROKU_APP_NAME` ุงุณู ุงูุชุทุจูู ุงุฐุง ููุช ูุงุชุนูู.",
        )
    if HEROKU_API_KEY is None:
        return await edit_delete(
            dyno,
            "โ โซ โซ ุงุถุจุท Var ุงููุทููุจ ูู Heroku ุนูู ูุธููุฉ ูุฐุง ุจุดูู ุทุจูุนู `HEROKU_API_KEY` ุงุฐุง ููุช ูุงุชุนูู ุงูู ููุฌุฏ ููุท ุงุฐูุจ ุงูู ุญุณุงุจู ูู ููุฑููู ุซู ุงูู ุงูุงุนุฏุงุฏุงุช ุณุชุฌุฏู ุจุงูุงุณูู ุงูุณุฎู ูุฏุฎูู ูู ุงููุงุฑ. ",
        )
    dyno = await edit_or_reply(dyno, "**โ โซ โซ ุฌุงุฑู ุงููุนูุงูุฌู..**")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit(
            "โ โซ โซ ุฎุทุง:** ุดู ุณูุก ูุฏ ุญุฏุซ **\n" f" โ โซ โซ `{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    # - Used -
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    # - Current -
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    return await dyno.edit(
        "๐ฉ ๐๐ค๐ช๐ง๐๐ ๐๐ค๐ ๐๐ค - ๐ฟ๐๐๐ ๐๐๐ผ๐๐ ๐ช\nูดโถโโโโโโบแดแดแดสแดโปโโโโโโท\n"
        f"**โ โซ โซ ุงุณู ุงูุชุทุจูู ูู ููุฑููู :**\n"
        f"**    - ูุนุฑู ุงุดุชุฑุงูู โ โซ โซ {Config.HEROKU_APP_NAME}**"
        f"\n\n"
        f" **โ โซ โซ ูุฏุฉ ุงุณูุชุฎุฏุงูู ูุจูุช ุทูููู : **\n"
        f"     -  `{AppHours}`**ุณุงุนู**  `{AppMinutes}`**ุฏูููู**  "
        f"**โ โซ โซ**  `{AppPercentage}`**%**"
        "\n\n"
        " **โ โซ โซ ุงูุณุงุนุงุช ุงููุชุจููู ูุงุณุชุฎุฏุงูู : **\n"
        f"     -  `{hours}`**ุณุงุนู**  `{minutes}`**ุฏูููู**  "
        f"**โ โซ โซ**  `{percentage}`**%**"
    )


@bot.on(admin_cmd(pattern="herokulogs$", outgoing=True))
@bot.on(sudo_cmd(pattern="herokulogs$", allow_sudo=True))
async def _(dyno):
    if HEROKU_APP_NAME is None:
        return await edit_delete(
            dyno,
            "Set the required var in heroku to function this normally `HEROKU_APP_NAME`.",
        )
    if HEROKU_API_KEY is None:
        return await edit_delete(
            dyno,
            "Set the required var in heroku to function this normally `HEROKU_API_KEY`.",
        )
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await dyno.reply(
            " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
        )
    data = app.get_log()
    key = (
        requests.post("https://nekobin.com/api/documents", json={"content": data})
        .json()
        .get("result")
        .get("key")
    )
    url = f"https://nekobin.com/{key}"
    reply_text = f"Recent 100 lines of heroku logs: [here]({url})"
    await edit_or_reply(dyno, reply_text)


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""
    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


@bot.on(icss_cmd(pattern="ู24"))
async def cmd(hero):
    await eor(hero, Heroku_cmd)


CMD_HELP.update(
    {
        "heroku": "Info for Module to Manage Heroku:**\n\n`.ุงุณุชุฎุฏุงูู`\nุงุณุชุฎุฏุงูู:__ูุนุฑุถ ุณุงุนุงุช ุงุณุชุฎุฏุงูู ุงูุญุงููู ูุงููุชุจููู.__\n\n`.set var <NEW VAR> <VALUE>`\nUsage: __add new variable or update existing value variable__\n**!!! WARNING !!!, after setting a variable the bot will restart.**\n\n`.get var or .get var <VAR>`\nUsage: __get your existing varibles, use it only on your private group!__\n**This returns all of your private information, please be cautious...**\n\n`.del var <VAR>`\nUsage: __delete existing variable__\n**!!! WARNING !!!, after deleting variable the bot will restarted**\n\n`.herokulogs`\nUsage:sends you recent 100 lines of logs in heroku"
    }
)
