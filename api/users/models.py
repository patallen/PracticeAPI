from api import db
import bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    polls = db.relationship('Poll', backref='user', lazy='dynamic')
    _password_hash = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.hashpw(
            password.encode('UTF-8'),
            bcrypt.gensalt()
        )

    def verify_password(self, password):
        return bcrypt.hashpw(password, str(self.password)) == self.password

    @classmethod
    def create(cls, username, email, password):
        user = cls(username, email, password)
        db.session.add(user)
        db.session.commit()
        return user

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User: {}>".format(self.username)
