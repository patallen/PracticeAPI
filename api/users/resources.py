from flask_restful import Resource, reqparse
from flask import request
from api.users.models import User
from api.users.schemas import UserSchema
from api.utils.decorators import use_schema, use_class_schema


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
    schema = UserSchema()

    @use_class_schema(many=True)
    def get(self):
        return User.query.all(), 200

    @use_class_schema(many=False)
    def post(self):
        args = user_parser.parse_args()
        user = User.create(
            username=args.username,
            email=args.email,
            password=args.password,
        )
        return user, 201


class UserAPI(Resource):
    schema = UserSchema()

    @use_class_schema(many=False)
    def get(self, username):
        user = User.get_by_or_abort404(username=username)
        return user, 200

    def delete(self, username):
        user = User.get_by_or_abort404(username)
        user.delete()
        return {}, 204


class UserSignupAPI(Resource):
    schema = UserSchema()

    @use_class_schema(many=False)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.create(
                username=username,
                password=password,
                email=email
            )
        except:
            return "Unable to process request.", 400
        return user, 200
