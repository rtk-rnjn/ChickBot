from __future__ import annotations

from core import ChickBot

from .info import Info


async def setup(bot: ChickBot) -> None:
    await bot.add_cog(info(bot))
