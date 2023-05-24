from __future__ import annotations

from contextlib import suppress
from typing import Optional, TYPE_CHECKING
import asyncio
import config
import discord

__all__ = ("View",)

class View(discord.ui.View):
    message: discord.Message
    custom_id = None
    def __init__(self, ctx: discord.ext.commands.Context, *, timeout: Optional[float]=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.bot = ctx.bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "Sorry, you can't use this interaction as it is not started by you.",
                ephemeral=True,
            )
            return False
        return True

    async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
        print("View Error:", error)
        self.ctx.bot.dispatch("command_error", self.ctx, error)
