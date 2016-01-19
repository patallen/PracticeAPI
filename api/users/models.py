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
        user = User.get_or_abort404(username=username)
        if user.verify_password(password):
            return user

    @staticmethod
    def identity(payload):
        username = payload['identity']
        return User.query.filter_by(username=username).first()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User: {}>".format(self.username)


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
