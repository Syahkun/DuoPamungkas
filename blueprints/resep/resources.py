import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
import json
from blueprints import app, internal_required
from blueprints.bmi.resources import GetBmi
from ..user.model import Users

import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

bp_resep = Blueprint('resep', __name__)
api = Api(bp_resep)

class GetResep(Resource):
    
    @internal_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            GetBmi()

            x = GetBmi().get(id)
            
            if qry.sex == "Male":
                BMR = 66 + (13.86*float(qry.weight)) + (5.03*float(qry.height)) - (6.8*float(qry.age))
            else:
                BMR = 655 + (9.46*float(qry.weight)) + (1.83*float(qry.height)) - (4.7*float(qry.age))

            if x['status_health'] == "Overweight":
                BMR *= 0.6
            elif x['status_health'] == "Low":
                BMR *= 1.8
            elif x['status_health'] == "Normal":
                BMR *= 1.2
        
            ## get menu API 2

            querystring = {"timeFrame":"day", "targetCalories": BMR, "exclude": qry.food}

            headers = {
                'x-rapidapi-host': app.config['X_RAPIDAPI_HOST_2'],
                'x-rapidapi-key':  app.config['X_RAPIDAPI_APIKEY_2']
                }

            response = requests.request('GET', 'https://' + headers['x-rapidapi-host'] + '/recipes/mealplans/generate', headers=headers, params=querystring)
            
            return response.json()

        return {'status': 'NOT_FOUND'}, 404
        

api.add_resource(GetResep, '/<id>')