import re
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, make_response
from app.api.v1.models.landlord_models import LandlordRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.validators import validate

INIT_DB = init_db()

LANDLORD = Blueprint('landlord', __name__)

LANDLORD_RECORDS = LandlordRecords()

@LANDLORD.route('/landlord/registration', methods=['POST'])
def landlord_registration():
    '''landlord registration endpoint'''
    try:
        data = request.get_json()

        firstname = data["firstname"]
        lastname = data["lastname"]
        email = data["email"]
        phonenumber = data["phonenumber"]
        pwd = data["password"]
        password = generate_password_hash(pwd)

        validate(firstname, lastname, email, phonenumber, password, pwd)

        cur = INIT_DB.cursor()
        cur.execute("""SELECT email FROM landlord WHERE email = '%s' """ % (email))
        data = cur.fetchone()

        if data is not None:
            return jsonify({"message": "account already exists"}), 400

        try:
            return (LANDLORD_RECORDS.register_landlord(firstname, lastname, email, password, phonenumber))

        except (psycopg2.Error) as error:
            return jsonify({"error":str(error)})

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400


@LANDLORD.route('/landlord/login', methods=['POST'])
def login():
    '''Allow landlords to log in'''
    return LANDLORD_RECORDS.login_landlord()

@LANDLORD.route('/landlord/logout', methods=['POST'])
def logout():
    '''logout a user'''
    return jsonify("Goodbye!")

@LANDLORD.route('/landlord/tenants', methods=['POST'])
def tenants():
    '''Allow landlords to log in'''
    return LANDLORD_RECORDS.view_tenants()