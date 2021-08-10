# Userbot module for purging unneeded messages(usually spam or ot).

from asyncio import sleep

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID

purgelist = {}


@bot.on(admin_cmd(pattern="تنظيف(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="تنظيف(?: |$)(.*)"))
@errors_handler
async def fastpurger(event):
    if event.fwd_from:
        return
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            count += 1
            async for msg in event.client.iter_messages(
                event.chat_id,
                limit=(int(input_str) - 1),
                offset_id=reply.id,
                reverse=True,
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str:
            return await edit_or_reply(
                event, f"**Error**\n`{input_str} is not an integer. Use proper syntax.`"
            )
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
    else:
        await edit_or_reply(
            event,
            "**لم يتم تحديد رسالة.**",
        )
        return
    if msgs:
        await event.client.delete_messages(chat, msgs)
    await event.delete()
    hi = await event.client.send_message(
        event.chat_id,
        "اكتمل الحذف السريع!\nحذف " + str(count) + " رساله.",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#التنظيف \n تم تنظيف " + str(count) + " رساله بنجاح",
        )
    await sleep(5)
    await hi.delete()


CMD_HELP.update(
    {
        "purge": "**Plugin : **`purge`\
        \n\n•  **Syntax : **`.purge <count> reply`\
        \n•  **Function : **__Deletes the x(count) amount of messages from the replied message if you don't use count then deletes all messages from there.__\
        \n\n•  **Syntax : **`.purgefrom reply`\
        \n•  **Function : **__Will Mark that message as oldest message of interval to delete messages.__\
        \n\n•  **Syntax : **`.purgeto reply`\
        \n•  **Function : **__Will Mark that message as newest message of interval to delete messages and will delete all messages in that interval.__\
        \n\n•  **Syntax : **`.purgeme <count>`\
        \n•  **Function : **__Deletes x(count) amount of your latest messages.__\
        \n\n•  **Syntax : **`.del <count> reply`\
        \n•  **Function : **__Deletes the message you replied to in x(count) seconds if count is not used then deletes immediately.__"
    }
)
