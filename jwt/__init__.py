from flask import request, g


def _default_anonymous_handler():
	auth_header = request.headers.get('Authorization')
	@after_this_request
	def authorization_header(response):
		if auth_header is None:
			# generate key & return jwt in response
			response.headers['Authorization'] = 'BOOBS, DUDE'
		else:
			# update expiration and return new jwt in response
			### 

def call_deferred_callbacks(response):
	for cb in g.deferred_callbacks:
		cb(response)
	return response

def after_this_request(f):
	if not hasattr(g, 'deferred_callbacks'):
		g.deferred_callbacks = []
	g.deferred_callbacks.append(f)
	return f

class JWT(object):
	def __init__(self, app, anonymous_handler=None):
		app.after_request(call_deferred_callbacks)
		if not anonymous_handler:
			anonymous_handler = _default_anonymous_handler
		if app.config.get('ANONYMOUS_USERS', True):
			app.before_request(anonymous_handler)

