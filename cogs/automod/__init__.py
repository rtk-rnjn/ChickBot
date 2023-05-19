from .spam import AntiSpam
from .manycaps import TooManyCaps

async def setup(bot):
    await bot.add_cog(TooManyCaps(bot))
    await bot.add_cog(AntiSpam(bot))