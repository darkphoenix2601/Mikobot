"""
Copyright (c) 2021 TheHamkerCat
This is part of @szMikobotbot so don't change anything....
"""

from Mikobot.utils.http import post

BASE = "https://batbin.me/"


async def paste(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    return BASE + resp["message"]
