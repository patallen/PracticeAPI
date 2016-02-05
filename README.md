# Practice API
Written in Python/Flask-Restful

You Need:
- Vagrant
- Fabric for Python 2

Install:
1. Create a base directory: `$ mkdir PracticeAPI`
1. Clone the repo: `$ git clone http://github.com/patallen/practiceapi repo`
1. `$ vagrant up`
1. Add `api.practiceapi.dev` to /etc/hosts
1. Set up the server: `fab setup_server`
1. Run the WSGI server: `fab runserver`
