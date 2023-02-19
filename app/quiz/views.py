from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import querystring_schema, request_schema, response_schema

from app.quiz.models import Answer
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredDecorator
from app.web.utils import json_response


@AuthRequiredDecorator
class ThemeAddView(View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]
        theme = await self.store.quizzes.get_theme_by_title(title)
        if theme:
            raise HTTPConflict(reason="Theme with this title already exists.")
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


@AuthRequiredDecorator
class ThemeListView(View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        data = {"themes": themes}
        return json_response(data=ThemeListSchema().dump(data))


@AuthRequiredDecorator
class QuestionAddView(View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        data = await self.request.json()
        question = await self.store.quizzes.get_question_by_title(data["title"])
        if question:
            raise HTTPConflict(reason="Question with this title already exists.")
        theme = await self.store.quizzes.get_theme_by_id(data["theme_id"])
        if not theme:
            raise HTTPNotFound(
                reason=f"Theme with id={data['theme_id']} was not found."
            )
        question = await self.store.quizzes.create_question(
            title=data["title"],
            theme_id=data["theme_id"],
            answers=[Answer(**a) for a in data["answers"]]
        )
        return json_response(data=QuestionSchema().dump(question))


@AuthRequiredDecorator
class QuestionListView(View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        theme_id = self.request.rel_url.query.get("theme_id")
        if theme_id:
            try:
                theme_id = int(theme_id)
            except ValueError:
                raise HTTPBadRequest(reason="Theme id must be integer.")
        questions = await self.store.quizzes.list_questions(theme_id)
        data = {"questions": questions}
        return json_response(data=ListQuestionSchema().dump(data))
