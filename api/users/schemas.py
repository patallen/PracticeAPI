from marshmallow_jsonapi import Schema, fields


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str()
    email = fields.Str()

    class Meta:
        type_ = 'users'
        strict = True
