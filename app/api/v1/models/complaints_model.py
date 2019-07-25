'''model to handle complaints data'''
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import jwt
from flask import jsonify, request
from app.api.v1.models.database import init_db
from app.api.v1.models.landlord_models import token_verification
from instance.config import Config
JWT_SECRET = Config.SECRET_KEY

INIT_DB = init_db()

class ComplaintsRecords():
    """ Create a model to handle complaints data"""

    def __init__(self):
        """initialize the database and argument variables"""
        self.database = INIT_DB

    def complaint(self, title, description):
        """ Add a new complaint """

        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split( )[1]
        
        decoded_token = jwt.decode(auth_token, JWT_SECRET, algorithms='HS256')
        tenant_id = decoded_token['sub']

        date = datetime.datetime.now()

        payload = {
            "title": title,
            "description": description,
            "date":date,
            "tenant_id": tenant_id
        }

        query = """INSERT INTO complaints (title, description, date, tenant_id) VALUES (%(title)s, %(description)s, , %(date)s, , %(tenant_id)s);"""

        cur = self.database.cursor()
        cur.execute(query, payload)
        self.database.commit()

        return jsonify({"message": ("complaint %s posted")%(title)}), 201

    def view_complaints(self):
        '''View all complaints'''
        try:
            cur = self.database.cursor(cursor_factory=RealDictCursor)
            cur.execute("""  SELECT * FROM complaints """)
            data = cur.fetchall()

            if len(data) == 0:
                return jsonify({"message":"You're doing a good job, no complaints found!"})

            return jsonify({"complaints": data}), 400

        except (psycopg2.Error) as error:
            return jsonify(str(error))

    def view_complaint(self, complaint_id):
        '''View a particular complaint'''
        try:
            cur = self.database.cursor(cursor_factory=RealDictCursor)
            cur.execute("""  SELECT * FROM complaints WHERE complaint_id = '%s' """ % (complaint_id))
            data = cur.fetchone()

            if data == None:
                return jsonify({"message":"no complaints found"}), 400

            return jsonify({"complaints ": data})

        except (psycopg2.Error) as error:
            return jsonify(str(error))
