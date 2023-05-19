from core import Chick
from .utility import Utility

async def setup(bot: Chick):
    await bot.add_cog(Utility(bot))