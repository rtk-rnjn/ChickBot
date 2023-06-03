from __future__ import annotations

import asyncio
from typing import Optional

import discord
from discord.ext import commands
from typing_extensions import Annotated

from core import ChickBot, Cog

from .utils import askgpt, get_chick_fact, translate


class Misc(Cog):
    def __init__(self, bot: ChickBot):
        self.bot = bot

    @commands.hybrid_command()
    async def translate(
        self,
        ctx: commands.Context[ChickBot],
        *,
        message: Annotated[Optional[str], commands.clean_content] = None,
    ) -> None:
        """Translates a message to English using Google translate."""
        if message is None:
            await ctx.send("Missing a message to translate")
        try:
            result = await translate(message, session=self.bot.session)
        except Exception as e:
            return await ctx.send(f"An error occurred: {e.__class__.__name__}: {e}")

        embed = discord.Embed(title="Translated", colour=self.bot.color)
        embed.add_field(
            name=f"From {result.source_language}", value=result.original, inline=False
        )
        embed.add_field(
            name=f"To {result.target_language}", value=result.translated, inline=False
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="askgpt", description="Get answer of a question")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def askgpt(self, ctx: commands.Context[ChickBot], *, prompt: str) -> None:
        await ctx.defer(ephemeral=False)
        try:
            result = await asyncio.to_thread(askgpt, user_text=prompt)
            await ctx.send(
                embed=discord.Embed(
                    title="OpenAI GPT-3",
                    description=f"**Query** : ```{prompt}```\n**Response**; ```{result}```",
                    color=0x2F3136,
                ).set_footer(
                    text="Text-da-vinci-003", icon_url=self.bot.user.display_avatar.url
                )
            )
        except Exception as e:
            await ctx.send("404 not found ! Try again later.")

    @commands.hybrid_command(
        name="chick", description="Get a random fact about chicken"
    )
    async def chick(self, ctx: commands.Context[ChickBot]) -> None:
        try:
            fact = await get_chick_fact()
        except Exception as e:
            fact = "chiken fact not found ! Try again later."
        async with ctx.typing():
            await ctx.send(fact)
