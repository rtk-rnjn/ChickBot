from .modaration import Moderation
from core import Chick

async def setup(bot: Chick):
    await bot.add_cog(Moderation(bot))