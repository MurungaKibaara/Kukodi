import re
import psycopg2
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, url_for, redirect
from app.api.v1.models.tenant_models import TenantRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.validators import validate
from app.api.v1.utils.token import login_required

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
        house_no = data["house_no"]
        pwd = data["password"]
        password = generate_password_hash(pwd)

        validate(firstname, lastname, email, phonenumber, password, pwd)

        cur = INIT_DB.cursor()
        cur.execute("""SELECT email FROM tenants WHERE email = '%s' """ % (email))
        data = cur.fetchone()
        print(data)

        if data is not None:
            return jsonify({"message": "tenant already exists"}), 400
        
        cur = INIT_DB.cursor()
        cur.execute(""" SELECT house_no FROM houses WHERE house_no = '%s' """ % (house_no))
        data = cur.fetchone()

        if len(data) !=0:
            return jsonify({"message": "house number %s does not exist"%(house_no)}), 400
        
        cur = INIT_DB.cursor()
        cur.execute(""" SELECT house_no FROM tenants WHERE house_no = '%s' """ % (house_no))
        data = cur.fetchall()

        if len(data) !=0:
            return jsonify({"message": "house number %s already assigned to another tenant"%(house_no)}), 400

        try:
            return (TENANT_RECORDS.register_tenant(firstname, lastname, email, password, phonenumber, house_no))

        except (psycopg2.Error) as error:
            return jsonify({"error":str(error)})

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400

@TENANT.route('/tenant/login', methods=['POST'])
def login():
    '''Allow tenants to log in'''
    return TENANT_RECORDS.login_tenant()

@TENANT.route('/tenant/logout', methods=['POST'])
@login_required
def logout():
    '''logout a user'''
    return jsonify({"message":"logged out, bye!"}), 200

@TENANT.route('/tenant/emailupdate', methods=['POST'])
@login_required
def update_email():
    '''update user email'''
    return TENANT_RECORDS.update_email()

@TENANT.route('/tenant/passwordupdate', methods=['POST'])
@login_required
def update_password():
    '''update user password'''
    return TENANT_RECORDS.update_password()