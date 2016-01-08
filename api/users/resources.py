from flask_restful import Resource, reqparse, abort
from api.users.models import User
from api.users.schemas import UserSchema
from api.utils.decorators import use_schema


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

signin_parser = reqparse.RequestParser()
signin_parser.add_argument(
    'username',
    dest='username',
    location='form',
    required=True
)
signin_parser.add_argument(
    'password',
    dest='password',
    location='form',
    required=True
)


class UserListAPI(Resource):
    @use_schema(UserSchema, many=True)
    def get(self):
        return User.query.all()

    def post(self):
        args = user_parser.parse_args()
        user = User.create(
            username=args.username,
            email=args.email,
            password=args.password,
        )
        return UserSchema().dump(user).data, 201


class UserAPI(Resource):

    def get(self, username):
        user = User.get_by_or_abort404(username=username)
        return UserSchema().dump(user).data, 200


class UserAuthAPI(Resource):
    def post(self):
        args = signin_parser.parse_args()
        user = User.filter(username=args.username)[0]
        if user:
            if user.verify_password(args.password):
                return {"token": "Bearer thisisatokenher"}
        abort(403, "Incorrect username or password.")
