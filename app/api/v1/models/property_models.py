'''Properties model: Class to manage property data'''
import datetime
import psycopg2
from psycopg2.extras import DictCursor
from flask import jsonify, request
from app.api.v1.models.database import init_db

INIT_DB = init_db()

class PropertyRecords():
    """ Create a model that stores property data"""

    def __init__(self):
        """initialize the database and argument variables"""
        self.database = INIT_DB

    def register_property(self, property_name):
        """ Add a new property """

        payload = {
            "property_name": property_name,
        }

        query = """INSERT INTO properties (property_name) VALUES (%(property_name)s);"""

        cur = self.database.cursor()
        cur.execute(query, payload)
        self.database.commit()

        return jsonify({"message": ("property %s successfully registered")%(property_name)}), 201

    def view_properties(self, property_id):
        '''sign in a tenant'''
        try:
            cur = INIT_DB.cursor(cursor_factory=DictCursor)
            cur.execute("""  SELECT * FROM properties """)
            data = cur.fetchall()

            if len(data) == 0:
                return jsonify({"message":"no properties found"})

            return jsonify({"properties": data})

        except (psycopg2.Error) as error:
            return jsonify(error)

    def view_property(self, property_id):
        '''sign in a tenant'''
        try:
            cur = INIT_DB.cursor(cursor_factory=DictCursor)
            cur.execute("""  SELECT * FROM properties WHERE property_id = '%s' """ % (property_id))
            data = cur.fetchone()

            if data is None:
                return jsonify({"message":"property does not exist"})

            return jsonify({"property ": data})

        except (psycopg2.Error) as error:
            return jsonify(error)
