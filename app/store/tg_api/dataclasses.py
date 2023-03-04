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
    def from_dict(cls, from_: dict, message: dict, data: str, callback_query_id: int):
        from_["id_"] = from_["id"]
        message["from_"] = message["from"]
        return cls(
            from_=User.from_dict(**from_),
            message=Message.from_dict(**message) if message else None,
            data=data,
            id=callback_query_id,
        )


@dataclass
class Update:
    id: int
    message: Optional[Message]
    callback_query: Optional[CallbackQuery]

    @classmethod
    def from_dict(
        cls,
        update_id: int,
        message: Optional[dict] = None,
        callback_query: Optional[dict] = None,
    ):
        return cls(
            id=update_id,
            message=Message.from_dict(
                message_id=message["message_id"],
                from_=message["from"],
                chat=message["chat"],
                date=message["date"],
                text=message["text"],
            )
            if message
            else None,
            callback_query=CallbackQuery.from_dict(
                from_=callback_query["from"],
                callback_query_id=callback_query["id"],
                message=callback_query["message"],
                data=callback_query["data"],
            )
            if callback_query
            else None,
        )
