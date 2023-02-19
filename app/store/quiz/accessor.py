from sqlalchemy import select
from sqlalchemy.orm import subqueryload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme, ThemeModel, QuestionModel, AnswerModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = ThemeModel(
            title=title,
        )
        async with self.app.database.session() as s:
            async with s.begin():
                s.add(theme)
        return Theme(
            id=theme.id,
            title=theme.title,
        )

    async def get_theme_by_title(self, title: str) -> Theme | None:
        async with self.app.database.session() as s:
            theme = (await s.execute(
                select(ThemeModel).where(ThemeModel.title == title)
            )).scalar()
            return Theme.from_orm(theme)

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        async with self.app.database.session() as s:
            theme = (await s.execute(
                select(ThemeModel).where(ThemeModel.id == id_)
            )).scalar()
            return Theme.from_orm(theme)

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session() as s:
            return [Theme.from_orm(t) for t in (await s.execute(
                select(ThemeModel)
            )).scalars()]

    async def create_answers(
            self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        async with self.app.database.session() as s:
            async with s.begin():
                for answer in answers:
                    s.add(AnswerModel(
                        title=answer.title,
                        is_correct=answer.is_correct,
                        question_id=question_id
                    ))
        return answers

    async def create_question(
            self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = QuestionModel(
            title=title,
            theme_id=theme_id,
            answers=[AnswerModel(title=a.title, is_correct=a.is_correct) for a in answers]
        )
        async with self.app.database.session() as s:
            async with s.begin():
                s.add(question)
        return Question(
            id=question.id,
            title=question.title,
            theme_id=question.theme_id,
            answers=answers
        )

    async def get_question_by_title(self, title: str) -> Question | None:
        async with self.app.database.session() as s:
            question = (await s.execute(
                select(QuestionModel).where(QuestionModel.title == title).options(subqueryload(QuestionModel.answers))
            )).scalar()
            return Question.from_orm(question)

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        stmt = select(QuestionModel).options(subqueryload(QuestionModel.answers))
        if theme_id:
            stmt = stmt.where(QuestionModel.theme_id == theme_id)
        async with self.app.database.session() as s:
            return [Question.from_orm(q) for q in (await s.execute(stmt)).scalars()]
