import discord
import re
from discord.ext import commands
from core import Cog, Chick

class TooManyCaps(Cog):
    def __init__(self, bot: Chick):
        self.bot = bot
        

    @Cog.listener()
    async def on_message(self, message):
        caps_count = sum(1 for c in message.content if c.isupper())
        if caps_count != 0:
            message_length = len(message.content)
            cap_percentage = caps_count / message_length
            max_cap_percentage = 0.5
            if cap_percentage > max_cap_percentage:
                warning_message = f"{message.author.mention}, Please avoid excessive use of capital letters."
                await message.delete()
                await message.channel.send(warning_message, delete_after = 5)