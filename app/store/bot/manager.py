import typing
from logging import getLogger

from app.store.tg_api.dataclasses import Update
from app.store.tg_api.keyboards import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = getLogger("handler")

    async def handle_updates(self, updates: list[dict]):
        for update in updates:
            # TODO: сделать разделение апдейтов
            # match update:
            #     case {"message": message, ""}
            await self.test(update)

    async def test(self, update: dict):
        update_ = Update.from_dict(**update)
        reply_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        reply_markup.add(KeyboardButton(text="Кто я"))
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(InlineKeyboardButton(text="Я кто", callback_data="who"))

        await self.app.store.tg_api.send_message(
            chat_id=update_.message.chat.id if update_.message else update_.callback_query.message.chat.id,
            text="Привет!",
            reply_markup=inline_markup,
            parse_mode="HTML",
        )
