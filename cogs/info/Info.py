from __future__ import annotations

import datetime
import platform
import sys

import config
import discord
import lavalink
import psutil
from discord.ext import commands

from core import ChickBot, Cog, LinkButton, LinkType


class Info(Cog):
    def __init__(self, bot: ChickBot) -> None:
        self.bot = bot

    async def get_latest_commit(self) -> dict:
        async with self.bot.session.get(
            "https://api.github.com/repos/himangshu147-git/ChickBot/commits?per_page=1"
        ) as r:
            return await r.json()

    @commands.hybrid_command(name="ping", description="Shows the bot's latency")
    async def ping(self, ctx: commands.Context[ChickBot]) -> None:
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.hybrid_command(
        name="about", description="Shows information about the bot"
    )
    async def about(self, ctx: commands.Context[ChickBot]):
        embed = discord.Embed(title="Chick | a discord bot", color=self.bot.color)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.description = "Chick is a discord bot written in Python using discord.py. It is a bot that is meant to be used for moderation, utility, and fun."
        links = [
            LinkType("Support", config.SERVER_LINK),
            LinkType("Invite", self.bot.invite_url),
        ]
        await ctx.send(embed=embed, view=LinkButton(links))

    @commands.hybrid_command(
        name="source", description="Shows the bot's source code", aliases=["src"]
    )
    async def source(self, ctx: commands.Context[ChickBot]) -> None:
        await ctx.defer(ephemeral=False)
        commit_data = await self.get_latest_commit()
        time = commit_data["commit"]["author"]["date"]
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        embed = (
            discord.Embed(
                title="Chick Bot",
                description="Chick is a discord bot written in Python using discord.py. It is a bot that is meant to be used for moderation, music, utility, and fun.",
                color=self.bot.color,
            )
            .set_thumbnail(url=self.bot.user.display_avatar.url)
            .add_field(
                name="Latest Commit",
                value=f"[{commit_data['sha'][:7]}]({commit_data['html_url']})",
            )
            .add_field(name="Commit Message", value=commit_data["commit"]["message"])
            .add_field(
                name="Commiter",
                value=f"[{commit_data['commit']['author']['name']}]({commit_data['author']['html_url']})",
            )
            .add_field(
                name="Commited at",
                value=datetime.datetime.strptime(time, date_format).strftime(
                    "%A , %d-%m-%Y"
                ),
            )
        )
        links = [
            LinkType("Support", config.SERVER_LINK),
            LinkType("Invite", self.bot.invite_url),
            LinkType("Github", "https://github.com/himangshu147-git/ChickBot"),
        ]
        await ctx.send(embed=embed, view=LinkButton(links))

    @commands.hybrid_command(name="stats", description="Shows the bot's stats")
    async def stats(self, ctx: commands.Context[ChickBot]) -> None:
        async with ctx.typing():
            embed = (
                discord.Embed(title="Chick | Stats", color=self.bot.color)
                .set_thumbnail(url=self.bot.user.display_avatar.url)
                .add_field(name="Guilds", value=len(self.bot.guilds))
                .add_field(name="Users", value=len(self.bot.users))
                .add_field(name="Commands", value=len(self.bot.commands))
                .add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms")
                .add_field(
                    name="RAM", value=f"{round(psutil.virtual_memory().percent)}% used"
                )
                .add_field(
                    name="CPU",
                    value=f"{round(psutil.cpu_percent(5) / psutil.cpu_count())}% used",
                )
                .add_field(
                    name="Python",
                    value=f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                )
                .add_field(name="Discord.py", value=f"v{discord.__version__}")
                .add_field(name="Lavalink", value=f"v{lavalink.__version__}")
                .add_field(
                    name="OS", value=f"{platform.system()} v{platform.release()}"
                )
            )
            links = [
                LinkType("Support", config.SERVER_LINK),
                LinkType("Invite", self.bot.invite_url),
            ]
            await ctx.send(embed=embed, view=LinkButton(links))
