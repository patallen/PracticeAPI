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


class PollAPI(Resource):

    @marshal_with(poll_fields)
    def get(self, id):
        poll = Poll.query.get(id)
        return poll

    @marshal_with(poll_fields)
    def put(self, id):
        args = poll_parser.parse_args()
        poll = Poll.query.get(id)
        poll.text = args.text
        db.session.add(poll)
        db.session.commit()
        return poll, 200


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
        return Choice.query.get(id)


class ChoiceListAPI(Resource):
    @marshal_with(choice_fields)
    def get(self, id):
        return Poll.query.get(id).choices
