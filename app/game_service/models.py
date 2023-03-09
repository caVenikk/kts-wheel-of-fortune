import typing
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.store.database.sqlalchemy_base import Base

if typing.TYPE_CHECKING:
    from app.game_service.game import Game


@dataclass
class Player:
    id: int
    first_name: str
    points: int
    username: Optional[str] = None
    game_points: int = 0

    @classmethod
    def from_orm(cls, player: "PlayerModel"):
        if player:
            return cls(id=player.id, first_name=player.first_name, username=player.username, points=player.points)
        return None


@dataclass
class Secret:
    question: str
    answer: str

    @classmethod
    def from_orm(cls, secret: "SecretModel"):
        if secret:
            return cls(question=secret.question, answer=secret.answer)


class PlayerModel(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    first_name: Mapped[str]
    username: Mapped[Optional[str]]
    points: Mapped[int]

    game: Mapped["GameModel"] = relationship(back_populates="players")

    @classmethod
    def from_dto(cls, player: Player) -> "PlayerModel":
        return cls(id=player.id, first_name=player.first_name, username=player.username, points=player.points)


class SecretModel(Base):
    __tablename__ = "secrets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str]
    answer: Mapped[str]

    games: Mapped[list["GameModel"]] = relationship(back_populates="secret")

    @classmethod
    def from_dto(cls, secret: Secret) -> "SecretModel":
        return cls(question=secret.question, answer=secret.answer)


class GameModel(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int]
    is_ended: Mapped[bool]
    secret_id: Mapped[int] = mapped_column(ForeignKey("secrets.id"))
    winner_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"))
    winner_points: Mapped[int | None]

    players: Mapped[list["PlayerModel"]] = relationship(back_populates="game")
    secret: Mapped["SecretModel"] = relationship(back_populates="games")

    @classmethod
    def from_dto(cls, game: "Game", is_ended: bool) -> "GameModel":
        return cls(
            chat_id=game.chat_id,
            is_ended=is_ended,
            secret=SecretModel.from_dto(game.secret),
            winner_id=game.winner.id,
            winner_points=game.winner.game_points,
        )
