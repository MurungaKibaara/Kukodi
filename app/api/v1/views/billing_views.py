import re
import psycopg2
from flask import Blueprint, request, jsonify
from app.api.v1.models.billing_model import BillingRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.token import login_required

INIT_DB = init_db()

BILLING = Blueprint('billing', __name__)

BILLING_RECORDS = BillingRecords()

@BILLING.route('/bills', methods=['POST'])
@login_required
def create_bill():
    '''bill creation'''
    return BILLING_RECORDS.billing()

@BILLING.route('/bills', methods=['GET'])
def view_all():
    '''view all bills'''
    return BILLING_RECORDS.view_bills()

@BILLING.route('/bills/<int:billing_id>', methods=['GET'])
def view_one(billing_id):
    '''view bills by billing id'''
    return BILLING_RECORDS.view_bill(billing_id)
