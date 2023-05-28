from __future__ import annotations

import asyncio
import io
import re
from typing import TYPE_CHECKING, Optional, Union

import discord
import yarl
from discord import app_commands
from discord.ext import commands
from typing_extensions import Annotated

from core import Chick, Cog, ConfirmView

from .utils import EmojiURL, emoji_name, partial_emoji


class Utility(Cog):
    def __init__(self, bot: Chick):
        self.bot = bot

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

    @commands.hybrid_command(name="nuke", description="Nukes the channel")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        """
        Nukes the channel
        """
        result = ConfirmView(member=ctx.author, timeout=60)
        await ctx.send("Are you sure you want to nuke this channel?", view=result)
        await result.wait()
        if result.value:
            await ctx.send("Nuking channel...")
            for i in range(1, 4):
                await ctx.send("# " + str(i))
                await asyncio.sleep(1)
            await asyncio.sleep(1)
            chan = await ctx.channel.clone()
            await ctx.channel.delete()
            await chan.send(f"# Hey {ctx.author.mention}, I just nuked {chan.mention}")

            await chan.send("https://tenor.com/view/chicken-bomb-gif-26332692")
        else:
            await ctx.send("Canceled nuke.")

    @commands.hybrid_command(name='emoji', description='Creates a new emoji in the server using imoji url or file')
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(
        name='The emoji name',
        file='The image file to use for uploading',
        url='The URL to use for uploading',
    )
    async def emoji(self, ctx, name: Annotated[str, emoji_name], file: Optional[discord.Attachment], *, url: Optional[str]):
        if not ctx.me.guild_permissions.manage_emojis:
            return await ctx.send('Bot does not have permission to add emoji.')
        reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'
        if file is None and url is None:
            return await ctx.send('Missing emoji file or url to upload with')
        if file is not None and url is not None:
            return await ctx.send('Cannot mix both file and url arguments, choose only')
        is_animated = False
        request_url = ''
        if url is not None:
            upgraded = await EmojiURL.convert(ctx, url)
            is_animated = upgraded.animated
            request_url = upgraded.url
        elif file is not None:
            if not file.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return await ctx.send('Unsupported file type given, expected png, jpg, or gif')

            is_animated = file.filename.endswith('.gif')
            request_url = file.url

        emoji_count = sum(e.animated == is_animated for e in ctx.guild.emojis)
        if emoji_count >= ctx.guild.emoji_limit:
            return await ctx.send('There are no more emoji slots in this server.')

        async with self.bot.session.get(request_url) as resp:
            if resp.status >= 400:
                return await ctx.send('Could not fetch the image.')
            if int(resp.headers['Content-Length']) >= (256 * 1024):
                return await ctx.send('Image is too big.')

            data = await resp.read()
            coro = ctx.guild.create_custom_emoji(name=name, image=data, reason=reason)
            async with ctx.typing():
                try:
                    created = await asyncio.wait_for(coro, timeout=10.0)
                except asyncio.TimeoutError:
                    return await ctx.send('Sorry, the bot is rate limited or it took too long.')
                except discord.HTTPException as e:
                    return await ctx.send(f'Failed to create emoji somehow: {e}')
                else:
                    return await ctx.send(f'Created {created}')