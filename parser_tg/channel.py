from telethon.tl.functions.channels import GetFullChannelRequest

from loader import client


async def full_info(channel):
    return await client(GetFullChannelRequest(channel=channel))
