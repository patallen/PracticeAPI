from marshmallow_jsonapi import Schema, fields
from marshmallow import post_load
from api.users.models import User


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str()
    email = fields.Str()

    class Meta:
        type_ = 'users'
        strict = True

    @post_load
    def make_user(self, data):
        return User(**data)
