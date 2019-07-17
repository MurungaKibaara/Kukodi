import re
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, make_response
from app.api.v1.models.tenant_models import TenantRecords
from app.api.v1.models.database import init_db

INIT_DB = init_db()

REGISTRATION = Blueprint('tenant_registration', __name__)
LOGIN = Blueprint('tenant_login', __name__)

TENANT_RECORDS = TenantRecords()

@REGISTRATION.route('/tenant/registration', methods=['POST'])
def tenant_registration():
    '''tenant registration endpoint'''
    try:
        data = request.get_json()

        firstname = data["firstname"]
        lastname = data["lastname"]
        email = data["email"]
        phonenumber = data["phonenumber"]
        pwd = data["password"]
        password = generate_password_hash(pwd)
        confirm_password = data["confirm_password"]

        if not firstname.strip():
            return jsonify({"error": "firstname cannot be empty"}), 400

        if not re.match(r"^[A-Za-z][a-zA-Z]", firstname):
            return jsonify({"error": "input valid firstname"}), 400

        if not lastname.strip():
            return jsonify({"error": "lastname cannot be empty"}), 400

        if not re.match(r"^[A-Za-z][a-zA-Z]", lastname):
            return jsonify({"error": "input valid lastname"}), 400

        if not phonenumber.strip():
            return jsonify({"error": "phonenumber cannot be empty"}), 400

        if len(phonenumber) != 10:
            return jsonify({"error": "phonenumber has 10 digits"}), 400

        if not re.match(r"^[0-9]", phonenumber):
            return jsonify({"error": "input valid phonenumber"}), 400

        if not email.strip():
            return jsonify({"error": "email cannot be empty"}), 400

        if not password.strip():
            return jsonify({"error": "password cannot be empty"}), 400

        if not re.match(r'[A-Za-z0-9@#$]{6,12}', pwd):
            return jsonify({"error": "Input a stronger password"}), 400

        if not confirm_password.strip():
            return jsonify({"error": "confirm password cannot be empty"}), 400

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return jsonify({"error": "input valid email"}), 400

        if not check_password_hash(password, confirm_password):
            return jsonify({"error": "passwords did not match"}), 400

        # Check whether a user exists
        cur = INIT_DB.cursor()
        cur.execute("""SELECT email FROM tenants WHERE email = '%s' """ % (email))
        data = cur.fetchone()

        if data is not None:
            return jsonify({"message": "tenant already exists"}), 400

        try:
            return TENANT_RECORDS.register_tenant(firstname, lastname, email, password, phonenumber)

        except (psycopg2.Error) as error:
            return jsonify(error)

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400


@LOGIN.route('/tenant/login', methods=['POST'])
def login():
    '''Allow tenants to log in'''
    return TENANT_RECORDS.login_tenant()