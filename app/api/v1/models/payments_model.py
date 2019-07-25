'''Model to manage payment records'''
import datetime
import psycopg2
import base64
import requests
from psycopg2.extras import RealDictCursor
import jwt
from datetime import datetime, timedelta
from flask import jsonify
from app.api.v1.models.database import init_db
from app.api.v1.models.landlord_models import token_verification
from instance.config import Config
JWT_SECRET = Config.SECRET_KEY

INIT_DB = init_db()


class PaymentRecords():
    """ Create a model that creates monthly bills"""

    def __init__(self):
        """initialize the database and argument variables"""
        self.database = INIT_DB

    def payments_details(self):
        """ Get payment details """

        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split()[1]

        decoded_token = jwt.decode(auth_token, JWT_SECRET, algorithms='HS256')
        landlord_id = decoded_token['sub']

        property_id_query = (
            "SELECT property_id FROM property WHERE landlord_id='%(landlord_id)s'")

        cur = self.database.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, property_id_query)
        data = cur.fetchone()

        property_id = data['property_id']

        house_details_query = (
            "SELECT * FROM houses WHERE property_id='%(property_id)s'")

        cur = self.database.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, property_id_query)
        data = cur.fetchall()

        house_no = data["house_no"]
        amount_payable = data["rent_amount"]
        house_id = data["house_id"]

        billing_details_query = (
            "SELECT * FROM billing WHERE house_id='%(house_id)s'")

        cur = self.database.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, billing_details_query)
        data = cur.fetchall()

        billing_id = data["billing_id"]

        phone_number_query = '''SELECT phonenumber FROM tenants WHERE house_id = %(house_id)s '''

        cur = self.database.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, phone_number_query)
        data = cur.fetchall()

        phonenumber = data["phonenumber"]

        return billing_id, amount_payable, phonenumber

    def generate_access_token(self):
        '''Generate Access Token'''

        token = base64.b64encode(bytes('R2IgWD782FqFGiBi2Fr5phkvaI2szqAo:OFyNN6V3Keonc9Oh', 'utf-8'))
        token = token.decode('utf-8')
        token = json.dumps(token).strip('"')
        oauth = ("Basic " + token).strip('"')

        oauthurl = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

        oauthHeader = {
            "Host": "sandbox.safaricom.co.ke",
            "Authorization": str(oauth),
            "Content-Type": "application/json"
        }

        oauthresp = requests.get(oauthurl, headers=oauthHeader)

        oauth=oauthresp.json()
        access = oauth['access_token']


        Access_token = ("Bearer " + access).strip('"')

        return Access_token

    def make_lnm_request(self):
        '''Get api resource'''
        Access_token = generate_access_token()

        billing_id, amount_payable, phonenumber = self.payments_details()

        passkey = 'R2IgWD782FqFGiBi2Fr5phkvaI2szqAoOFyNN6V3Keonc9Oh'
        ts= time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        print(timestamp)

        lnmpasskey = '174379' + passkey + timestamp

        passkey = base64.b64encode(bytes(lnmpasskey, 'utf-8'))
        passkey = passkey.decode()
        key= json.dumps(passkey).strip('"').strip('=')
        print(key)

        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        Header = {
            "Host": "sandbox.safaricom.co.ke",
            "Authorization": str(Access_token),
            "Content-Type": "application/json"
        }

        body= {
            "BusinessShortCode": "174379",
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTkwNzE5MjE1NjQ3",
            "Timestamp": "20190719215647",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",
            "PartyA": "254719562555",
            "PartyB": "174379",
            "PhoneNumber": "254719562555",
            "CallBackURL": "https://peternjeru.co.ke/safdaraja/api/callback.php",
            "AccountReference": "account",
            "TransactionDesc": "test" ,
        }

        try:
            response = requests.post(url, headers=Header, json=body)

            if response.ok:
                return response.json()
            else:
                return(response)
        except Exception as e:
            return(e)

    def payment_processing(self):
        '''Use MPESA api to process payments'''

        billing_id, amount_payable, phonenumber = self.payments_details()
        mpesaresponse = self.make_lnm_request()

        transaction_id = mpesaresponse['CheckoutRequestID']

        payload = {
            "transaction_id": transaction_id,
            "house_id": house_id,
            "amount_paid": amount_payable,
            "billing_id": billing_id
        }


        query = """INSERT INTO payments (transaction_id, date_paid, amount_paid, house_id, billing_id) VALUES (%(transaction_id)s,%(date_paid)s,%(amount_paid)s,%(house_id)s, %(billing_id)s);"""

        cur = self.database.cursor()
        cur.execute(query, payload)
        self.database.commit()

        return jsonify({"message": ("payment for bill: %s successfully posted") % (billing_id)}), 201

    def view_payments(self):
        '''View all payments'''
        try:
            cur = self.database.cursor(cursor_factory=RealDictCursor)
            cur.execute("""  SELECT * FROM payments """)
            data = cur.fetchall()

            if len(data) == 0:
                return jsonify({"message": "no payments made"}), 400

            return jsonify({"payments": data}), 200

        except (psycopg2.Error) as error:
            return jsonify(error)

    def view_payment(self, payment_id):
        '''View individual payment'''
        try:
            cur = self.database.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                """  SELECT * FROM payments WHERE payment_id = '%s' """ % (payment_id))
            data = cur.fetchone()

            if data == None:
                return jsonify({"message": "No payment found"})

            return jsonify({"payment ": data})

        except (psycopg2.Error) as error:
            return jsonify(error)
