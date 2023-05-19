import discord
import config
from core import Cog, Chick, LinkButton, LinkType
from discord.ext import commands

class Info(Cog):
    def __init__(self, bot: Chick):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Shows the bot's latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.hybrid_command(name="about", description="Shows information about the bot")
    async def about(self, ctx):
        embed = discord.Embed(title="Chick | a discord bot", color=self.bot.color) 
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.description = f"Chick is a discord bot written in Python using discord.py. It is a bot that is meant to be used for moderation, utility, and fun."
        links = [
            LinkType("Support", config.SERVER_LINK),
            LinkType("Invite", self.bot.invite_url),
        ]
        await ctx.send(embed=embed, view=LinkButton(links))