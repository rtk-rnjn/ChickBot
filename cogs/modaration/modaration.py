import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Union
from core import Cog, Chick

class Moderation(Cog):
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

    @commands.hybrid_command(name="kick", description="Kicks a member from the server")
    @app_commands.describe(member="The member to kick.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        """
        Kicks a member from the server
        member: The member to kick. 
        """
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member} .")


    @commands.hybrid_command(name="ban", description="Bans a member from the server")       
    @app_commands.describe(member="The member to ban.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        """
        Bans a member from the server
        member: The member to ban. 
        """
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member}.")

    @commands.hybrid_command(name="unban", description="Unbans a member from the server")
    @app_commands.describe(member="The member to unban.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: Union[discord.Member, discord.User]):
        """
        Unbans a member from the server
        member: The member to unban. 
        """
        await member.unban(reason=reason)
        await ctx.send(f"Unbanned {member}.")