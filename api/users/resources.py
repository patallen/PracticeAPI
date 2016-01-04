from flask_restful import Resource, marshal_with, fields, reqparse
from api.users.models import User

user_fields = {
    'username': fields.String,
    'email': fields.String,
    'uri': fields.Url('user')
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
user_parser.add_argument(
    'password',
    dest='password',
    location='form',
    required=True
)


class UserListAPI(Resource):

    @marshal_with(user_fields)
    def get(self):
        return User.query.all()

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User.create(
            username=args.username,
            email=args.email,
            password=args.password
        )
        return user, 201


class UserAPI(Resource):

    @marshal_with(user_fields)
    def get(self, username):
        user = User.query.filter_by(username=username).one()
        return user
