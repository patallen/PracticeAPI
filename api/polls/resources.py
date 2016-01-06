from api import db
from flask_restful import Resource, marshal_with, fields, reqparse
from api.polls.models import Choice, Poll


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

    @marshal_with(poll_fields)
    def get(self, id):
        poll = Poll.get_or_abort404(id)
        return poll

    @marshal_with(poll_fields)
    def put(self, id):
        args = poll_parser.parse_args()
        poll = Poll.get_or_abort404(id)
        poll.text = args.text
        poll.save()
        return poll, 200

    def delete(self, id):
        poll = Poll.get_or_abort404(id)
        poll.delete()
        return 200


class PollListAPI(Resource):

    @marshal_with(poll_fields)
    def get(self):
        return Poll.query.all()

    @marshal_with(poll_fields)
    def post(self):
        args = poll_parser.parse_args()
        poll = Poll.create(text=args.text)
        return poll, 201


class ChoiceAPI(Resource):

    @marshal_with(choice_fields)
    def get(self, id):
        choice = Choice.get_or_abort404(id)
        return choice

    def delete(self, id):
        choice = Choice.get_or_abort404(id)
        choice.delete()
        return 200


class ChoiceListAPI(Resource):
    @marshal_with(choice_fields)
    def get(self, id):
        choices = Poll.get_or_abort404(id).choices
        return choices

    @marshal_with(choice_fields)
    def post(self, id):
        args = choice_parser.parse_args()
        poll = Poll.query.get(id)
        choice = Choice.create(text=args.text, commit=False)
        poll.choices.append(choice)
        db.session.commit()
        return choice

    def delete(self, id):
        choice = Choice.get_or_abort404(id)
        choice.delete()
        return 200
