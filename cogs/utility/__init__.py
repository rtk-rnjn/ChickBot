from __future__ import annotations

from core import ChickBot

from .utility import Utility


async def setup(bot: ChickBot):
    await bot.add_cog(Utility(bot))
