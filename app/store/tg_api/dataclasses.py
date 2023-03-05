from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    first_name: str
    username: Optional[str]

    @classmethod
    def from_dict(cls, id_: int, first_name: str, username: Optional[str] = None, **_):
        return cls(
            id=id_,
            first_name=first_name,
            username=username,
        )


@dataclass
class Chat:
    id: int

    @classmethod
    def from_dict(cls, id_: int):
        return cls(id=id_)


@dataclass
class Message:
    chat: Chat
    text: str
    id: Optional[int] = None
    from_: Optional[User] = None
    date: Optional[int] = None

    @classmethod
    def from_dict(cls, message_id: int, from_: dict, chat: dict, date: int, text: str, **_):
        from_["id_"] = from_["id"]
        return cls(
            id=message_id,
            from_=User.from_dict(**from_),
            chat=Chat(id=chat["id"]),
            date=date,
            text=text,
        )


@dataclass()
class CallbackQuery:
    from_: User
    message: Message
    data: str
    id: Optional[int] = None

    @classmethod
    def from_dict(cls, from_: dict, message: dict, data: str, id_: int, **_):
        message["from_"] = message["from"]
        from_["id_"] = from_["id"]
        return cls(
            from_=User.from_dict(**from_),
            message=Message.from_dict(**message) if message else None,
            data=data,
            id=id_,
        )
