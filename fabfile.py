from fabric.api import *

user = "vagrant"
host = "10.10.10.6"

connection = "%s@%s" % (user, host)
virtualenv = "/var/apienv"
root = "/var/api"


@hosts(connection)
def runserver(host="0.0.0.0"):
    with cd(root):
        run("%s/bin/python manage.py runserver -h %s" % (virtualenv, host))


@hosts(connection)
def manage(task):
    with cd(root):
        run("%s/bin/python manage.py %s" % (virtualenv, task))


@hosts(connection)
def db(task):
    with cd(root):
        run("%s/bin/python manage.py db %s" % (virtualenv, task))
