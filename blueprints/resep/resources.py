import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
import json
from blueprints import app
from blueprints.bmi.resources import GetBmi

import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

bp_resep = Blueprint('resep', __name__)
api = Api(bp_resep)

class GetResep(Resource):
    
    # @jwt_required
    def get(self):
        GetBmi()

        x = GetBmi().get()
        
        if x['gender'] == "M":
            BMR = 66 + (13.86*float(x['weight'])) + (5.03*float(x['height'])) - (6.8*float(x['umur']))
        else:
            BMR = 655 + (9.46*float(x['weight'])) + (1.83*float(x['height'])) - (4.7*float(x['umur']))

        if x['status_health'] == "Overweight":
            BMR *= 0.6
        elif x['status_health'] == "Low":
            BMR *= 1.8
        elif x['status_health'] == "Normal":
            BMR *= 1.2
        
        ## get menu API 2

        querystring = {"targetCalories": BMR, "timeFrame":"day"}

        headers = {
            'x-rapidapi-host': app.config['X_RAPIDAPI_HOST_2'],
            'x-rapidapi-key':  app.config['X_RAPIDAPI_APIKEY_2']
            }

        response = requests.request('GET', 'https://' + headers['x-rapidapi-host'] + '/recipes/mealplans/generate', headers=headers, params=querystring)
        
        return response.json()

api.add_resource(GetResep, '')