import re
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, make_response
from app.api.v1.models.property_models import PropertyRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.validators import validate

INIT_DB = init_db()

PROPERTY = Blueprint('property', __name__)

PROPERTY_RECORDS = PropertyRecords()

@PROPERTY.route('/property/registration', methods=['POST'])
def tenant_registration():
    '''property registration'''
    try:
        data = request.get_json()

        property_name = data["property_name"]

        cur = INIT_DB.cursor()
        cur.execute("""SELECT property_name FROM properties WHERE property_name = '%s' """ % (property_name))
        data = cur.fetchone()

        if data is not None:
            return jsonify({"message": "property already exists"}), 400

        try:
            return (PROPERTY_RECORDS.register_property(property_name))

        except (psycopg2.Error) as error:
            return jsonify(error)

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400


@PROPERTY.route('/property/all', methods=['GET'])
def view_all():
    '''view all properties'''
    return PROPERTY_RECORDS.view_properties()

@PROPERTY.route('/property/<int: property_id>', methods=['GET'])
def view_one(property_id):
    '''view property by property id'''
    return PROPERTY_RECORDS.view_property(property_id)

@PROPERTY.route('/property/<string: property_name>', methods=['GET'])
def view_one(property_name):
    '''view property by property name'''
    return PROPERTY_RECORDS.view_property_by_name(property_name)