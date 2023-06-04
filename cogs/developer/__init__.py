from __future__ import annotations

from core import ChickBot

from .dev import Developer


async def setup(bot: ChickBot) -> None:
    await bot.add_cog(Developer(bot))
