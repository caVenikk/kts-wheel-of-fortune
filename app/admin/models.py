from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.store.database.sqlalchemy_base import Base


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])

    @classmethod
    def from_orm(cls, admin: "AdminModel"):
        if admin:
            return cls(id=admin.id, email=admin.email, password=admin.password)
        return None


class AdminModel(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str]
    password: Mapped[str]

    @classmethod
    def from_dto(cls, admin: Admin) -> "AdminModel":
        return cls(email=admin.email, password=admin.password)
