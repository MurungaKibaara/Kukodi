'''Create database model to store user data'''
import datetime
import re
import psycopg2
from psycopg2.extras import DictCursor
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
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
        """ Add a new tenant """

        payload = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password,
            "phonenumber": phonenumber
        }

        query = """INSERT INTO tenants (firstname, lastname, email,
        password, phonenumber) VALUES (%(firstname)s, %(lastname)s, %(email)s,%(password)s, %(phonenumber)s);"""

        cur = self.database.cursor()
        cur.execute(query, payload)
        self.database.commit()

        return jsonify({"message": ("tenant %s successfully created")%(firstname)}), 201

    def login_tenant(self):
        ''' sign in a tenant '''
        try:
            data = request.get_json()

            user_email = data["email"]
            user_password = data["password"]

            if not user_email.strip():
                return jsonify({"error": "email cannot be empty"}), 400

            if not re.match(r"^[A-Za-z][a-zA-Z]", user_email):
                return jsonify({"error": "input valid Email"}), 400

            if not user_password.strip():
                return jsonify({"error": "password cannot be empty"}), 400

            cur = INIT_DB.cursor(cursor_factory=DictCursor)
            cur.execute("""  SELECT password, tenant_id, firstname FROM tenants WHERE email = '%s' """ % (user_email))
            data = cur.fetchone()

            if data is None:
                return jsonify({"message":"tenant does not exist"})

            password = data["password"]
            tenant_id = data["tenant_id"]
            tenant = data["firstname"]

            if password is not None:
                if check_password_hash(password, user_password):
                    payload = {
                        'sub':tenant_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                        }
                    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

                    auth_token = token.decode('UTF-8')

                    return jsonify({
                        "logged in as":tenant,
                        "token":auth_token}), 200

                return jsonify({"message": "invalid credentials, try again"}), 401
            return ({"message": "tenant doesn't exist"}), 404
        except KeyError as error:
            return jsonify({"error":"a key is missing"}), 400

        except (psycopg2.Error) as error:
            return jsonify({"error":str(error)}), 400

    def update_password(self):
        ''' Update password '''
        data = request.get_json()
        old_password = data["old_password"]
        new_password = data["new_password"]

        if not re.match(r'[A-Za-z0-9@#$]{6,12}', new_password):
            return jsonify({"error": "Input a stronger password"}), 400

        cur = self.database.cursor(cursor_factory=DictCursor)
        cur.execute("""  SELECT password, email FROM tenants WHERE password = '%s' """ % (old_password))
        data = cur.fetchone()

        password = data["password"]
        email = data["email"]

        if check_password_hash(password, old_password):
            pwd = generate_password_hash(new_password)

            update_password_query = ''' UPDATE tenants SET password = "%s" WHERE email = "%s" '''%(pwd, email)
            cur.execute(update_password_query)

            return jsonify({"message":"password successfully updated"}), 200

        else:
            return jsonify({"error":"you entered the wrong password"}), 401

    def update_email(self):
        '''Update mail'''
         data = request.get_json()

        user_email = data["user_email"]
        new_email = data["new_email"]

        if not user_email.strip():
            return jsonify({"error": "email cannot be empty"}), 400

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return jsonify({"error": "input valid email"}), 400

        cur = self.database.cursor(cursor_factory=DictCursor)
        cur.execute("""  SELECT email FROM tenants WHERE email = '%s' """ % (user_email))
        data = cur.fetchone()

        if len(data) != 0:
            old_email=["email"]
            if old_email == user_email:
                update_email_query = ''' UPDATE tenants SET email = "%s" 'WHERE email= "%s" '''%(pwd, old_email)
                cur.execute(update_email_query)

                return jsonify({"message":"email successfully updated"}), 200
            else:
                jsonify({"error":"You entered the wrong email"}), 401
        else:
            return jsonify({"error":"email does not exist, check syntax"}), 401


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
