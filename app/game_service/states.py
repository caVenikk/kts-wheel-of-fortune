from enum import StrEnum, auto


class State(StrEnum):
    default = auto()
    registration = auto()
    finishing_registration = auto()
    start = auto()
