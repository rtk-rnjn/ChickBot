from __future__ import annotations

import aiohttp


async def thumbnail(identifier: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://embed.spotify.com/oembed/?url=spotify:track:{identifier}"
        ) as r:
            return (await r.json())["thumbnail_url"]
