from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
db = SQLAlchemy(app)

from api.users.models import User
jwt = JWT(app, User.authenticate, User.identity)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization'
    )
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

from api.users.models import *
from api.todos.models import *

# Load User Endpoints
from api.users.resources import UserListAPI, UserAPI
api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<username>', endpoint='user')

# Load Todo Endpoints
from api.todos.resources import TodoListAPI, TodoAPI
api.add_resource(TodoListAPI, '/todos', endpoint='todos')
api.add_resource(TodoAPI, '/todos/<int:id>', endpoint='todo')
