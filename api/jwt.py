from datetime import datetime

from flask import request, current_app

from api import app, jwt


@app.route("/refresh-token", methods=['POST'])
def token_refresh_endpdoint():
    data = request.get_json()
    token = data.get('access_token')
    payload = jwt.jwt_decode_callback(token)
    identity = jwt.identity_callback(payload)
    new_token = jwt.jwt_encode_callback(identity)
    return jwt.auth_response_callback(new_token, identity)


@jwt.jwt_payload_handler
def make_payload(identity):
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    identity = getattr(identity, 'username') or identity['username']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}
