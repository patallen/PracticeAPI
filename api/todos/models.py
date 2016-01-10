from api import db
from api.utils.mixins import BaseMixin

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
