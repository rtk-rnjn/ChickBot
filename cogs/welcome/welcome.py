from __future__ import annotations

import discord

from core import ChickBot, Cog

GUILD_ID = 1105378568734769284
CHANNEL_ID = 1108718525343871099
CHANNEL_ID_RULES = 1109493306657874030


class Welcome(Cog):
    def __init__(self, bot: ChickBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if member.guild.id == GUILD_ID:
            channel = self.bot.get_channel(CHANNEL_ID)
            embed = (
                discord.Embed(
                    title="Welcome to Chick Dev",
                    description=f"hey, {member.mention}!\nPlease read the rules\nin <#{CHANNEL_ID_RULES}> and \nenjoy your stay!",
                    color=self.bot.color,
                )
                .set_thumbnail(url=member.display_avatar.url)
                .set_footer(text="Chick OP", icon_url=self.bot.user.display_avatar.url)
            )
            await channel.send(embed=embed)
