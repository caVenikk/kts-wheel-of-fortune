from app.game_service.models import Player
from app.game_service.states import State
from app.store.bot.manager import BotManager
from app.store.tg_api.dataclasses import CallbackQuery


async def register_player(bot: BotManager, callback_query: CallbackQuery):
    if not bot.game or bot.game.state != State.registration:
        return

    user_id = callback_query.from_.id
    if next((player for player in bot.game.players if player.id == user_id), None):
        return

    text = callback_query.message.text
    first_name = callback_query.from_.first_name
    username = callback_query.from_.username

    player = await bot.app.store.games.get_player_by_id(user_id)
    if not player:
        player = Player(id=user_id, first_name=first_name, username=username, points=0)
        await bot.app.store.games.create_player(player)

    bot.game.players.append(player)
    new_line = "\n"
    text = f"{text}{new_line if new_line in text else 2 * new_line}🔸{first_name} (@{username})"
    if len(bot.game.players) == 3:
        text = text.replace("Открыта регистрация!", "Все участники на месте! Игра начинается через 5 секунд...")
        bot.game.state = State.finishing_registration

    await bot.app.store.tg_api.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.id,
        text=text,
        reply_markup=callback_query.message.reply_markup,
    )


async def undo_registration(bot: BotManager, callback_query: CallbackQuery):
    if not bot.game or bot.game.state not in (State.registration, State.finishing_registration):
        return
    player = next((player for player in bot.game.players if player.id == callback_query.from_.id), None)
    if not player:
        return

    text = callback_query.message.text
    if len(bot.game.players) == 3:
        text = text.replace("Все участники на месте! Игра начинается через 5 секунд...", "Открыта регистрация!")
        bot.game.state = State.registration
    bot.game.players.remove(player)
    new_line = "\n"
    text = text.replace(
        f"{new_line if len(bot.game.players) >= 1 else ''}"
        f"🔸{callback_query.from_.first_name} (@{callback_query.from_.username})",
        "",
    )

    await bot.app.store.tg_api.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.id,
        text=text,
        reply_markup=callback_query.message.reply_markup,
    )
