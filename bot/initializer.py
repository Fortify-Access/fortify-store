from pyrogram import Client, compose
from . import models


async def main():
    apps = [
        Client(bot_config.title, api_id=bot_config.api_id, api_hash=bot_config.api_hash, bot_token=bot_config.bot_token, plugins=dict(root='bot/plugins'), workdir='bot/sessions')
        async for bot_config in models.BotConfiguration.objects.filter(is_active=True)
    ]

    await compose(apps)
