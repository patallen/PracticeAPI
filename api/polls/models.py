from api import db


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    choices = db.relationship('Choice', backref='poll')

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Poll: {}>".format(self.text)


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    votes = db.Column(db.Integer, default=0)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Choice: {}>".format(self.text)
