from __future__ import annotations
from typing import List, NamedTuple, Optional, Union
import discord

class LinkType(NamedTuple):
    name: Optional[str] = None
    url: Optional[str] = None
    emoji: Optional[str] = None


class LinkButton(discord.ui.View):
    def __init__(self, links: Union[LinkType, List[LinkType]]):
        super().__init__()
    

        links = links if isinstance(links, list) else [links]

        for link in links:
            self.add_item(discord.ui.Button(label=link.name, url=link.url, emoji=link.emoji))
