from __future__ import annotations

from typing import Literal

from discord.ext import commands

from core import ChickBot, Cog


class Developer(Cog):
    def __init__(self, bot: ChickBot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: commands.Context[ChickBot]) -> bool:
        if hasattr(self.bot, "owner_id"):
            return ctx.author.id == self.bot.owner_id
        return ctx.author.id in self.bot.owner_ids

    @commands.command(hidden=True)
    async def reload(self, ctx: commands.Context[ChickBot], *, cog: str):
        """Reloads a cog"""
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(
                f"Failed to reload cog `{cog}`: `{e.__class__.__name__}`: `{e}`"
            )
        else:
            await ctx.send(f"Reloaded cog `{cog}`")

    @commands.command(hidden=True)
    async def load(self, ctx: commands.Context[ChickBot], *, cog: str):
        """Loads a cog"""
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(
                f"Failed to reload cog `{cog}`: `{e.__class__.__name__}`: `{e}`"
            )
        else:
            await ctx.send(f"Loaded cog `{cog}`")

    @commands.command(hidden=True)
    async def sync(
        self, ctx: commands.Context[ChickBot], scope: Literal["global", "guild"]
    ) -> None:
        if scope == "global":
            await ctx.send(
                "Synchronizing. It may take more then 30 sec", delete_after=15
            )
            synced = await ctx.bot.tree.sync()
            await ctx.send(
                f"{len(synced)} Slash commands have been globally synchronized."
            )
            return
        elif scope == "guild":
            await ctx.send(
                "Synchronizing. It may take more then 30 sec", delete_after=15
            )
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(
                f"{len(synced)} Slash commands have been synchronized in this guild.",
                delete_after=5,
            )
            return
        await ctx.send("The scope must be `global` or `guild`.", delete_after=5)

    @commands.command(hidden=True)
    async def unsync(
        self, ctx: commands.Context[ChickBot], scope: Literal["global", "guild"]
    ) -> None:
        if scope == "global":
            await ctx.send("Unsynchronizing...", delete_after=5)
            ctx.bot.tree.clear_commands(guild=None)
            unsynced = await ctx.bot.tree.sync()
            await ctx.send(
                f"{len(unsynced)} Slash commands have been globally unsynchronized.",
                delete_after=5,
            )
            return
        elif scope == "guild":
            await ctx.send("Unsynchronizing...", delete_after=5)
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            unsynced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(
                f"{len(unsynced)} Slash commands have been unsynchronized in this guild.",
                delete_after=5,
            )
            return
        await ctx.send("The scope must be `global` or `guild`.", delete_after=5)
