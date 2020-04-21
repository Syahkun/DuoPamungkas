from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

import hashlib, uuid
from blueprints import internal_required
from ..client.model import Clients

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args',required=True)
        parser.add_argument('client_secret',location='args', required=True)
        args = parser.parse_args()
        
        qry = Clients.query.filter_by(client_key=args['client_key']).first()
        if qry is not None:
            encoded = ('%s%s' % (args['client_secret'], qry.salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            
            if hash_pass == qry.client_secret:
                qry = marshal(qry, Clients.jwt_claim_fields)
                if args['client_key'] == 'internal' and args['client_secret'] == 'th1s1s1nt3n4lcl13nt':
                    qry = {
                        'identifier': 'alta batch 5',
                        'status': "True"
                    }
                    token = create_access_token(identity=args['client_key'], user_claims=qry)
                    return {'token':token}, 200
                else:
                    qry['identifier'] = 'alta batch 5'
                    qry['status'] = "False"
                    token = create_access_token(identity=args['client_key'], user_claims=qry)
                    return {'token':token}, 200
        else:
            return  {'status':'UNAUTHORIZED', 'message': 'invalid key or secret'}, 404

class RefreshTokenResource(Resource):
    
    @internal_required
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt_claims()
        token = create_access_token(identity=current_user, user_claims=claims)
        return {'token':token, 'claims':claims}, 200

api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')
