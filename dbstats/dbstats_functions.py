
async def disable_old_paginations(bot, stored_paginations):
    for entry in stored_paginations:
        channel = bot.get_channel(entry["channel_id"])
        if not channel:
            continue
        try:
            message = await channel.fetch_message(entry["message_id"])
        except:
            continue
        await message.edit(view=None)