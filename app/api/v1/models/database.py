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
            confirm_password character varying(1000) NOT NULL
            house_id serial FOREIGN KEY NOT NULL);
            """

    landlord = """CREATE TABLE IF NOT EXISTS landlord (
            landlord_id serial PRIMARY KEY NOT NULL,
            firstname character varying(255) NOT NULL,
            lastname character varying(255) NOT NULL,
            phonenumber character varying(255) NOT NULL,
            email character varying(255) NOT NULL,
            password character varying(255) NOT NULL,
            confirm_password character varying(255) NOT NULL
            );"""

    Property = """CREATE TABLE IF NOT EXISTS property (
            property_id serial PRIMARY KEY NOT NULL,
            property_name character varying(255) NOT NULL,
            landlord_id serial FOREIGN KEY NOT NULL;"""

    houses = """CREATE TABLE IF NOT EXISTS houses (
            house_id serial PRIMARY KEY NOT NULL,
            house_no integer varying(50) NOT NULL,
            house_type character varying(50) NOT NULL,
            rent_amount integer varying(255) NOT NULL,
            property_id serial FOREIGN KEY NOT NULL);"""

    payments = """CREATE TABLE IF NOT EXISTS payments (
            payment_id serial PRIMARY KEY NOT NULL,
            amount_paid integer varying(255) NOT NULL,
            date_paid character varying(50) NOT NULL,
            transaction_id character varying(255) NOT NULL,
            billing_id serial FOREIGN KEY NOT NULL);"""

    billing = """CREATE TABLE IF NOT EXISTS billing (
            billing_id serial PRIMARY KEY NOT NULL,
            amount_payable integer varying(255) NOT NULL,
            house_id serial FOREIGN KEY NOT NULL);"""

    complaints = """CREATE TABLE IF NOT EXISTS complaints (
            complaint_id serial PRIMARY KEY NOT NULL,
            title character varying(255) NOT NULL,
            description character varying(255) NOT NULL,
            date character varying(255) NOT NULL,
            tenant_id serial FOREIGN KEY NOT NULL;"""

    queries = [tenants, landlord, payments, billing, complaints, houses, Property]

    return queries