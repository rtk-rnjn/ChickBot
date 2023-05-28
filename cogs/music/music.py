import math
import re

import discord
import lavalink
import requests
from typing import Optional
from discord.ext import commands
from discord import app_commands
from lavalink.filters import LowPass

import config
from core import Chick, View

from .spotify import thumbnail

url_rx = re.compile(r'https?://(?:www\.)?.+')



class VoiceClient(discord.VoiceClient):
    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                config.LAVALINK_HOST,
                config.LAVALINK_PORT,
                config.LAVALINK_AUTH,
                'us',
                'music-node'
            )
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        lavalink_data = {
            't': 'VOICE_SERVER_UPDATE',
            'd': data
        }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        lavalink_data = {
            't': 'VOICE_STATE_UPDATE',
            'd': data
        }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = False, self_mute: bool = False) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel, self_mute=self_mute, self_deaf=self_deaf)

    async def disconnect(self, *, force: bool = False) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)
        if not force and not player.is_connected:
            return
        await self.channel.guild.change_voice_state(channel=None)
        player.channel_id = None
        self.cleanup()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = commands.Context

        if not hasattr(bot, 'lavalink'): 
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node(config.LAVALINK_HOST, config.LAVALINK_PORT, config.LAVALINK_AUTH, 'eu', 'music-node')  # Host, Port, Password, Region, Name

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
        
    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id)
        should_connect = ctx.command.name in ('play')

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')
            await ctx.send('Join a voicechannel first.', delete_after=10)

        v_client = ctx.voice_client
        if not v_client:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')
                await ctx.send('Not connected.', delete_after=10)

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')
                await ctx.send('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=VoiceClient)
        else:
            if v_client.channel.id != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')
                await ctx.send('You need to be in my voicechannel.', delete_after=10)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.TrackStartEvent):
            c = event.player.fetch('channel')
            if c:
                c = self.bot.get_channel(c)
                if c:
                    requester = await self.bot.fetch_user(event.track.requester)
                    embed = discord.Embed(colour=self.bot.color, title='Now Playing', color=self.bot.color)
                    embed.add_field(name='Song', value=f'[{event.track.title}]({event.track.uri})')
                    embed.add_field(name='Duration', value=str(lavalink.utils.format_time(event.track.duration)))
                    embed.set_footer(text=f'Requested by {requester.name}', icon_url=requester.display_avatar.url)
                    embed.set_thumbnail(url=f"{thumbnail(event.track.identifier)}")
                    await c.send(embed=embed, delete_after=event.track.duration/1000-5)
        elif isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = event.player.guild_id
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    @commands.hybrid_command()
    async def join(self, ctx):  
        """ Joins a voicechannel. """
        await self.ensure_voice(ctx)
        await ctx.send('Connected.', delete_after=10)

    @commands.hybrid_command()
    @app_commands.describe(
        song="Song/playlist name or url, Provide artist for better result", 
        artist="Artist name for better result")
    async def play(self, ctx, song: str,*, artist:Optional[str]=None):
        """Searches and plays a song from a given query. provide artist for better result"""
        if not ctx.voice_client:
            await ctx.invoke(self.bot.get_command(self.music.join))
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if artist is None:
            query = song.strip('<>')
        else:
            query = artist.strip('[]') + ' ' + song.strip('<>')
        if not url_rx.match(query):
            query = f'spsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results.tracks:
            return await ctx.send('Nothing found!', delete_after=10)

        embed = discord.Embed(color=self.bot.color)
        if results.load_type == 'PLAYLIST_LOADED':
            tracks = results.tracks

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results.playlist_info.name} - {len(tracks)} tracks'
        else:
            track = results.tracks[0]
            embed.title = f'Added to queue.'
            embed.description = f'Song : [{track.title}]({track.uri}) by {track.author}'
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed, delete_after=10)
        if not player.is_playing:
            await player.play()

    @commands.hybrid_command()
    async def pause(self, ctx):
        """Pauses the player."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Not playing.', delete_after=10)
        if player.paused:
            return await ctx.send('Already paused.', delete_after=10)
        else:
            await player.set_pause(True)

    @commands.hybrid_command()
    async def resume(self, ctx):
        """Resumes the player."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Not playing.', delete_after=10)
        if not player.paused:
            return await ctx.send('Not paused.', delete_after=10)
        else:
            await player.set_pause(False)
            await ctx.send('⏯ | Resumed.', delete_after=10)

    @commands.hybrid_command()
    async def skip(self, ctx):
        """ Skips the current track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Not playing.', delete_after=10)
        await player.skip()
        await ctx.send('⏭ | Skipped.', delete_after=10)

    @commands.hybrid_command()
    async def stop(self, ctx):
        """ Disconnects the player and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not ctx.voice_client:
            return await ctx.send('Not connected.', delete_after=10)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!', delete_after=10)
        player.queue.clear()
        await player.stop()
        await ctx.voice_client.disconnect(force=True)
        await ctx.send('Disconnected.', delete_after=10)

    @commands.hybrid_command()
    async def volume(self, ctx, volume: int = None):
        """ Changes the player's volume. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not volume:
            return await ctx.send(f'🔈 | {player.volume}%', delete_after=10)
        await player.set_volume(volume)
        await ctx.send(f'🔈 | Set to {player.volume}%', delete_after=10)

    @commands.hybrid_command()
    async def shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Nothing playing.', delete_after=10)
        player.shuffle = not player.shuffle
        await ctx.send('🔀 | Shuffle ' + ('enabled' if player.shuffle else 'disabled'), delete_after=10)

    @commands.hybrid_command()
    async def queue(self, ctx, page: int=1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            return await ctx.send('There\'s nothing in the queue! Why not queue something?', delete_after=10)
        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue_list = ''
        for i, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{i + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=self.bot.color, description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}, do {ctx.prefix}queue <page> to view a different page.')
        await ctx.send(embed=embed)