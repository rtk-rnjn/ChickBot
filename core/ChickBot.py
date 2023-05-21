import asyncio
import logging

import aiohttp
import discord
from discord.ext import commands

from .Butons import LinkButton, LinkType
from .Help import HelpCommand

Logger = logging.getLogger("discord.client")
hdlr = logging.StreamHandler()
frmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', "%Y-%m-%d %H:%M:%S", style='{')
hdlr.setFormatter(frmt)
Logger.addFilter(hdlr)


class ChickBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or(self.config.PREFIX),
            help_command=HelpCommand(),
            intents=discord.Intents.all(), 
            activity=discord.Activity(
                type=discord.ActivityType.competing, 
                name="development"),
            **kwargs
            )

    @property
    def Logger(self):
        return Logger

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

    async def on_ready(self):
        for ext in self.config.EXTENSIONS:
            await self.load_extension(ext)
            self.Logger.info(f'Loaded extension {ext}')
        await asyncio.sleep(10)
        synced = await self.tree.sync()
        self.Logger.info(f"{len(synced)} Slash commands have been globally synchronized.")
        self.Logger.info(f'Logged in as {self.user}')

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()

    async def on_command_error(self, ctx, error) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            await ctx.send(f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.", delete_after=5)
        if isinstance(error, commands.CommandNotFound):
            return  
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing a required argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("One or more arguments are invalid.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
        else:
            # Print the error to the console for debugging purposes
            print(f"An error occurred: {type(error).__name__} - {error}")
            await ctx.send("An error occurred while executing the command.")

    async def on_message(self, message):
        if self.user.mention in message.content:
            embed = discord.Embed(title="Chick | a discord bot", description=f"Hi {message.author.mention}!\nMy prefix is `{self.config.PREFIX}`.\nUse `{self.config.PREFIX}help` to get started. \n`All commands are available as slash (/)`", color=self.color)
            embed.set_thumbnail(url=self.user.display_avatar.url)
            embed.set_footer(text=self.config.FOOTER, icon_url=self.user.display_avatar.url)
            links = [
                LinkType("Invite", self.invite_url),
                LinkType("Support", self.config.SERVER_LINK)
            ]
            await message.channel.send(embed=embed, view=LinkButton(links))



Chick = ChickBot()