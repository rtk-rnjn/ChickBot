from __future__ import annotations

from core import ChickBot

from .manycaps import TooManyCaps
from .spam import AntiSpam


async def setup(bot: ChickBot) -> None:
    await bot.add_cog(TooManyCaps(bot))
    await bot.add_cog(AntiSpam(bot))
