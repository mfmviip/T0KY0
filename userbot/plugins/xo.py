U = "𓆰 𝙎𝙤𝙪𝙧𝙘𝙚 𝙏𝙤𝙠𝙔𝙤 - 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎 𓆪\nٴ⊶─────≺ᴛᴏᴋʏᴏ≻─────⊷\n**✘ ∫ قائـمه اوامر الالعاب :** \n⪼ `.اكس او` \nٴ⊶─────≺ᴛᴏᴋʏᴏ≻─────⊷\n 𓆩[𝙎𝙤𝙪𝙧𝙘𝙚 𝙏𝙤𝙠𝙔𝙤](t.me/TOKYO_TEAM)𓆪\n 𓆩[𝙈𝙐𝙎𝙏𝘼𝙁𝘼](t.me/MFMVIP)𓆪"


@bot.on(admin_cmd(pattern="م22"))
async def wspr(yoland):
    await eor(yoland, U)


@bot.on(admin_cmd(pattern="اكس او$"))
async def gamez(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()
