from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: int | None
    title: str

    @classmethod
    def from_orm(cls, theme: "ThemeModel"):
        if theme:
            return cls(id=theme.id, title=theme.title)
        return None


@dataclass
class Question:
    id: int | None
    title: str
    theme_id: int
    answers: list["Answer"]

    @classmethod
    def from_orm(cls, question: "QuestionModel"):
        if question:
            return cls(
                id=question.id,
                title=question.title,
                theme_id=question.theme_id,
                answers=[Answer.from_orm(a) for a in question.answers]
            )
        return None


@dataclass
class Answer:
    title: str
    is_correct: bool

    @classmethod
    def from_orm(cls, answer: "AnswerModel"):
        if answer:
            return cls(title=answer.title, is_correct=answer.is_correct)
        return None


class ThemeModel(db):
    __tablename__ = "themes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False, unique=True)


class QuestionModel(db):
    __tablename__ = "questions"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False, unique=True)
    theme_id = Column("theme_id", Integer, ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)

    answers: list["AnswerModel"] = relationship("AnswerModel", back_populates="question", cascade="all, delete")


class AnswerModel(db):
    __tablename__ = "answers"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    is_correct = Column("is_correct", Boolean, nullable=False)
    question_id = Column("question_id", Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    question = relationship("QuestionModel", back_populates="answers")
