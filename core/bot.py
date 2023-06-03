from __future__ import annotations

import asyncio
import logging
import random
import re
import time

import aiohttp
import discord
import lavalink
from discord.ext import commands, tasks

from .help import HelpCommand
from .view import LinkButton, LinkType

logger = logging.getLogger("discord.client")
hdlr = logging.StreamHandler()
frmt = logging.Formatter(
    "[{asctime}] [{levelname:<7}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
hdlr.setFormatter(frmt)
logger.addFilter(hdlr)

__all__ = ("Chick", "logger")


class ChickBot(commands.Bot):
    lavalink: lavalink.Client

    def __init__(self, **kwargs) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(self.config.PREFIX),
            help_command=HelpCommand(),
            intents=discord.Intents.all(),
            case_insensitive=True,
            **kwargs,
        )

        self.BOT_IS_READY: bool = False

    @property
    def logger(self) -> "logging.Logger":
        return logger

    @property
    def config(self):
        return __import__("config")

    @property
    def color(self):
        return self.config.COLOR

    @property
    def invite_url(self) -> str:
        return discord.utils.oauth_url(
            self.user.id,
            permissions=discord.Permissions(10430261488759),
            scopes=("bot", "applications.commands"),
            disable_guild_select=False,
        )

    async def on_ready(self) -> None:
        if self.BOT_IS_READY:
            return

        await asyncio.sleep(10)

        synced = await self.tree.sync()
        self.logger.info(
            f"{len(synced)} Slash commands have been globally synchronized."
        )

        self.BOT_IS_READY = True

    @property
    def started(self):
        return time.time()

    @tasks.loop(minutes=15)  # Anything below 15min will result in a 429
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        guilds = len(self.guilds)
        user = len(self.users)
        statuses = self.config.STATUSES
        statuses = [
            status.replace("_guilds_", str(guilds)).replace("_user_", str(user))
            for status in statuses
        ]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for ext in self.config.EXTENSIONS:
            await self.load_extension(ext)
            self.logger.info(f"Loaded extension {ext}")
        self.logger.info(f"Logged in as {self.user}")
        self.status_task.start()

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            await ctx.send(
                f"**Please slow down** - You can use this command again in "
                f"{f'{round(hours)} hours' if round(hours) > 0 else ''} "
                f"{f'{round(minutes)} minutes' if round(minutes) > 0 else ''} "
                f"{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                delete_after=5,
            )
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing a required argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("One or more arguments are invalid.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
        else:
            print(f"An error occurred: {type(error).__name__} - {error}")
            await ctx.send("An error occurred while executing the command.")

    async def on_message(self, message: discord.Message) -> None:
        if re.fullmatch(rf"<@!?{self.user.id}>", message.content):
            embed = (
                discord.Embed(
                    title="Chick | a discord bot for your server",
                    description=(
                        f"Hi {message.author.mention}!\n"
                        f"My prefix is `{self.config.PREFIX}`\n"
                        f"Use `{self.config.PREFIX}help` to get started.\n"
                        f"I provide some nice features such as modaration, music, utility, fun and more"
                        f"`All commands are available as slash (/)`"
                    ),
                    color=self.color,
                )
                .set_thumbnail(url=self.user.display_avatar.url)
                .set_footer(
                    text=self.config.FOOTER, icon_url=self.user.display_avatar.url
                )
            )
            links = [
                LinkType("Invite", self.invite_url),
                LinkType("Support", self.config.SERVER_LINK),
            ]
            await message.channel.send(embed=embed, view=LinkButton(links))
            return

        await self.process_commands(message)


Chick = ChickBot()
