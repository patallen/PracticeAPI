from api import api, db
from flask_restful import Resource, marshal_with, fields, reqparse
from api.polls.models import Choice, Poll


choice_fields = {
    'text': fields.String,
    'id': fields.Integer
}
poll_fields = {
    'id': fields.Integer,
    'text': fields.String,
    'choices': fields.List(fields.Nested(choice_fields))
}

poll_parser = reqparse.RequestParser()
poll_parser.add_argument(
    'text',
    dest='text',
    location='form',
    required=True
)


class PollItem(Resource):

    @marshal_with(poll_fields)
    def get(self, poll_id):
        poll = Poll.query.get(poll_id)
        return poll

    @marshal_with(poll_fields)
    def put(self, poll_id):
        args = poll_parser.parse_args()
        poll = Poll.query.get(poll_id)
        poll.text = args.text
        db.session.add(poll)
        db.session.commit()
        return poll


class PollsList(Resource):

    @marshal_with(poll_fields)
    def get(self):
        return Poll.query.all()

    @marshal_with(poll_fields)
    def post(self):
        args = poll_parser.parse_args()
        poll = Poll(text=args.text)
        db.session.add(poll)
        db.session.commit()
        return poll
