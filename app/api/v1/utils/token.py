'''Validators and decorators'''
from functools import wraps
from flask import request, jsonify
from app.api.V2.models.user_models import verify_token

def login_required(auth_function):
    '''Creates login requred decorator'''
    @wraps(auth_function)
    def decorated_function(*args, **kwargs):
        '''Create decorated function'''

        auth_token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split( )[0]

        if not auth_token:
            return jsonify({"message": "token required"}), 401
        try:
            response = verify_token(auth_token)

            if isinstance(response, str):
                user = response
                if not user:
                    return jsonify({"message": "wrong email"}), 400
        except:
            return jsonify({"message": "token is invalid"}), 400

        return auth_function(*args, **kwargs)
    return decorated_function