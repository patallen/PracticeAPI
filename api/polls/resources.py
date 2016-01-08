from api import db
from flask_restful import Resource, reqparse, abort
from api.polls.models import Choice, Poll

from api.polls.schemas import PollSchema, ChoiceSchema
from api.utils.decorators import use_schema


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
    @use_schema(PollSchema, many=False)
    def get(self, id):
        poll = Poll.get_or_abort404(id)
        return poll, 200

    @use_schema(PollSchema, many=False)
    def put(self, id):
        args = poll_parser.parse_args()
        poll = Poll.get_or_abort404(id)
        poll.text = args.text
        poll.save()
        return poll, 200

    def delete(self, id):
        poll = Poll.get_or_abort404(id)
        poll.delete()
        return {}, 200


class PollListAPI(Resource):
    @use_schema(PollSchema, many=True)
    def get(self):
        polls = Poll.query.all()
        return polls, 200

    @use_schema(PollSchema, many=False)
    def post(self):
        args = poll_parser.parse_args()
        poll = Poll.create(text=args.text)
        return poll, 201


class ChoiceAPI(Resource):
    @use_schema(ChoiceSchema, many=False)
    def get(self, id):
        choice = Choice.get_or_abort404(id)
        return choice, 200


class PollChoiceAPI(Resource):
    @use_schema(ChoiceSchema, many=False)
    def get(self, poll_id, id):
        choice = Choice.get_or_abort404(id)
        poll = choice.poll
        if poll.id == poll_id:
            return choice, 200
        abort(404)

    def delete(self, poll_id, id):
        choice = Choice.get_or_abort404(id)
        poll = choice.poll
        if poll.id == poll_id:
            choice.delete()
            return {}, 200
        abort(404)


class PollChoiceListAPI(Resource):
    @use_schema(ChoiceSchema, many=True)
    def get(self, id):
        choices = Poll.get_or_abort404(id).choices.all()
        return choices, 200

    @use_schema(ChoiceSchema, many=False)
    def post(self, id):
        args = choice_parser.parse_args()
        poll = Poll.query.get(id)
        choice = Choice.create(text=args.text, commit=False)
        poll.choices.append(choice)
        db.session.commit()
        return choice, 200
