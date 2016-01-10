from api import db
from api.utils.mixins import BaseMixin

class Todo(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.ForeignKey('user.id'))
