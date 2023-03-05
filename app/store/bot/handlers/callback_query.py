from app.store.bot.manager import BotManager
from app.store.tg_api.dataclasses import CallbackQuery


async def echo(bot: BotManager, callback_query: CallbackQuery):
    await bot.app.store.tg_api.send_message(
        chat_id=callback_query.message.chat.id,
        text="Echo",
    )
