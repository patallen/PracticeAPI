from api import api, db
from flask_restful import Resource, marshal_with, fields, reqparse
from api.users.models import User

user_fields = {
    'username': fields.String,
    'email': fields.String
}

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    'username',
    dest='username',
    location='form',
    required=True
)
user_parser.add_argument(
    'email',
    dest='email',
    location='form',
    required=True
)


class UsersList(Resource):
    @marshal_with(user_fields)
    def get(self):
        return User.query.all()

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User(args.username, args.email)
        db.session.add(user)
        db.session.commit()
        return user


class UserItem(Resource):
    @marshal_with(user_fields)
    def get(self, username):
        user = User.query.filter_by(username=username).one()
        return user
