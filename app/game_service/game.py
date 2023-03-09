from collections import deque

from app.game_service.models import Player, Secret, GameModel
from app.game_service.states import State


class Game:
    def __init__(self, chat_id: int, secret: Secret):
        self.chat_id: int = chat_id
        self.players: deque[Player] = deque()
        self.secret: Secret = secret
        self.displayed_word: str = "🟦" * len(secret.answer)
        self.current_player: Player | None = None
        self.winner: Player | None = None
        self.state: State = State.default

    @classmethod
    def from_orm(cls, game: GameModel):
        return cls(
            chat_id=game.chat_id,
            secret=Secret.from_orm(game.secret),
        )
