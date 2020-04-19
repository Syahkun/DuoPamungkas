import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
import json
from blueprints import app

import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

bp_bmi = Blueprint('bmi', __name__)
api = Api(bp_bmi)

class GetBmi(Resource):
  
    host = "gabamnml-health-v1.p.rapidapi.com"
    key = "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79"
   
    
    headers_resep = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79"
    }
    
    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('weight', location='args', default=None)
        parser.add_argument('height', location='args', default=None)
        parser.add_argument('umur', location='args', default=None)
        parser.add_argument('gender', location='args', default=None)
        args = parser.parse_args()
        
        #check ion lat from ip
        querystring = {"weight": args['weight'],"height": args['height']}
        headers = {
            'x-rapidapi-host': app.config['X_RAPIDAPI_HOST'],
            'x-rapidapi-key': app.config['X_RAPIDAPI_APIKEY']
            }
        
        response = requests.request('GET', headers['x-rapidapi-host'] + '/bmi', headers=headers, params=querystring)
        status = response.json()['status']
        
        # pengolahan bmi
        if args['gender'] == "M":
            BMR = 66 + (13.86*float(args['weight'])) + (5.03*float(args['height'])) - (6.8*float(args['umur']))
        else:
            BMR = 655 + (9.46*float(args['weight'])) + (1.83*float(args['height'])) - (4.7*float(args['umur']))

        if status == "Overweight":
            BMR *= 0.6
        elif status == "Low":
            BMR *= 1.8
        elif status == "Normal":
            BMR *= 1.2
        
        #get menu

        querystring = {"targetCalories": BMR, "timeFrame":"day"}

        headers = {
            'x-rapidapi-host': app.config['X_RAPIDAPI_HOST_2'],
            'x-rapidapi-key':  app.config['X_RAPIDAPI_APIKEY_2']
            }

        response = requests.request('GET', headers['x-rapidapi-host_2'] + '/recipes/mealplans/generate', headers=headers, params=querystring)

        # print(json.dumps(response.json(), indent=2))
        
        return json.dumps(response.json())

api.add_resource(GetBmi, '')