import pytest
from blueprints import app
from app import cache, logging
from flask import Flask, request, json
from blueprints.client.resources import Clients
from blueprints.user.resources import Users



from blueprints import db
import hashlib, uuid

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    db.drop_all()
    db.create_all()

    salt = uuid.uuid4().hex
    encoded = ('%s%s' % ("th1s1s1nt3n4lcl13nt", salt)).encode('utf-8')
    hash_pass = hashlib.sha512(encoded).hexdigest()
    
    salt2 = uuid.uuid4().hex
    encoded2 = ('%s%s' % ("alterra", salt2)).encode('utf-8')
    hash_pass2 = hashlib.sha512(encoded2).hexdigest()

    client_internal = Clients(client_key="internal", client_secret=hash_pass, status="True", salt=salt)
    client_noninternal = Clients(client_key="asa", client_secret=hash_pass2, status="False", salt=salt2)
    db.session.add(client_internal)
    db.session.add(client_noninternal)
    db.session.commit()

    user = Users(name="andre", age=23, sex="Female", weight= 97, height=167, food='olives')

    db.session.add(user)
    db.session.commit()

    yield db

def create_token():
    token = cache.get('test-token')
    if token is None:
        data = {
            'client_key': 'internal',
            'client_secret': 'th1s1s1nt3n4lcl13nt'
        }

        req = call_client(request)
        res = req.get(
            '/auth', 
            query_string=data, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200

        cache.set('test-token', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token
