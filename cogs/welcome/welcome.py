import discord
from core import Cog, Chick
from database import DB

class Welcome(Cog):
    def __init__(self, bot: Chick):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 1105378568734769284:
            channel = self.bot.get_channel(1108718525343871099)
            embed=discord.Embed(title="Welcome to Chick Dev", description=f"hey, {member.mention}!\nPlease read the rules\nin <#1109493306657874030> and \nenjoy your stay!", color=self.bot.color)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Chick OP", icon_url=self.bot.user.display_avatar.url)
            await channel.send(embed=embed)
        else: 
            pass