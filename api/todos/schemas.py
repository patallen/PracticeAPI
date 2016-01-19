from marshmallow_jsonapi import Schema, fields


class TodoSchema(Schema):
    id = fields.Str(dump_only=True)
    text = fields.Str()
    complete = fields.Boolean()

    class Meta:
        type_ = 'todos'
        strict = True
