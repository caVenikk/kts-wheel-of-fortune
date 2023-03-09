import typing
from typing import Optional
from logging import getLogger

from app.game_service.game import Game
from app.store.tg_api.dataclasses import Message, CallbackQuery

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = getLogger("handler")
        self.game: Optional[Game] = None
        self.command_handlers: dict[callable] = {}
        self.callback_query_handlers: dict[callable] = {}

    async def handle_updates(self, updates: list[dict]):
        for update in updates:
            match update:
                case {"message": {"text": text, "from": {"is_bot": False}} as data} if text.startswith("/"):
                    data["text"] = data["text"].replace(f"@{self.app.store.tg_api.bot_username}", "")
                    data["from_"] = data["from"]
                    if data["text"] in self.command_handlers:
                        await self.command_handlers[data["text"]](bot=self, message=Message.from_dict(**data))
                case {"message": {"text": text, "from": {"is_bot": False}} as data}:
                    # Text handlers
                    pass
                case {"callback_query": {"data": callback_data, "from": {"is_bot": False}} as data}:
                    data["from_"] = data["from"]
                    data["id_"] = data["id"]
                    if callback_data in self.callback_query_handlers:
                        await self.callback_query_handlers[callback_data](
                            bot=self, callback_query=CallbackQuery.from_dict(**data)
                        )

    def register_command(self, commands: list[str] | str, handler: callable):
        if isinstance(commands, str):
            commands = [commands]
        for command in commands:
            self.command_handlers[command] = handler

    def register_callback_query_handler(self, data: str, handler: callable):
        self.callback_query_handlers[data] = handler
