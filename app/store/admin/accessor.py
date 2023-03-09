import typing
from hashlib import sha256
from logging import getLogger

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.logger = getLogger("AdminAccessor")

    async def connect(self, app: "Application"):
        admin = AdminModel(
            email=self.app.config.admin.email, password=sha256(self.app.config.admin.password.encode()).hexdigest()
        )
        async with self.app.database.session() as s:
            async with s.begin():
                s.add(admin)
        return Admin.from_orm(admin)

    async def get_by_email(self, email: str) -> Admin | None:
        async with self.app.database.session() as s:
            admin = (await s.execute(select(AdminModel).where(AdminModel.email == email))).scalar()
            return Admin.from_orm(admin)

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = AdminModel(email=email, password=sha256(password.encode()).hexdigest())
        async with self.app.database.session() as s:
            async with s.begin():
                s.add(admin)
        return Admin.from_orm(admin)
