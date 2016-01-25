from datetime import timedelta

DEBUG = True
SECRET_KEY = 'This will be replaced in production'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgres://vagrant:vagrant@localhost/apidb'

JWT_EXPIRATION_DELTA = timedelta(seconds=900)
