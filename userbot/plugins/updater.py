import asyncio
import os
import sys

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

# -- Constants -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

if Config.UPSTREAM_REPO == "T0KY0":
    UPSTREAM_REPO_URL = "https://github.com/MFMVIIP/T0KY0"
else:
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**يوجد تحديث جديد ل طوكيو↯ قم بالتحديث الان للتمتع بجميع الميزات الجديده **"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Changelog is too big, view the file to see it.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "**⪼ تم التحديث بنجاح ✅**\n **جارٍ إعادة تشغيل الروبوت ، انتظر** \n **⫷ [T0KY0↫](t.me/MFMVIP) ⫸**"
    )
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    os.execle(sys.executable, *args, os.environ)
    return


@bot.on(admin_cmd(outgoing=True, pattern=r"تحديث(| الان)$"))
@bot.on(sudo_cmd(pattern="تحديث(| الان)$", allow_sudo=True))
async def upstream(event):
    "بالنسبة لأمر التحديث ، تحقق مما إذا كان الروبوت محدثًا ، أو قم بالتحديث إذا تم بتحديثه"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "**⪼ جاري البحث عن التحديثات ...🌐**")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await edit_or_reply(
            event, "**اضبط المتغيرات المطلوبة أولاً لتحديث الروبوت**"
        )
    try:
        txt = "`عفوًا .. لا يمكن لبرنامج التحديث المتابعة بسبب "
        txt += "حدثت بعض المشاكل`\n\n**تتبع السجل:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\nالدليل {error} غير موجود")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`فشل مبكر! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Unfortunately, the directory {error} "
                "does not seem to be a git repository.\n"
                "But we can fix that by force updating the userbot using "
                ".update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if changelog == "" and not force_update:
        await event.edit(
            "\n𓆰 𝙎𝙤𝙪𝙧𝙘𝙚 𝙏𝙤𝙠𝙔𝙤 𓌺 \nٴ⊶─────≺ᴛᴏᴋʏᴏ≻─────⊷\n**↲ سورس طوكيو محدث لأخر اصدار ༗ **"
            #             f"**{UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond( 
            "𝙏𝙤𝙠𝙔𝙤 ⇢ 𝙐𝙋𝘿𝘼𝙏𝙀 𝙈𝙎𝙂\n ٴ⊶─────≺ᴛᴏᴋʏᴏ≻─────⊷\nاضغط هنا **للتحديث السريع ↫ **[`.تحديث الان`] او اضغط هنا **لتنصيب التحديث** وقد يستغرق 5 دقائق ↫ [`.تحديث البوت`]\nٴ⊶─────≺ᴛᴏᴋʏᴏ≻─────⊷"
        )

    if force_update:
        await event.edit(
            "`Force-Syncing to latest stable userbot code, please wait...`"
        )
    if conf == "الان":
        await event.edit("**⪼ يتم تحديث البوت انتظر قليلاً 🌐،**")
        await update(event, repo, ups_rem, ac_br)
    return


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "`Please set up the` **HEROKU_APP_NAME** `Var`"
                " to be able to deploy your userbot...`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n" "`Invalid Heroku credentials for deploying userbot dyno.`"
            )
            return repo.__del__()
        await event.edit(
            "**تنصيب تحديث طوكيو قيد التقدم ، يرجى الانتظار حتى تنتهي العملية ، وعادة ما يستغرق التحديث من 4 إلى 5 دقائق.**"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n`Here is the error log:\n{error}`")
            return repo.__del__()
        build_status = app.builds(order_by="created_at", sort="desc")[0]
        if build_status.status == "failed":
            await event.edit("فشل التنصيب\n" "تم الإلغاء أو كان هناك بعض الأخطاء ...")
            await asyncio.sleep(5)
            return await event.delete()
        await event.edit("`Successfully deployed!\n" "Restarting, please wait...`")
    else:
        await event.edit("`Please set up`  **HEROKU_API_KEY**  ` Var...`")
    return


@bot.on(admin_cmd(outgoing=True, pattern=r"تحديث البوت$"))
@bot.on(sudo_cmd(pattern="تحديث البوت$", allow_sudo=True))
async def upstream(event):
    event = await edit_or_reply(event, "سحب التحديث  انتظر لحظة ....")
    off_repo = "https://github.com/MFMVIIP/catpack"
    os.chdir("/app")
    catcmd = f"rm -rf .git"
    try:
        await _catutils.runcmd(catcmd)
    except BaseException:
        pass
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("**⪼ يتم تنصيب التحديث  انتظر قليلاً ✔️،**")
    await deploy(event, repo, ups_rem, ac_br, txt)


CMD_HELP.update(
    {
        "updater": "**Plugin : **`updater`"
        "\n\n•  **Syntax : **`.update`"
        "\n•  **Function :** Checks if the main userbot repository has any updates "
        "and shows a changelog if so."
        "\n\n•  **Syntax : **`.update now`"
        "\n•  **Function :** Update your userbot, "
        "if there are any updates in your userbot repository.if you restart these goes back to last time when you deployed"
        "\n\n•  **Syntax : **`.update deploy`"
        "\n•  **Function :** Deploy your userbot.So even you restart it doesnt go back to previous version"
        "\nThis will triggered deploy always, even no updates."
        "\n\n•  **Syntax : **`.badcat`"
        "\n•  **Function :** Shifts from official cat repo to jisan's repo(for gali commands)"
    }
)
