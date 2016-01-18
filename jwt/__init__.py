from flask import request


def _default_anonymous_handler():
	auth_header = request.headers.get('Authorization')
	if auth_header is None:
		return {}
	else:
		if auth_header == 'password':
			print "YOU SHALL PASS"
		else:
			print "That's not the password"


class JWT(object):
	def __init__(self, app, anonymous_handler=None):

		if not anonymous_handler:
			anonymous_handler = _default_anonymous_handler

		if app.config.get('ANONYMOUS_USERS', True):
			app.before_request(anonymous_handler)
		