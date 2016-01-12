from flask_restful import Resource, reqparse, abort
from api.users.models import User
from api.users.schemas import UserSchema
from api.utils.decorators import use_schema

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    'email',
    type=str
)
user_parser.add_argument(
    'username',
    type=str
)
user_parser.add_argument(
    'password',
    type=str
)

class UserListAPI(Resource):
    @use_schema(UserSchema, many=True)
    def get(self):
        return User.query.all(), 200

    @use_schema(UserSchema, many=False)
    def post(self):
        args = user_parser.parse_args()
        user = User.create(
            username=args.username,
            email=args.email,
            password=args.password,
        )
        return user, 201


class UserAPI(Resource):
    @use_schema(UserSchema, many=False)
    def get(self, username):
        user = User.get_by_or_abort404(username=username)
        return user, 200


class UserAuthAPI(Resource):
    def post(self):
        args = signin_parser.parse_args()
        user = User.filter(username=args.username)[0]
        if user:
            if user.verify_password(args.password):
                return {"token": "Bearer thisisatokenher"}, 200
        abort(403, "Incorrect username or password.")
