from api import db
from api.utils.mixins import BaseMixin, AuditMixin


class TodoList(AuditMixin, BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))

    # Relationships
    todos = db.relationship('Todo', backref='todo_list', lazy='dynamic')


class Todo(AuditMixin, BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))
    complete = db.Column(db.Boolean, default=False)

    todo_list_id = db.Column(db.ForeignKey('todo_list.id'))
    user_id = db.Column(db.ForeignKey('user.id'))
