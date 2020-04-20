import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Clients
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
# from blueprints import internal_required


bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    def __init__(self):
        pass
    
    @internal_required
    def get(self, id):
        qry = Clients.query.get(id)
        if qry is not None:
            return marshal(qry, Clients.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json')
        parser.add_argument('status', location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['client_secret'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()
        
        result = Clients(args['client_key'], hash_pass, args['status'], salt)
        
        db.session.add(result)
        db.session.commit()

        return marshal(result, Clients.response_fields), 200, {'Content-Type': 'application/json'}
    
    @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json')
        parser.add_argument('status', location='json')
        data = parser.parse_args()
        
        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        encoded = ('%s%s' % (data['client_secret'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()
        
        qry.client_key = data['client_key']
        qry.client_secret = hash_pass
        qry.status = data['status']
        db.session.commit()
        
        return marshal(qry, Clients.response_fields), 200, {'Content-Type': 'application/json'}
    
    @internal_required
    def delete(self, id):
        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        db.session.delete(qry)
        db.session.commit()
        
        return {'status': 'DELETED'}, 200
    
    @internal_required
    def patch(self):
        return 'Not yet implemented', 501

class ClientList(Resource):
    @internal_required
    def __init__(self):
        pass
    
    @internal_required
    def get(self):        # parser.add_argument('client_name', location='json', required=True)ocation='args', default=1)
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('status', location='args', choices=('true', 'false', 'True', 'False'))
        parser.add_argument('orderby', location='args', help='invalid status', choices=('id', 'status'))
        parser.add_argument('sort', location='args', help='invalid status', choices=('desc', 'asc'))
        
        
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = Clients.query 
        
        if args['id'] is not None:
            qry = qry.filter_by(id=args['id'])
            
        if args['status'] is  not None:
            qry = qry.filter_by(status=True if args['status'].lower() == 'true' else False)
        
        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.id))
                else:
                    qry = qry.order_by(Clients.id)
            elif args['orderby'] == 'status':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.status))
                else:
                    qry = qry.order_by(Clients.status)
        
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Clients.response_fields))  
            
        return rows, 200

api.add_resource(ClientList, '', '/list')    
api.add_resource(ClientResource, '', '/<id>')
