from dataclasses import dataclass
from typing import Optional

from app.store.tg_api.keyboards import ReplyKeyboardMarkup


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    username: Optional[str]

    @classmethod
    def from_dict(cls, id_: int, is_bot: bool, first_name: str, username: Optional[str] = None):
        return cls(
            id=id_,
            is_bot=is_bot,
            first_name=first_name,
            username=username,
        )


@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None

    @classmethod
    def from_dict(
        cls,
        id_: int,
        type_: str,
        first_name: Optional[str] = None,
        username: Optional[str] = None,
        title: Optional[str] = None,
    ):
        return cls(
            id=id_,
            type=type_,
            first_name=first_name,
            username=username,
            title=title,
        )


@dataclass
class Message:
    chat: Chat
    text: str
    id: Optional[int] = None
    from_: Optional[User] = None
    date: Optional[int] = None
    reply_markup: Optional[ReplyKeyboardMarkup] = None

    @classmethod
    def from_dict(cls, message_id: int, from_: dict, chat: dict, date: int, text: str):
        return cls(
            id=message_id,
            from_=User.from_dict(
                id_=from_["id"],
                is_bot=from_["is_bot"],
                first_name=from_["first_name"],
                username=from_["username"],
            ),
            chat=Chat.from_dict(
                id_=chat["id"],
                type_=chat["type"],
                first_name=chat["first_name"] if "first_name" in chat else None,
                username=chat["username"] if "username" in chat else None,
                title=chat["title"] if "title" in chat else None,
            ),
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
        return cls(
            from_=User.from_dict(
                id_=from_["id"],
                is_bot=from_["is_bot"],
                first_name=from_["first_name"],
                username=from_["username"],
            ),
            message=Message.from_dict(
                message_id=message["message_id"],
                from_=message["from"],
                chat=message["chat"],
                date=message["date"],
                text=message["text"],
            )
            if message
            else None,
            data=data,
            id=callback_query_id,
        )


@dataclass
class Update:
    id: int
    message: Optional[Message]
    callback_query: Optional[CallbackQuery]

    @classmethod
    def from_dict(cls, update_id: int, message: Optional[dict] = None, callback_query: Optional[dict] = None):
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
