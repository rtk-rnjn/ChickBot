
from __future__ import annotations
import discord
import config
from discord.ext import commands
from difflib import get_close_matches
from typing import List, Mapping
from .Butons import LinkButton, LinkType


class HelpCommand(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__(
            verify_checks=False,
            command_attrs={
                "help": "Shows help about the bot, a command, or a category",
            },
        )

    @property
    def color(self):
        return self.context.bot.color

    async def send_bot_help(self, mapping: Mapping[Cog, List[commands.Command]]):
        ctx = self.context
        hidden = ("HelpCog", "Developer")
        embed = discord.Embed(color=self.color)
        embed.title = f"{ctx.bot.user.name} Help Menu"
        embed.description = f"Use `{ctx.prefix}help <command>` for more information about a command."
        embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)
        for cog, cmds in mapping.items():
            if cog and cog.qualified_name not in hidden and await self.filter_commands(cmds, sort=True):
                embed.add_field(
                    name=cog.qualified_name.title(),
                    value=", ".join(map(lambda x: f"`{x}`", cog.get_commands())),
                )

        slash_cmds = await ctx.bot.tree.fetch_commands(guild=ctx.guild)
        slash_cmds = [f"{i.mention}" for i in slash_cmds]
        embed.add_field(name=f"{ctx.bot.user.name} Slash Commands", value=", ".join(slash_cmds), inline=False)

        links = [
            LinkType("Support", config.SERVER_LINK),
            LinkType("Invite", self.context.bot.invite_url),
        ]
        await ctx.send(embed=embed, view=LinkButton(links))

    async def send_group_help(self, group: commands.Group):
        prefix = self.context.prefix

        if not group.commands:
            return await self.send_command_help(group)

        embed = discord.Embed(color=discord.Color(self.color))

        embed.title = f"{group.qualified_name} {group.signature}"
        _help = group.help or "No description provided..."

        _cmds = "\n".join(f"`{prefix}{c.qualified_name}` : {truncate_string(c.short_doc,60)}" for c in group.commands)

        embed.description = f"> {_help}\n\n**Subcommands**\n{_cmds}"

        embed.set_footer(text=f'Use "{prefix}help <command>" for more information.')

        if group.aliases:
            embed.add_field(
                name="Aliases",
                value=", ".join(f"`{aliases}`" for aliases in group.aliases),
                inline=False,
            )

        examples = []
        if group.extras:
            if _gif := group.extras.get("gif"):
                embed.set_image(url=_gif)

            if _ex := group.extras.get("examples"):
                examples = [f"{self.context.prefix}{i}" for i in _ex]

        if examples:
            examples: str = "\n".join(examples)  # type: ignore
            embed.add_field(name="Examples", value=f"```{examples}```")

        await self.context.send(embed=embed)


    async def send_command_help(self, cmd: commands.Command):
        embed = discord.Embed(color=self.color)
        embed.title = "Command: " + cmd.qualified_name

        examples = []

        alias = ",".join((f"`{alias}`" for alias in cmd.aliases)) if cmd.aliases else "No aliases"
        _text = (
            f"**Description:** {cmd.help or 'No help found...'}\n"
            f"**Usage:** `{self.get_command_signature(cmd)}`\n"
            f"**Aliases:** {alias}\n"
            f"**Examples:**"
        )

        if cmd.extras:
            if _gif := cmd.extras.get("gif"):
                embed.set_image(url=_gif)

            if _ex := cmd.extras.get("examples"):
                examples = [f"{self.context.prefix}{i}" for i in _ex]

        examples: str = "\n".join(examples) if examples else "Command has no examples"  # type: ignore

        _text += f"```{examples}```"

        embed.description = _text

        await self.context.send(embed=embed)

    async def command_not_found(self, string: str):
        message = f"Could not find the `{string}` command. "
        commands_list = (str(cmd) for cmd in self.context.bot.walk_commands())

        if dym := "\n".join(get_close_matches(string, commands_list)):
            message += f"Did you mean...\n{dym}"

        return message
