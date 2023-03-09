from app.game_service.game import Game
from app.game_service.states import State
from app.store.bot.manager import BotManager
from app.store.tg_api.dataclasses import Message
from app.store.tg_api.keyboards import InlineKeyboardMarkup, InlineKeyboardButton


async def start(bot: BotManager, message: Message):
    inline_markup = InlineKeyboardMarkup(row_width=2)
    inline_markup.add(
        InlineKeyboardButton(text="Играю", callback_data="register"),
        InlineKeyboardButton(text="Не играю", callback_data="undo_register"),
    )
    secret = await bot.app.store.games.get_random_secret()
    bot.game = Game(chat_id=message.chat.id, secret=secret)
    bot.game.state = State.registration

    await bot.app.store.tg_api.send_message(
        chat_id=message.chat.id,
        text="Открыта регистрация!",
        reply_markup=inline_markup,
    )
