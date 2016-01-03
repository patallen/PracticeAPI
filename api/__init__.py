from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

api = Api(app)

from api.users.models import *
from api.polls.models import *

# Load User Endpoints
from api.users.resources import UsersList, UserItem
api.add_resource(UsersList, '/users')
api.add_resource(UserItem, '/user/<username>')

from api.polls.resources import PollItem, PollsList
api.add_resource(PollItem, '/poll/<poll_id>')
api.add_resource(PollsList, '/polls')
