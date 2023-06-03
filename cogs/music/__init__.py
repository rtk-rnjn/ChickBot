from __future__ import annotations

from core import ChickBot

from .music import Music


async def setup(bot: ChickBot):
    await bot.add_cog(Music(bot))
