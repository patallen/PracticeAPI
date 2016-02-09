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
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE,PATCH'
    )
    return response

from api.users.models import *
from api.todos.models import *

# Load User Endpoints
from api.users.resources import UserListAPI, UserAPI, UserSignupAPI
api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<username>', endpoint='user')
api.add_resource(UserSignupAPI, '/signup', endpoint='signup')

# Load Todo Endpoints
from api.todos.resources import TodoListAPI, TodoAPI, ListsAPI, ListAPI
api.add_resource(TodoAPI, '/todos/<int:id>', endpoint='todo')
api.add_resource(ListsAPI, '/lists', endpoint='todo_lists')
api.add_resource(ListAPI, '/lists/<int:id>', endpoint='todo_list')

api.add_resource(TodoListAPI, '/lists/<int:id>/todos', endpoint='list_todos')

from api.jwt import make_payload
