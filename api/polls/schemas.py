from marshmallow_jsonapi import Schema, fields


class PollSchema(Schema):
    id = fields.Str(dump_only=True)
    text = fields.Str()

    choices = fields.Relationship(
        related_url='/polls/{poll_id}/choices',
        related_url_kwargs={'poll_id': '<id>'},
        many=True, include_data=True,
        type_='choices'
    )

    class Meta:
        type_ = 'polls'
        strict = True


class ChoiceSchema(Schema):
    id = fields.Str(dump_only=True)
    text = fields.Str()

    poll = fields.Relationship(
        related_url='/polls/{poll_id}',
        related_url_kwargs={'poll_id': '<poll.id>'},
        include_data=True,
        type_='polls'
    )

    class Meta:
        type_ = 'choices'
        strict = True
