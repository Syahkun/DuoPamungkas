from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


Base = declarative_base()

class Users(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    food = db.Column(db.String(100), default="donut")
    
    response_fields = {
        'id': fields.Integer,
        'client_id': fields.Integer,
        'name': fields.String,
        'age':fields.Integer,
        'sex': fields.String,
        'weight': fields.Integer,
        'height': fields.Integer,
        'food': fields.String
    }

    def __init__(self, name, age, sex, weight, height, food, client_id=2):
        self.client_id = client_id
        self.name = name
        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height
        self.food = food

    def __repr__(self):
        return '<User %r>' % self.id
    