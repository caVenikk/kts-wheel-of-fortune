import json
import typing
from typing import Optional

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.tg_api.keyboards import InlineKeyboardMarkup, ReplyKeyboardMarkup
from app.store.tg_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class TelegramAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.poller: Optional[Poller] = None
        self.base_url: str = kwargs["base_url"] if "base_url" in kwargs else "https://api.telegram.org/"
        self.bot_username: str = ""
        self.offset: int = 1
        self.limit: int = 100
        self.timeout: int = 2
        self.allowed_updates: list[str] = (
            kwargs["allowed_updates"] if "allowed_updates" in kwargs else ["message", "callback_query"]
        )

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        try:
            self.bot_username = (await self.get_me())["username"]
        except Exception as e:
            self.logger.error("Exception", exc_info=e)
        self.poller = Poller(app.store)
        self.logger.info("Start polling")
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.poller:
            await self.poller.stop()
        if self.session:
            await self.session.close()

    @staticmethod
    def _build_query(host: str, token: str, method: str, params: dict) -> str:
        url = host + f"bot{token}/" + method + "?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def poll(self):
        async with self.session.get(
            self._build_query(
                host=self.base_url,
                token=self.app.config.bot.token,
                method="getUpdates",
                params={
                    "offset": self.offset,
                    "limit": self.limit,
                    "timeout": self.timeout,
                    "allowed_updates": self.allowed_updates,
                },
            )
        ) as resp:
            data = await resp.json()
            self.logger.info(json.dumps(data, indent=4))
            if not data.get("result", []):
                return
            self.offset = data["result"][-1]["update_id"] + 1
            raw_updates = data["result"]
            updates = [update for update in raw_updates]
            if updates:
                await self.app.store.bots_manager.handle_updates(updates)

    async def get_me(self):
        async with self.session.get(
            self._build_query(host=self.base_url, token=self.app.config.bot.token, method="getMe", params={})
        ) as resp:
            data = await resp.json()
        return data["result"]

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: Optional[ReplyKeyboardMarkup | InlineKeyboardMarkup] = None,
        parse_mode: Optional[str] = None,
    ) -> None:
        params = {
            "chat_id": chat_id,
            "text": text,
        }
        if reply_markup:
            params["reply_markup"] = reply_markup.json()
        if parse_mode:
            params["parse_mode"] = parse_mode
        async with self.session.get(
            self._build_query(
                host=self.base_url,
                token=self.app.config.bot.token,
                method="sendMessage",
                params=params,
            )
        ) as resp:
            data = await resp.json()
            self.logger.info(data)
