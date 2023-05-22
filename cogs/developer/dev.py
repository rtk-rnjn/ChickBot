import discord
from typing import Optional
from discord.ext import commands
from core import Chick, Cog

class Developer(Cog):
    def __init__(self, bot: Chick):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Reloads a cog"""
        try:
            await self.bot.unload_extension("cogs."+cog)
            await self.bot.load_extension("cogs."+cog)
        except Exception as e:
            await ctx.send(f'Failed to reload cog `{cog}`: `{e.__class__.__name__}`: `{e}`')
        else:
            await ctx.send(f'Reloaded cog `{cog}`')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sync(self, ctx, scope:Optional[str]) -> None:
        if scope == "global":
            await ctx.send("Synchronizing. It may take more then 30 sec", delete_after=15)
            synced=await ctx.bot.tree.sync()
            await ctx.send(f"{len(synced)} Slash commands have been globally synchronized.")
            return
        elif scope == "guild":
            await ctx.send("Synchronizing. It may take more then 30 sec", delete_after=15)
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(f"{len(synced)} Slash commands have been synchronized in this guild.", delete_after=5)
            return
        await ctx.send("The scope must be `global` or `guild`.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unsync(self, ctx, scope:Optional[str]) -> None:
        if scope == "global":
            await ctx.send("Unsynchronizing...", delete_after=5)
            ctx.bot.tree.clear_commands(guild=None)
            unsynced = await ctx.bot.tree.sync()
            await ctx.send(f"{len(unsynced)} Slash commands have been globally unsynchronized.", delete_after=5)
            return
        elif scope == "guild":
            await ctx.send("Unsynchronizing...", delete_after=5)
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            unsynced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(f"{len(unsynced)} Slash commands have been unsynchronized in this guild.", delete_after=5)
            return
        await ctx.send("The scope must be `global` or `guild`.", delete_after=5)