'''Properties model: Class to manage property data'''
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

class PropertyRecords():
    """ Create a model that stores property data"""

    def __init__(self):
        """initialize the database and argument variables"""
        self.database = INIT_DB

    def register_property(self, property_name):
        """ Add a new property """

        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split( )[1]
        
        decoded_token = jwt.decode(auth_token, JWT_SECRET, algorithms='HS256')
        landlord_id = decoded_token['sub']

        payload = {
            "property_name": property_name,
            "landlord_id": landlord_id
        }


        query = """INSERT INTO property (property_name, landlord_id) VALUES (%(property_name)s, %(landlord_id)s);"""


        cur = self.database.cursor()
        cur.execute(query, payload)
        self.database.commit()

        return jsonify({"message": ("property %s successfully registered")%(property_name)}), 201

    def view_properties(self):
        '''View all properties'''
        try:
            cur = self.database.cursor(cursor_factory=RealDictCursor)
            cur.execute("""  SELECT * FROM property """)
            data = cur.fetchall()

            if len(data) == 0:
                return jsonify({"message":"no properties found"})

            return jsonify({"properties": data})

        except (psycopg2.Error) as error:
            return jsonify({"error":error})

    def view_property(self, property_id):
        '''View a particular property'''
        try:
            cur = self.database.cursor(cursor_factory=RealDictCursor)
            cur.execute("""  SELECT * FROM property WHERE property_id = '%s' """ % (property_id))
            data = cur.fetchone()

            if len(data) is None:
                return jsonify({"message":"property does not exist"})

            return jsonify({"property ": data})

        except (psycopg2.Error) as error:
            return jsonify({"error":error})
    
    def view_property_by_name(self, property_name):
        '''View a particular property by name(To allow for search)'''
        try:
            cur = self.database.cursor(cursor_factory=RealDictCursor)
            cur.execute("""  SELECT * FROM property WHERE property_name = '%s' """ % (property_name))
            data = cur.fetchone()

            if data == None:
                return jsonify({"message":"property does not exist"})

            return jsonify({"property ": data})

        except (psycopg2.Error) as error:
            return jsonify({"error":error})