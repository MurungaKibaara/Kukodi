import re
import psycopg2
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, url_for, redirect
from app.api.v1.models.tenant_models import TenantRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.validators import validate

INIT_DB = init_db()

TENANT = Blueprint('tenant', __name__)

TENANT_RECORDS = TenantRecords()

@TENANT.route('/tenant/registration', methods=['POST'])
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

        validate(firstname, lastname, email, phonenumber, password, confirm_password, pwd)

        cur = INIT_DB.cursor()
        cur.execute("""SELECT email FROM tenants WHERE email = '%s' """ % (email))
        data = cur.fetchone()

        if data is not None:
            return jsonify({"message": "tenant already exists"}), 400

        try:
            return (TENANT_RECORDS.register_tenant(firstname, lastname, email, password, phonenumber))

        except (psycopg2.Error) as error:
            return jsonify(error)

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400


@TENANT.route('/tenant/login', methods=['POST'])
def login():
    '''Allow tenants to log in'''
    return TENANT_RECORDS.login_tenant()

@TENANT.route('/tenant/logout', methods=['POST'])
def logout():
    '''logout a user'''
    return jsonify("Goodbye!")