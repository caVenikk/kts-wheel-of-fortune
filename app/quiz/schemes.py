from marshmallow import Schema, fields, ValidationError


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


def validate_answers(answers: "AnswerSchema"):
    if len(answers) <= 1:
        raise ValidationError("the number of answers must be more than one")
    if len(list(filter(lambda x: x.get("is_correct"), answers))) != 1:
        raise ValidationError("there must be one correct answer")


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested("AnswerSchema", many=True, required=True, validate=validate_answers)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class ThemeIdSchema(Schema):
    theme_id = fields.Int()


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)
