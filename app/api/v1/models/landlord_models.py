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

class LandlordRecords():
    """ A model that stores users data"""

    def __init__(self):
        """initialize the database and argument variables"""
        self.database = INIT_DB

    def register_landlord(self, firstname, lastname, email, password, phonenumber):
        """ Add a new landlord """

        payload = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password,
            "phonenumber": phonenumber
        }

        query = """INSERT INTO landlord (firstname, lastname, email,
        password, phonenumber) VALUES (%(firstname)s, %(lastname)s, %(email)s,%(password)s, %(phonenumber)s);"""

        cur = self.database.cursor()
        cur.execute(query, payload)
        self.database.commit()

        return jsonify({"message": ("Landlord %s successfully created")%(firstname)}), 201

    def login_landlord(self):
        '''sign in a landlord'''
        try:
            user_email = request.get_json()["email"]
            user_password = request.get_json()["password"]

            cur = INIT_DB.cursor(cursor_factory=DictCursor)
            cur.execute("""  SELECT password, landlord_id, firstname FROM landlord WHERE email = '%s' """ % (user_email))
            data = cur.fetchone()

            if data is None:
                return jsonify({"message":"account does not exist"})

            password = data["password"]
            landlord_id = data["landlord_id"]
            landlord = data["firstname"]

            if password is not None:
                if check_password_hash(password, user_password):
                    payload = {
                        'sub':landlord_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                        }
                    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

                    auth_token = token.decode('UTF-8')

                    return jsonify({
                        "logged in as":landlord,
                        "token":auth_token}), 200

                return jsonify({"message": "invalid credentials, try again"}), 401
            return ({"message": "account doesn't exist"}), 404

        except (psycopg2.Error) as error:
            return jsonify({"error":str(error)})


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