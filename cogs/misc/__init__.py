from __future__ import annotations

from core import ChickBot

from .misc import Misc


async def setup(bot: ChickBot) -> None:
    await bot.add_cog(Misc(bot))
