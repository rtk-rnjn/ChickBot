from __future__ import annotations

from core import ChickBot

from .modaration import Moderation


async def setup(bot: ChickBot):
    await bot.add_cog(Moderation(bot))
