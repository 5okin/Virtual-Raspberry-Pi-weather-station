import json
from flask import Flask, request, url_for, render_template
from flask_restful import Resource, Api
from app.services import data_process, database_handle
from flask_pymongo import PyMongo
from app import app


#Create the API
API = Api(app)

#Keeps every measurment received by server for 5 min.
MEASUREMENTS = []


@app.route("/")
def index():
    return render_template('index.html', data=MEASUREMENTS)


class ReceiveMeasurments(Resource):
    '''Receives and handles data send to api'''

    def put(self):
        new_data = json.loads(request.get_json())
        MEASUREMENTS.append(new_data.copy())
        data_process.process(MEASUREMENTS)
        database_handle.send_data(new_data.copy())
        return 200

API.add_resource(ReceiveMeasurments, '/api/send')
