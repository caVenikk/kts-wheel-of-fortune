from app.store.bot.manager import BotManager
from app.store.tg_api.dataclasses import Message
from app.store.tg_api.keyboards import InlineKeyboardMarkup, InlineKeyboardButton


async def start(bot: BotManager, message: Message):
    inline_markup = InlineKeyboardMarkup(row_width=1)
    inline_markup.add(InlineKeyboardButton(text="Я кто", callback_data="who"))
    await bot.app.store.tg_api.send_message(
        chat_id=message.chat.id,
        text="Привет!",
        reply_markup=inline_markup,
        parse_mode="HTML",
    )
