import re
import psycopg2
from flask import Blueprint, request, jsonify
from app.api.v1.models.house_models import HouseRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.validators import validate_house_data
from app.api.v1.utils.token import login_required

INIT_DB = init_db()

HOUSE = Blueprint('house', __name__)

HOUSE_RECORDS = HouseRecords()

@HOUSE.route('/houses', methods=['POST'])
@login_required
def house_registration():
    '''house registration'''
    try:
        data = request.get_json()

        house_number = data["house_number"]
        house_type = data["house_type"]
        rent_amount = data["rent_amount"]

        validate_house_data(house_number, house_type, rent_amount)

        cur = INIT_DB.cursor()
        cur.execute("""SELECT house_number FROM houses WHERE house_number = '%s' """ %(house_number))
        data = cur.fetchone()
        print(data)

        if data != None:
            return jsonify({"message": "house already exists"}), 400

        try:
            return HOUSE_RECORDS.register_house(house_number,house_type,rent_amount)

        except (psycopg2.Error) as error:
            return jsonify(error)

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400


@HOUSE.route('/houses', methods=['GET'])
def view_all():
    '''view all houses'''
    return HOUSE_RECORDS.view_houses()

@HOUSE.route('/houses/<int:house_id>', methods=['GET'])
def view_one(house_id):
    '''view house by house id'''
    return HOUSE_RECORDS.view_house(house_id)

@HOUSE.route('/houses/<string:house_no>', methods=['GET'])
def view_one_by_number(house_no):
    '''view house by house number'''
    return HOUSE_RECORDS.view_house_by_number(house_no)