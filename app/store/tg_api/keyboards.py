import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class KeyboardButton:
    text: str

    def to_dict(self):
        return {"text": self.text}


class ReplyKeyboardMarkup:
    def __init__(
        self,
        keyboard: list[list[KeyboardButton]] = None,
        row_width: int = 3,
        resize_keyboard: bool = None,
        selective: bool = None,
    ):
        if keyboard is None:
            keyboard = []
        self.keyboard = keyboard
        self.row_width = row_width
        self.resize_keyboard = resize_keyboard
        self.selective = selective

    def __str__(self):
        return str(self.keyboard)

    def __repr__(self):
        return str(self.keyboard)

    def add(self, *args):
        row = []
        for index, button in enumerate(args, start=1):
            row.append(button)
            if index % self.row_width == 0:
                self.keyboard.append(row)
                row = []
        if row:
            self.keyboard.append(row)
        return self

    def row(self, *buttons):
        self.keyboard.append(list(buttons))
        return self

    def insert(self, button):
        if self.keyboard and len(self.keyboard[-1]) < self.row_width:
            self.keyboard[-1].append(button)
        else:
            self.add(button)
        return self

    def json(self):
        dict_ = {"keyboard": [[button.to_dict() for button in row] for row in self.keyboard]}
        if self.resize_keyboard:
            dict_["resize_keyboard"] = self.resize_keyboard
        if self.selective:
            dict_["selective"] = self.selective
        return json.dumps(dict_)


@dataclass
class InlineKeyboardButton:
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None

    def to_dict(self):
        dict_ = {"text": self.text}
        if self.url:
            dict_["url"] = self.url
        if self.callback_data:
            dict_["callback_data"] = self.callback_data
        return dict_


class InlineKeyboardMarkup:
    def __init__(self, row_width: int = 3, inline_keyboard: list[list[InlineKeyboardButton]] = None):
        if inline_keyboard is None:
            inline_keyboard = []
        self.inline_keyboard = inline_keyboard
        self.row_width = row_width

    def __str__(self):
        return str(self.inline_keyboard)

    def __repr__(self):
        return str(self.inline_keyboard)

    def add(self, *args):
        row = []
        for index, button in enumerate(args, start=1):
            row.append(button)
            if index % self.row_width == 0:
                self.inline_keyboard.append(row)
                row = []
        if row:
            self.inline_keyboard.append(row)
        return self

    def row(self, *buttons):
        self.inline_keyboard.append(list(buttons))
        return self

    def insert(self, button):
        if self.inline_keyboard and len(self.inline_keyboard[-1]) < self.row_width:
            self.inline_keyboard[-1].append(button)
        else:
            self.add(button)
        return self

    def json(self):
        return json.dumps({"inline_keyboard": [[button.to_dict() for button in row] for row in self.inline_keyboard]})
