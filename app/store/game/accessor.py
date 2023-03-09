import typing
from logging import getLogger

from sqlalchemy import select
from sqlalchemy.sql.functions import random

from app.base.base_accessor import BaseAccessor
from app.game_service.models import Secret, SecretModel, PlayerModel, Player

if typing.TYPE_CHECKING:
    from app.web.app import Application


class GameAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.logger = getLogger("GameAccessor")

    async def connect(self, app: "Application"):
        pass

    async def get_player_by_id(self, id_: int) -> Player | None:
        async with self.app.database.session() as s:
            player = (await s.execute(select(PlayerModel).where(PlayerModel.id == id_))).scalar()
            return Player.from_orm(player) if player else None

    async def create_player(self, player: Player) -> Player:
        player_ = PlayerModel.from_dto(player)
        async with self.app.database.session() as s:
            async with s.begin():
                s.add(player_)
        return player

    async def get_random_secret(self) -> Secret:
        async with self.app.database.session() as s:
            admin = (await s.execute(select(SecretModel).order_by(random()).limit(1))).scalar()
            return Secret.from_orm(admin)
