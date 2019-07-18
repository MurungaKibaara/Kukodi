import re
import psycopg2
from flask import Blueprint, request, jsonify
from app.api.v1.models.complaints_model import ComplaintsRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.validators import complaints_verification
from app.api.v1.utils.token import login_required

INIT_DB = init_db()

COMPLAINTS = Blueprint('complaints', __name__)

COMPLAINTS_RECORDS = ComplaintsRecords()

@COMPLAINTS.route('/complaints', methods=['POST'])
@login_required
def complaints():
    '''post complaints'''
    try:
        data = request.get_json()

        title = data["title"]
        description = data["description"]

        complaints_verification(title, description)

        cur = INIT_DB.cursor()
        cur.execute("""SELECT description FROM complaints WHERE description = '%s' """ %(description))
        data = cur.fetchone()

        if data != None:
            return jsonify({"message": "complaint already exists"}), 400

        try:
            return COMPLAINTS_RECORDS.complaint(title, description)

        except (psycopg2.Error) as error:
            return jsonify(error)

    except KeyError:
        return jsonify({"error": "a key is missing"}), 400


@COMPLAINTS.route('/complaints', methods=['GET'])
def view_all():
    '''view all complaints'''
    return COMPLAINTS_RECORDS.view_complaints()

@COMPLAINTS.route('/complaints/<int:complaint_id>', methods=['GET'])
def view_one(complaint_id):
    '''view complaints by complaint id'''
    return COMPLAINTS_RECORDS.view_complaint(complaint_id)
