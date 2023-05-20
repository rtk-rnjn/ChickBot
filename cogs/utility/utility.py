import discord
import asyncio
from core import Cog
from discord import app_commands
from typing import Optional, Union
from discord.ext import commands
from .utils import Confirm
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

    @commands.hybrid_command(name="lock", description="Locks down a channel")
    @app_commands.describe(channel="The channel to lock down.")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel:discord.TextChannel):
        """
        Locks down a channel
        channel: The channel to lock down. 
        """
        await ctx.send(f"Locking down {channel}.")
        await asyncio.sleep(3)
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            

    @commands.hybrid_command(name="unlock", description="Unlocks a channel")
    @app_commands.describe(channel="The channel to unlock.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel:discord.TextChannel):
        """
        Unlocks a channel
        channel: The channel to unlock. 
        """
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"Unlocked {channel}.")  

    @commands.hybrid_command(name="nuke", description="Nukes a channel")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        """
        Nukes the channel
        """
        await ctx.send("Are you sure you want to nuke this channel?", view=Confirm(ctx), delete_after=60)

    