import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
import json
from blueprints import app
from ..user.model import Users
from blueprints import internal_required

import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

bp_bmi = Blueprint('bmi', __name__)
api = Api(bp_bmi)

class GetBmi(Resource):
    
    @internal_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:

            querystring = {
                "weight": qry.weight,
                "height": qry.height
                }

            headers = {
                'x-rapidapi-host': app.config['X_RAPIDAPI_HOST'],
                'x-rapidapi-key': app.config['X_RAPIDAPI_APIKEY']
                }
            
            response = requests.request("GET", ('https://' + headers['x-rapidapi-host'] + '/bmi'), headers=headers, params=querystring)
            status_health = response.json()['status']
            respon = {
                'weight': qry.weight,
                'height': qry.height,
                'umur': qry.age,
                'gender': qry.sex,
                'status_health': status_health
            }
        
            return respon

api.add_resource(GetBmi, '/<id>')