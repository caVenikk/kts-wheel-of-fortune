import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_handlers(app: "Application"):
    from app.store.bot.handlers.commands import start
    from app.store.bot.handlers.callback_query import echo

    app.store.bots_manager.register_command("/start", start)
    app.store.bots_manager.register_callback_query_handler("echo", echo)
