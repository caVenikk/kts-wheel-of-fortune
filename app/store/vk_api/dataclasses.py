from dataclasses import dataclass


@dataclass
class UpdateObject:
    id: int
    from_id: int
    peer_id: int
    text: str
    date: int


@dataclass
class Update:
    type: str
    object: UpdateObject


@dataclass
class Message:
    user_id: int
    text: str
