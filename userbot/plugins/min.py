U = "π° ππ€πͺπ§ππ ππ€π ππ€ - πΎππππΌππΏπ πͺ\nΩ΄βΆββββββΊα΄α΄α΄Κα΄β»ββββββ·\n**β β«  ΩΨ§Ψ¦ΩΩΩ Ψ§ΩΨ§ΩΨ± Ψ§ΩΨ§ΩΨΉΨ§Ψ¨ :** \nβͺΌ `.ΩΨΉΨ¨Ω 1` \nΩ΄βΆββββββΊα΄α΄α΄Κα΄β»ββββββ·\nπ© ππ€πͺπ§ππ ππ€π ππ€ - [πππππΌππΌ](t.me/MFMVIP) πͺ"


@bot.on(admin_cmd(pattern="Ω22"))
async def wspr(yoland):
    await eor(yoland, U)


@bot.on(admin_cmd(pattern="ΩΨΉΨ¨Ω 1$"))
async def gamez(event):
    if event.fwd_from:
        return
    botusername = "@nimBot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()
