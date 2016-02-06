from marshmallow_jsonapi import Schema, fields
from marshmallow import post_load

from api.todos.models import Todo


class TodoSchema(Schema):
    id = fields.Str(dump_only=True)
    text = fields.Str()
    complete = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        type_ = 'todos'
        strict = True

    @post_load
    def make_todo(self, data):
        return Todo(**data)
