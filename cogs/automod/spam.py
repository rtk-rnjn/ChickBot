from __future__ import annotations

from datetime import timedelta

import discord
from discord.ext import commands

from core import ChickBot, Cog


class AntiSpam(Cog):
    def __init__(self, bot: ChickBot) -> None:
        self.bot = bot
        self.anti_spam = commands.CooldownMapping.from_cooldown(
            5, 15, commands.BucketType.member
        )
        self.too_many_violations = commands.CooldownMapping.from_cooldown(
            4, 60, commands.BucketType.member
        )

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if (
            not isinstance(message.channel, discord.abc.Messageable)
            or message.author.bot
        ):
            return
        bucket = self.anti_spam.get_bucket(message)
        if retry_after := bucket.update_rate_limit():
            await message.delete(delay=0)
            await message.channel.send(
                f"{message.author.mention}, Please don't spam!", delete_after=10
            )
            violations = self.too_many_violations.get_bucket(message)
            if check := violations.update_rate_limit():
                try:
                    await message.author.timeout(
                        timedelta(minutes=3), reason="Spamming"
                    )
                    await message.author.send(
                        f"You have been muted for spamming! at {message.guild.name}"
                    )
                except discord.HTTPException:
                    await message.channel.send(
                        f"{message.author.mention}, don't spam! ", delete_after=10
                    )
