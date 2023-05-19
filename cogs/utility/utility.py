import discord
from core import Cog
from discord import app_commands
from typing import Optional, Union
from discord.ext import commands
from core import Chick

class Utility(Cog):
    def __init__(self, bot: Chick):
        self.bot = bot

    @commands.hybrid_command(name="purge", description="Purges messages from the channel")
    @app_commands.describe(limit="The amount of messages that should be deleted.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: Optional[int] = 10):
        """
        Purges messages from the channel
		"""
        await ctx.send(f"Purging {limit} messages.", delete_after=15)
        purged = await ctx.channel.purge(limit=limit)
        await ctx.channel.send(f"Purged {len(purged)} messages.", delete_after=15)