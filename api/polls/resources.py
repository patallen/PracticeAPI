from api import db
from flask_restful import Resource, marshal_with, fields, reqparse, abort
from api.polls.models import Choice, Poll

from marshmallow_jsonapi import Schema, fields as flds


class PollSchema(Schema):
    id = flds.Str(dump_only=True)
    text = flds.Str()

    choices = flds.Relationship(
        related_url='/polls/{poll_id}/choices',
        related_url_kwargs={'poll_id': '<id>'},
        # Include resource linkage
        many=True, include_data=True,
        type_='choices'
    )
    class Meta:
        type_ = 'polls'
        strict = True


choice_fields = {
    'text': fields.String,
    'votes': fields.Integer,
    'uri': fields.Url('choice')
}
poll_fields = {
    'text': fields.String,
    'choices': fields.Url('poll_choices'),
    'uri': fields.Url('poll')
}

poll_parser = reqparse.RequestParser()
poll_parser.add_argument(
    'text',
    dest='text',
    location='form',
    required=True
)

choice_parser = reqparse.RequestParser()
choice_parser.add_argument(
    'text',
    dest='text',
    location='form',
    required=True
)


class PollAPI(Resource):

    def get(self, id):
        poll = Poll.get_or_abort404(id)
        return PollSchema().dump(poll).data

    def put(self, id):
        args = poll_parser.parse_args()
        poll = Poll.get_or_abort404(id)
        poll.text = args.text
        poll.save()
        return PollSchema().dump(poll).data, 200

    def delete(self, id):
        poll = Poll.get_or_abort404(id)
        poll.delete()
        return {}, 200


class PollListAPI(Resource):

    def get(self):
        polls = Poll.query.all()
        return PollSchema(many=True).dump(polls).data

    def post(self):
        args = poll_parser.parse_args()
        poll = Poll.create(text=args.text)
        return PollSchema().dump(poll).data, 201


class PollChoiceAPI(Resource):

    @marshal_with(choice_fields)
    def get(self, poll_id, id):
        choice = Choice.get_or_abort404(id)
        poll = choice.poll
        if poll.id == poll_id:
            return choice
        abort(404)

    def delete(self, poll_id, id):
        choice = Choice.get_or_abort404(id)
        poll = choice.poll
        if poll.id == poll_id:
            choice.delete()
            return 200
        abort(404)


class PollChoiceListAPI(Resource):
    @marshal_with(choice_fields)
    def get(self, id):
        choices = Poll.get_or_abort404(id).choices.all()
        return choices

    @marshal_with(choice_fields)
    def post(self, id):
        args = choice_parser.parse_args()
        poll = Poll.query.get(id)
        choice = Choice.create(text=args.text, commit=False)
        poll.choices.append(choice)
        db.session.commit()
        return choice
