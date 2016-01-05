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
from api.users.resources import UserListAPI, UserAPI, UserAuthAPI
api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<username>', endpoint='user')
api.add_resource(UserAuthAPI, '/users/authenticate', endpoint='user_auth')

# Load Poll/Choice Endpoints
from api.polls.resources import PollAPI, PollListAPI, ChoiceAPI, ChoiceListAPI
api.add_resource(PollListAPI, '/polls', endpoint='polls')
api.add_resource(PollAPI, '/polls/<int:id>', endpoint='poll')

api.add_resource(ChoiceAPI, '/choice/<int:id>', endpoint='choice')
api.add_resource(
    ChoiceListAPI,
    '/polls/<int:id>/choices',
    endpoint='poll_choices'
)
