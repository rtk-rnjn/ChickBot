import discord
from datetime import timedelta
from discord.ext import commands
from core import Cog, Chick

class AntiSpam(Cog):
    def __init__(self, bot: Chick):
        self.bot = bot
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)

    @Cog.listener()
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Please don't spam!", delete_after = 10)
            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()
            if check:
                try: 
                    await message.author.timeout(timedelta(minutes = 3), reason = "Spamming")
                    await message.author.send(f"You have been muted for spamming! at {message.guild.name}")
                except: 
                    await message.channel.send(f"{message.author.mention}, don't spam! ", delete_after = 10)
            
