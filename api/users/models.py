from api import db
from api.utils.mixins import BaseMixin
import bcrypt


class User(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    _password_hash = db.Column(db.String(), nullable=False)

    # Ownership
    todos = db.relationship('Todo', backref='user', lazy='dynamic')

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return False

    @property
    def password(self):
        return self._password_hash.encode('UTF-8')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.hashpw(
            password.encode('UTF-8'),
            bcrypt.gensalt()
        )

    def verify_password(self, password):
        return bcrypt.hashpw(
            password.encode('UTF-8'), self.password
        ) == self.password

    def get_id(self):
        return self.id

    @staticmethod
    def authenticate(username, password):
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is None:
                user = DummyUser()
        if user.verify_password(password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return User.query.get(user_id)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User: {}>".format(self.username)


class DummyUser(object):
    def verify_password(self, password):
        return False


class AnonymousUserMixin(object):
    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None
