from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column

from app.store.database.sqlalchemy_base import db


@dataclass
class Player:
    id: int
    name: str
    points: int
    game_points: int = 0

    @classmethod
    def from_orm(cls, player: "PlayerModel"):
        if player:
            return cls(id=player.id, name=player.name, points=player.points)
        return None


@dataclass
class Secret:
    question: str
    answer: str


class PlayerModel(db):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str]
    points: Mapped[int]

    @classmethod
    def from_dto(cls, player: Player) -> "PlayerModel":
        return cls(id=player.id, name=player.name, points=player.points)


class SecretModel(db):
    __tablename__ = "secrets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str]
    answer: Mapped[str]

    @classmethod
    def from_dto(cls, secret: Secret) -> "SecretModel":
        return cls(question=secret.question, answer=secret.answer)
