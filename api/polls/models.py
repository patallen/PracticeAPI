from api import db


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), nullable=False)
    choices = db.relationship('Choice', backref='poll')

    def __init__(self, text):
        self.text = text


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
