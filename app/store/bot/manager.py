import typing
from logging import getLogger

from app.store.tg_api.dataclasses import Message, CallbackQuery

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = getLogger("handler")
        self.command_handlers: dict[callable] = {}
        self.callback_query_handlers: dict[callable] = {}

    async def handle_updates(self, updates: list[dict]):
        for update in updates:
            match update:
                case {"message": {"text": text, "from": {"is_bot": False}} as data} if text.startswith("/"):
                    data["from_"] = data["from"]
                    if text in self.command_handlers:
                        await self.command_handlers[text](bot=self, message=Message.from_dict(**data))
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
            # TODO: Исправить регистрацию команды в чате (с @username)
            # self.command_handlers[f"{command}@{self.app.store.tg_api.bot_username}"] = handler

    def register_callback_query_handler(self, data: str, handler: callable):
        self.callback_query_handlers[data] = handler
