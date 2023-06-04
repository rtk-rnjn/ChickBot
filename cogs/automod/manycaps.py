from __future__ import annotations

import discord

from core import ChickBot, Cog


class TooManyCaps(Cog):
    def __init__(self, bot: ChickBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        caps_count = sum(bool(c.isupper()) for c in message.content)
        if caps_count == 0:
            return

        message_length = len(message.content)
        cap_percentage = caps_count / message_length
        max_cap_percentage = 0.5

        if cap_percentage > max_cap_percentage:
            warning_message = f"{message.author.mention}, Please avoid excessive use of capital letters."
            await message.delete(dealy=0)
            await message.channel.send(warning_message, delete_after=5)
