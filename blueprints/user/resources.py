import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Users 
from blueprints import db, app
from sqlalchemy import desc
from blueprints import internal_required


bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):
    
    def __init__(self):
        pass
    
    @internal_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', location='json')
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json')
        parser.add_argument('sex', location='json')
        args = parser.parse_args()

        user = Users(args['client_id'], args['name'], args['age'], args['sex'])
        db.session.add(user)
        db.session.commit()
        
        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}
    
    @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int)
        parser.add_argument('sex', location='json')
        data = parser.parse_args()
        
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        qry.name = data['name']
        qry.age = data['age']
        qry.sex = data['sex']
        db.session.commit()
        
        return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}
    
    @internal_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        db.session.delete(qry)
        db.session.commit()
        
        return {'status': 'DELETED'}, 200

class UserList(Resource):
    
    def __init__(self):
        pass
    
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('name', location='args', help='invalid status')
        parser.add_argument('age', location='args', help='invalid status')
        parser.add_argument('orderby', location='args', help='invalid status', choices=('name', 'age'))
        parser.add_argument('sort', location='args', help='invalid status', choices=('desc', 'asc'))
        
        
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = Users.query 
        
        if args['name'] is not None:
            qry = qry.filter_by(name=args['name'])
        
        if args['age'] is not None:
            qry = qry.filter_by(age=args['age'])
        
        if args['orderby'] is not None:
            if args['orderby'] == 'name':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.name))
                else:
                    qry = qry.order_by(Users.name)
            elif args['orderby'] == 'age':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.age))
                else:
                    qry = qry.order_by(Users.age)
        
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))  
            
        return rows, 200

api.add_resource(UserList, '', '/list')    
api.add_resource(UserResource, '', '/<id>')
