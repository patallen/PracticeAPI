from flask import request
from flask_restful import Resource, reqparse
from api import jwt
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

    def delete(self, username):
        user = User.get_by_or_abort404(username)
        user.delete()
        return {}, 200


class TokenRefreshAPI(Resource):
    def post(self):
        data = request.get_json()
        token = data.get('access_token')
        payload = jwt.jwt_decode_callback(token)
        identity = jwt.identity_callback(payload)
        new_token = jwt.jwt_encode_callback(identity)
        return jwt.auth_response_callback(new_token, identity)
