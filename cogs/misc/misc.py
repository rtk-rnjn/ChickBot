import asyncio
from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands
from typing_extensions import Annotated

from core import Chick, Cog, LinkButton, LinkType

from .utils import askgpt, get_chick_fact, translate


class Misc(Cog):
    def __init__(self, bot: Chick):
        self.bot=bot
    
    @commands.hybrid_command()
    async def translate(self, ctx, *, message: Annotated[Optional[str], commands.clean_content] = None):
        """Translates a message to English using Google translate."""
        loop = self.bot.loop
        if message is None:
            await ctx.send('Missing a message to translate')
        try:
            result = await translate(message, session=self.bot.session)
        except Exception as e:
            return await ctx.send(f'An error occurred: {e.__class__.__name__}: {e}')

        embed = discord.Embed(title='Translated', colour=self.bot.color)
        embed.add_field(name=f'From {result.source_language}', value=result.original, inline=False)
        embed.add_field(name=f'To {result.target_language}', value=result.translated, inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="askgpt",
        description="Get answer of a question"
    )
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def askgpt(self, ctx, *, prompt: str):
        await ctx.defer(ephemeral=False)
        try:
            result = askgpt(user_text=prompt)
            embed.title="OpenAI GPT-3"
            embed.set_footer(text="Text-da-vinci-003", icon_url=self.bot.user.avatar.url)
            embed=discord.Embed(description=f"**Query** : ```{prompt}```\n**Response**; ```{result}```", color=0x2f3136)
            await ctx.send(embed=embed)
        except:
            await ctx.send("404 not found ! Try again later.")

    @commands.hybrid_command(name="chick", description="Get a random fact about chicken")
    async def chick(self, ctx):
        try: 
            fact = get_chick_fact()
        except: 
            fact = "chiken fact not found ! Try again later."
        async with ctx.typing():
            await ctx.send(fact)