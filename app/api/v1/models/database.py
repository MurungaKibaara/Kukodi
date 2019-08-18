'''Postgres Database connection model'''
import os
import psycopg2
from flask import jsonify

DB_URL = os.getenv('DATABASE')

def init_db():
    '''Connecting to the DB'''
    conn = psycopg2.connect(DB_URL)
    return conn

def create_tables():
    '''Function for creating tables in database'''
    conn = init_db()
    cur = conn.cursor()
    queries = tables()

    for query in queries:
        cur.execute(query)
        conn.commit()

def tables():
    '''Function to define the tables'''
    tenants = """CREATE TABLE IF NOT EXISTS tenants(
            tenant_id serial PRIMARY KEY NOT NULL,
            firstname character varying(1000) NOT NULL,
            lastname character varying(1000) NOT NULL,
            phonenumber character varying(1000) NOT NULL,
            email character varying(1000) NOT NULL,
            password character varying(1000) NOT NULL,
            house_no character varying(50) NOT NULL UNIQUE,
            house_id integer default null,
            FOREIGN KEY(house_id) REFERENCES houses(house_id));
            """

    landlord = """CREATE TABLE IF NOT EXISTS landlord (
            landlord_id serial PRIMARY KEY,
            firstname character varying(255) NOT NULL UNIQUE,
            lastname character varying(255) NOT NULL UNIQUE,
            phonenumber character varying(255) NOT NULL UNIQUE,
            email character varying(255) NOT NULL UNIQUE,
            password character varying(255) NOT NULL UNIQUE);"""

    properties = """CREATE TABLE IF NOT EXISTS property (
            property_id serial PRIMARY KEY NOT NULL UNIQUE,
            property_name character varying(255) NOT NULL,
            landlord_id integer default null,
            FOREIGN KEY(landlord_id) REFERENCES landlord(landlord_id));"""

    houses = """CREATE TABLE IF NOT EXISTS houses (
            house_id serial PRIMARY KEY NOT NULL UNIQUE,
            house_no character varying(50) NOT NULL UNIQUE,
            house_type character varying(50) NOT NULL,
            rent_amount integer NOT NULL,
            property_id integer default null,
            FOREIGN KEY(property_id) REFERENCES property(property_id));"""

    payments = """CREATE TABLE IF NOT EXISTS payments (
            payment_id serial PRIMARY KEY NOT NULL UNIQUE,
            amount_paid integer NOT NULL,
            date_paid DATE NOT NULL DEFAULT CURRENT_DATE,
            transaction_id character varying(255) NOT NULL,
            billing_id character(50) default null,
            FOREIGN KEY(billing_id) REFERENCES billing(billing_id));"""

    billing = """CREATE TABLE IF NOT EXISTS billing (
            billing_id character(50) PRIMARY KEY NOT NULL UNIQUE,
            amount_payable integer NOT NULL,
            house_id integer default null,
            FOREIGN KEY(house_id) REFERENCES houses(house_id));"""

    complaints = """CREATE TABLE IF NOT EXISTS complaints (
            complaint_id serial PRIMARY KEY NOT NULL UNIQUE,
            title character varying(255) NOT NULL,
            description character varying(255) NOT NULL,
            date DATE NOT NULL DEFAULT CURRENT_DATE,
            tenant_id integer default null,
            FOREIGN KEY(tenant_id) REFERENCES tenants(tenant_id) );"""

    queries = [landlord, properties, houses, tenants, billing, payments, complaints]

    return queries