'''Create database model to store user data'''
import datetime
import psycopg2
from psycopg2.extras import DictCursor
import jwt
from werkzeug.security import check_password_hash
from flask import jsonify, request
from app.api.v1.models.database import init_db
from instance.config import Config
JWT_SECRET = Config.SECRET_KEY

INIT_DB = init_db()

class TenantRecords():
    """ Create a model that stores users data"""

    def __init__(self):
        """initialize the database and argument variables"""
        self.database = INIT_DB

    def register_tenant(self, firstname, lastname, email, password, phonenumber):
        """ Add a new tenant to all tenant data """

        payload = {
            "tenant_id": tenant_id,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password,
            "confirm_password": confirm_password
            "phonenumber": phonenumber
        }

        query = """INSERT INTO tenants (firstname, lastname, email,
        password, phonenumber) VALUES
        (%(firstname)s, %(lastname)s, %(email)s,%(password)s, %(phonenumber)s);"""

        cur = self.database.cursor()
        cur.execute(query, payload)
        self.database.commit()

def login_tenant():
    '''sign in a tenant'''
    try:
        user_email = request.get_json()["email"]
        user_password = request.get_json()["password"]

        cur = INIT_DB.cursor(cursor_factory=DictCursor)
        cur.execute(
            """  SELECT password FROM tenants WHERE email = '%s' """ % (user_email))
        data = cur.fetchone()

        if data is None:
            return jsonify({"message":"no data here"})

        password = data["password"]

        if password is not None:
            if check_password_hash(password, user_password):
                payload = {
                    'sub':user_email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                    }
                token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

                auth_token = token.decode('UTF-8')

                return jsonify({
                    "logged in as":user_email,
                    "token":auth_token}), 200

            return jsonify({"message": "invalid credentials, try again"}), 401
        return ({"message": "user doesn't exist"}), 404

    except (psycopg2.Error) as error:
        return jsonify(error)


def token_verification(auth_token):
    '''authentication token verification'''
    try:
        payload = jwt.decode(auth_token, JWT_SECRET, algorithms='HS256')
        return payload['sub']

    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'

    except jwt.InvalidTokenError:
        return 'invalid token. Please log in again.'

    return 'Could not be verified'