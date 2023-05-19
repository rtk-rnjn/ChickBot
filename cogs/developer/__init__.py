from .dev import Developer

async def setup(bot):   
    await bot.add_cog(Developer(bot))