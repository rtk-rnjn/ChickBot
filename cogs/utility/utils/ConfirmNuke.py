import discord
import config
from typing import Optional

class Confirm(discord.ui.View):
    def __init__(self, ctx, timeout: Optional[float] = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.message = ctx.message

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user.id == self.ctx.author.id:
            return True
        else:
            await interaction.response.send_message('This is not for you.', ephemeral=True)
            return False

    # async def on_timeout(self, interaction: discord.Interaction) -> bool:
    #     if interaction.timeout:
    #         for child in self.children:
    #             child.disabled=True
    #         await interaction.response.edit_message("Interaction timed out. Please rerun the command", view=None)

    @discord.ui.button(label="Confirm", style= discord.ButtonStyle.red, custom_id="confirm")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            chan = await interaction.channel.clone()
            await interaction.channel.delete()
            await chan.send(f"Hey <@{self.ctx.author.id}>, I just nuked {interaction.channel}.")
            await chan.send("https://tenor.com/view/explosion-mushroom-cloud-atomic-bomb-bomb-boom-gif-4464831")
        except:
            await interaction.response.send_message("Nuke failed, I think i don't have enough permissions to do that.")

    @discord.ui.button(label="Cancel", style= discord.ButtonStyle.green, custom_id="cancel")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled=True
        await interaction.response.edit_message(content="Nuke cancelled", view=self)
        

    