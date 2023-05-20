import discord
import config
import asyncio
import datetime
from core import Cog, Chick, LinkButton, LinkType, truncate_string
from discord.ext import commands
from urllib.request import urlopen
import json

def get_latest_commit():
    url = 'https://api.github.com/repos/himangshu147-git/ChickBot/commits?per_page=1'
    response = urlopen(url).read()
    data = json.loads(response.decode())
    return data[0]

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

   
    @commands.hybrid_command(name="source", description="Shows the bot's source code", aliases=["src"])
    async def source(self, ctx):
        time=get_latest_commit()["commit"]["author"]["date"]
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        embed=discord.Embed(title="Chick Bot", description="Chick is a discord bot written in Python using discord.py. It is a bot that is meant to be used for moderation, utility, and fun.", color=self.bot.color)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Latest Commit", value=f"[{get_latest_commit()['sha'][:7]}]({get_latest_commit()['html_url']})")
        embed.add_field(name="Commit Message", value=get_latest_commit()["commit"]["message"])
        embed.add_field(name="Commiter", value=f"[{get_latest_commit()['commit']['author']['name']}]({get_latest_commit()['author']['html_url']})")
        embed.add_field(name="Commited at", value=datetime.datetime.strptime(time, date_format).strftime("%A , %d-%m-%Y"))
        links = [
            LinkType("Support", config.SERVER_LINK),
            LinkType("Invite", self.bot.invite_url),
            LinkType("Github", "https://github.com/himangshu147-git/ChickBot"),
        ]
        await ctx.send(embed=embed, view=LinkButton(links))