import json
import os
from flask_pymongo import PyMongo
from influxdb import InfluxDBClient
from app import app


#Connect to db using environment variables
CLIENT = InfluxDBClient('influxdb', 8086, os.environ['INFLUXDB_USERNAME'], os.environ['INFLUXDB_PASSWORD'], os.environ['INFLUXDB_DATABASE'])


def send_data(data):
    '''Send a single json object to the database'''

    data_to_send = []
    add_db_info = {}

    add_db_info['measurement'] = "Rpi_data"
    add_db_info['fields'] = data

    data_to_send.append(add_db_info)

    print(f'Send to DB: {data_to_send}', flush=True)

    try:
        CLIENT.write_points(data_to_send)
    except:
        print("Failed to send to database")
