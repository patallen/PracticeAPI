from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from jwt import JWT

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

api = Api(app)

jwt = JWT(app)

@app.after_request
def after_request(response):
	print("AFTER")
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

from api.users.models import *
from api.todos.models import *

# Load User Endpoints
from api.users.resources import UserListAPI, UserAPI, UserAuthAPI
api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<username>', endpoint='user')
api.add_resource(UserAuthAPI, '/users/authenticate', endpoint='user_auth')

# Load Todo Endpoints
from api.todos.resources import TodoListAPI, TodoAPI
api.add_resource(TodoListAPI, '/todos', endpoint='todos')
api.add_resource(TodoAPI, '/todos/<int:id>', endpoint='todo')