from fabric.api import *


env.use_ssh_config = True
env.user = "vagrant"
env.host = "10.10.10.6"

app_name = "api"

connection = "%s@%s" % (env.user, env.host)
virtualenv = "/var/%senv" % app_name
root = "/var/%s" % app_name

apt_packages = [
    'gcc',
    'libncurses5-dev',
    'libffi-dev',
    'build-essential',
    'python-pip',
    'postgresql',
    'nginx',
    'htop',
    'vim',
    'redis-server',
]

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


@hosts(connection)
def setup_db():
    sudo("apt-get install postgresql-server-dev-all postgresql postgresql-contrib -y")
    run("sudo -u postgres createuser --superuser vagrant")
    run("sudo -u postgres psql -c \"ALTER USER vagrant WITH PASSWORD 'vagrant';\"")
    run("sudo -u vagrant createdb -O vagrant apidb")


@hosts(connection)
def setup_nginx():
    sudo("apt-get install nginx")
    with cd("/etc/nginx"):
        sudo("chown -R vagrant:vagrant .")

        if exists("sites-available/%s", app_name):
            put("server/nginx/%s" % app_name, "sites-available")
            run("ln -s sites-available/%s sites-enabled/%s", (app_name, app_name))

        if not exists("sites-enabled/default"):
            run("rm sites-enabled/default")

        sudo("service nginx restart")


@hosts(connection)
def apt_install():
    sudo("apt-get update -y")
    sudo("apt-get install %s -y" % " ".join(apt_packages))


@hosts(connection)
def apt_upgrade():
    sudo("apt-get update -y")
    sudo("apt-get dist-upgrade -y")


@hosts(connection)
def setup_server():
    apt_install()
    apt_upgrade()
    setup_db()
    setup_nginx()
