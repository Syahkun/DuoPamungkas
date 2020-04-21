from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class Clients(db.Model):
    __tablename__= "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(50), unique=True, nullable=False)
    client_secret = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    status = db.Column(db.String(30), default=0)
    users = db.relationship('Users', backref='clients', lazy=True, uselist=False)

    
    response_fields = {
        'id': fields.Integer,
        'client_key': fields.String,
        'client_secret': fields.String,
        'status':fields.String
    }
    
    jwt_claims_fields = {
        'client_key': fields.String,
        'status': fields.String
    }

#urutan ini harus sesuai dengan def post result
    def __init__(self, client_key, client_secret, status, salt):
        self.client_key = client_key
        self.status = status
        self.client_secret = client_secret
        self.salt = salt
        
    def __repr__(self):
        return '<Client %r>' % self.id
    