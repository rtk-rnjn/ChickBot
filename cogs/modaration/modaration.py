from __future__ import annotations

from typing import Optional, Union

import discord
from discord import app_commands
from discord.ext import commands

from core import ChickBot, Cog


class Moderation(Cog):
    def __init__(self, bot: ChickBot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="purge", description="Purges messages from the channel"
    )
    @app_commands.describe(limit="The amount of messages that should be deleted.")
    @commands.has_permissions(manage_messages=True)
    async def purge(
        self, ctx: commands.Context[ChickBot], limit: Optional[int] = 10
    ) -> None:
        """
        Purges messages from the channel
        """
        await ctx.defer(ephemeral=False)
        await ctx.send(f"Purging {limit} messages.", delete_after=15)
        purged = await ctx.channel.purge(limit=limit)
        await ctx.channel.send(f"Purged {len(purged)} messages.", delete_after=15)

    @commands.hybrid_command(name="kick", description="Kicks a member from the server")
    @app_commands.describe(member="The member to kick.")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context[ChickBot],
        member: discord.Member,
        *,
        reason: Optional[str] = None,
    ) -> None:
        """
        Kicks a member from the server
        member: The member to kick.
        """
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member} .")

    @commands.hybrid_command(name="ban", description="Bans a member from the server")
    @app_commands.describe(member="The member to ban.")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context[ChickBot],
        member: Union[discord.Member, discord.User, discord.Object, int],
        *,
        reason: Optional[str] = None,
    ) -> None:
        """
        Bans a member from the server
        member: The member to ban.
        """
        if isinstance(member, int):
            member = discord.Object(id=member)

        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"Banned {member}.")

    @commands.hybrid_command(
        name="unban", description="Unbans a member from the server"
    )
    @app_commands.describe(member="The member to unban.")
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context[ChickBot],
        member: Union[discord.Member, discord.User, discord.Object, int],
        *,
        reason: Optional[str] = None,
    ) -> None:
        """
        Unbans a member from the server
        member: The member to unban.
        """
        if isinstance(member, int):
            member = discord.Object(id=member)
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f"Unbanned {member}.")
