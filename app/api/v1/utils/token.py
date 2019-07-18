'''Validators and decorators'''
from functools import wraps
from flask import request, jsonify
from app.api.v1.models.tenant_models import token_verification

def login_required(auth_function):
    '''creates login required decorator'''
    @wraps(auth_function)
    def decorated_function(*args, **kwargs):
        '''create decorated function'''

        auth_token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split( )[0]

        if not auth_token:
            return jsonify({"message": "token required"}), 401
        try:
            response = token_verification(auth_token)

            if isinstance(response, str):
                tenant = response
                if not tenant:
                    return jsonify({"message": "wrong email"}), 400
        except:
            return jsonify({"message": "token is invalid"}), 400

        return auth_function(*args, **kwargs)
    return decorated_function