from pathlib import Path
from typing import Union

from pyrogram.client import Client as TelegramClient
from pyrogram import filters

from . import log
from .models import Posts


class TelegramAgent(object):
    def __init__(self, name, bot_admin, work_dir):
        self.name = name
        self.bot_admin = bot_admin
        self.work_dir = work_dir
        self.session_path = Path(work_dir) / f"{name}.session"
        self.client = None

    async def connect(
        self,
        api_id: Union[str, None] = None,
        api_hash: Union[str, None] = None,
        bot_token: Union[str, None] = None,
    ):
        assert self.client is None, "Already connected?"
        if Path(self.session_path).exists():
            self.client = await self._create_telegram_client()
            log.debug(f"Telegram client: connecting to existing session...")
        else:
            if not (api_id and api_hash and bot_token):
                raise Exception("Auth Required")
            else:
                self.client = await self._create_telegram_client(
                    api_id=api_id, api_hash=api_hash, bot_token=bot_token
                )
        await self.client.start()
        self.status = "connected"
        log.debug(f"Telegram client: connected")

    async def disconnect(self):
        assert self.client
        await self.client.stop()
        self.status = "disconnected"
        self.client = None
        log.debug(f"Telegram client: disconnected")

    async def _create_telegram_client(
        self,
        api_id: Union[str, int, None] = None,
        api_hash: Union[str, int, None] = None,
        bot_token: Union[str, int, None] = None,
    ):
        assert self.client is None, "Already connected?"

        tg = TelegramClient(
            self.name,
            api_id=api_id,  # type: ignore
            api_hash=api_hash,  # type: ignore
            bot_token=bot_token,  # type: ignore
            workdir=self.work_dir,
        )

        @tg.on_message(
            filters.command(["start"]) & filters.private & filters.user(self.bot_admin)
        )
        async def welcome(client, message):
            log.debug(f"Telegram client: received text message: {message.text}")
            await message.reply(
                "Welcome to Tremolog!\n\n"
                "Send text messages, voice notes or photos to this chat, "
                "and they will be showcased on your website."
            )

        @tg.on_message(filters.private & filters.user(self.bot_admin))
        async def echo(client, message):
            log.debug(f"Telegram client: received text message: {message.text}")
            try:
                await Posts.create(text=message.text)
                await message.reply(f"Published: {message.text}")
            except Exception as e:
                log.error(f"Error: {e}")
                await message.reply(f"Error: {e}")

        return tg
