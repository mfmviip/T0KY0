from telethon.tl.types import ChannelParticipantsAdmins


@bot.on(admin_cmd(pattern="تاك$"))
@bot.on(sudo_cmd(pattern="تاك$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    mentions = "تاك للطامسين"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()


@bot.on(admin_cmd(pattern="للكل( (.*)|$)"))
@bot.on(sudo_cmd(pattern="للكل( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    mentions = input_str or "تاك للطامسين"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@bot.on(admin_cmd(pattern="تاك للادمنيه$"))
@bot.on(sudo_cmd(pattern="تاك للادمنيه$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "💞"
    chat = await event.get_input_chat()
    reply_to_id = await reply_id(event)
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        if not x.bot:
            mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@bot.on(admin_cmd(pattern="لنك (.*)"))
@bot.on(sudo_cmd(pattern="لنك (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        u = reply_msg.sender_id
    else:
        user, input_str = input_str.split(" ", 1)
        try:
            u = int(user)
        except ValueError:
            try:
                u = await event.client.get_entity(user)
            except ValueError:
                await event.delete()
                return
            u = int(u.id)
        except Exception:
            await event.delete()
            return
    await event.delete()
    await event.client.send_message(
        event.chat_id,
        f"<a href='tg://user?id={u}'>{input_str}</a>",
        parse_mode="HTML",
        reply_to=reply_to_id,
    )


CMD_HELP.update(
    {
        "mention": """**Plugin : **`mention`

  •  **Syntax : **`.all`
  •  **Function : **__tags recent 100 persons in the group may not work for all__  

  •  **Syntax : **`.tagall`
  •  **Function : **__tags recent 100 persons in the group may not work for all__ 

  •  **Syntax : **`.report`
  •  **Function : **__tags admins in group__  

  •  **Syntax : **`.men username/userid text`
  •  **Function : **__tags that person with the given custom text other way for this is __
  •  **syntax : **`Hi username[custom text]`
"""
    }
)
