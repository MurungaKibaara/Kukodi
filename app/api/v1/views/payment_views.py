import re
import psycopg2
from flask import Blueprint, request, jsonify
from app.api.v1.models.payments_model import PaymentRecords
from app.api.v1.models.database import init_db
from app.api.v1.utils.token import login_required

INIT_DB = init_db()

PAYMENTS = Blueprint('payments', __name__)

PAYMENT_RECORDS = PaymentRecords()

@PAYMENTS.route('/payments', methods=['POST'])
@login_required
def make_payment():
    '''bill creation'''
    return PAYMENT_RECORDS.make_lnm_request()

@PAYMENTS.route('/payments', methods=['GET'])
def view_all():
    '''view all bills'''
    return PAYMENT_RECORDS.view_payments()

@PAYMENTS.route('/payments/<int:payment_id>', methods=['GET'])
def view_one(payment_id):
    '''view bills by billing id'''
    return PAYMENT_RECORDS.view_payment(payment_id)
