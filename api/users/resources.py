from flask_restful import Resource
from flask import request
from api.users.models import User
from api.users.schemas import UserSchema
from api.utils.decorators import use_class_schema


class UserListAPI(Resource):
    schema = UserSchema()

    @use_class_schema(many=True)
    def get(self):
        return User.query.all(), 200


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
