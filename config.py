import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'This will be replaced in production'

SQLALCHEMY_DATABASE_URI = 'postgres://vagrant:vagrant@localhost/apidb'