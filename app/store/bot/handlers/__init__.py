import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_handlers(app: "Application"):
    from app.store.bot.handlers.commands import start
    from app.store.bot.handlers.callback_query import register_player, undo_registration

    # Start
    app.store.bots_manager.register_command("/start", start)

    # Registration
    app.store.bots_manager.register_callback_query_handler("register", register_player)
    app.store.bots_manager.register_callback_query_handler("undo_register", undo_registration)

    # Game
