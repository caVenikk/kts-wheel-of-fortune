from collections import deque

from app.game_service.models import Player, Secret


class Game:
    def __init__(self, secret: Secret, players: deque[Player] | None = None):
        self.players: deque[Player] = players
        self.secret: Secret = secret
        self.displayed_word: str = "🟦" * len(secret.answer)
        self.current_player: Player | None = None
        self.winner: Player | None = None
