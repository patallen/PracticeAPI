from marshmallow_jsonapi import Schema, fields


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str()
    email = fields.Str()

    polls = fields.Relationship(
        related_url='/users/{user_id}/polls',
        related_url_kwargs={'user_id': '<id>'},
        many=True, inluded_data=True,
        type_='polls'
    )

    class Meta:
        type_ = 'users'
        strict = True
