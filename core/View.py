from __future__ import annotations

from typing import List, NamedTuple, Optional, Union

import discord


class View(discord.ui.View):
    def __init__(
        self, *, member: discord.Member | discord.User, timeout: int | float = 180
    ) -> None:
        self.member: discord.Member | discord.User = member
        super().__init__(timeout=timeout)

    def disable_all(self) -> None:
        for child in self.children:
            if isinstance(child, (discord.ui.Button, discord.ui.Select)):
                child.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.member:
            embed = discord.Embed(
                description=f"This can only be used by {self.member}."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        if self.disable_view_after:
            self.disable_all()
            await self.edit(view=self)
            await self.ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")


class LinkType(NamedTuple):
    name: Optional[str] = None
    url: Optional[str] = None
    emoji: Optional[str] = None


class LinkButton(discord.ui.View):
    def __init__(self, links: Union[LinkType, List[LinkType]]):
        super().__init__()
        links = links if isinstance(links, list) else [links]
        for link in links:
            self.add_item(
                discord.ui.Button(label=link.name, url=link.url, emoji=link.emoji)
            )


class ConfirmView(View):
    def __init__(self, *, member: discord.Member, timeout: int | float) -> None:
        super().__init__(member=member, timeout=timeout)
        self.value: bool | None = None
        self.message: discord.Message | None = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        self.value = False
        self.stop()
