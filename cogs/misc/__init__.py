from core import Chick
from .misc import Misc

async def setup(bot: Chick):
    await bot.add_cog(Misc(bot))