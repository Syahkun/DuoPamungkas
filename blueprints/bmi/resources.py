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
    
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('weight', location='args', default=None)
        parser.add_argument('height', location='args', default=None)
        parser.add_argument('umur', location='args', default=None)
        parser.add_argument('gender', location='args', default=None)
        args = parser.parse_args()
        
        #check ion lat from ip
        querystring = {
            "weight": args['weight'],
            "height": args['height']
            }

        headers = {
            'x-rapidapi-host': app.config['X_RAPIDAPI_HOST'],
            'x-rapidapi-key': app.config['X_RAPIDAPI_APIKEY']
            }
        
        response = requests.request("GET", ('https://' + headers['x-rapidapi-host'] + '/bmi'), headers=headers, params=querystring)
        status_health = response.json()['status']
        respon = {
            'weight': args['weight'],
            'height': args['height'],
            'umur': args['umur'],
            'gender': args['gender'],
            'status_health': status_health
        }
        
        return respon

api.add_resource(GetBmi, '')