import re
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, make_response
from app.api.v1.models.property_models import PropertyRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.validators import validate
from app.api.v1.utils.token import login_required

INIT_DB = init_db()

PROPERTY = Blueprint('property', __name__)

PROPERTY_RECORDS = PropertyRecords()

@PROPERTY.route('/property', methods=['POST'])
@login_required
def property_registration():
    '''property registration'''
    try:
        data = request.get_json()

        property_name = data["property_name"]

        if not property_name.strip():
            return jsonify({"error": "property name cannot be empty"}), 400

        if not re.match(r"^[A-Za-z][a-zA-Z]", property_name):
            return jsonify({"error": "input valid property name"}), 400

        cur = INIT_DB.cursor()
        cur.execute("""SELECT property_name FROM property WHERE property_name = '%s' """ %(property_name))
        data = cur.fetchone()
        print(data)

        if data != None:
            return jsonify({"message": "property already exists"}), 400

        try:
            return PROPERTY_RECORDS.register_property(property_name)

        except (psycopg2.Error) as error:
            return jsonify({"error":error})

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400


@PROPERTY.route('/property', methods=['GET'])
def view_all():
    '''view all properties'''
    return PROPERTY_RECORDS.view_properties()

@PROPERTY.route('/property/<int:property_id>', methods=['GET'])
def view_one(property_id):
    '''view property by property id'''
    return PROPERTY_RECORDS.view_property(property_id)

@PROPERTY.route('/property/<string:property_name>', methods=['GET'])
def view_one_by_name(property_name):
    '''view property by property name'''
    return PROPERTY_RECORDS.view_property_by_name(property_name)