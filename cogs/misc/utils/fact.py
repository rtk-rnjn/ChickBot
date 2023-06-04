from __future__ import annotations

import random

import aiohttp


async def get_chick_fact() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://chickenfacts.io/api/v1/facts/{id}.json",
            format(id=random.randint(1, 100)),
        ) as resp:
            json = await resp.json()

    return json["fact"]
