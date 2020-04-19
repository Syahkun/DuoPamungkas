import json, config, os

from datetime import timedelta
from functools import wraps

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

app = Flask(__name__)


jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] == "False":
            return {'status': 'FORBIDDEN', 'message': 'Internal only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

if os.environ.get('FLASK_ENV', 'Production') == "Production" :
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.DevelopmentConfig)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



@app.after_request
def after_request(response):
    try:
        requestData = request.get.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
                           json.dumps({ 
                                       'request' : request.args.to_dict(),
                                       'response': json.loads(response.data.decode("utf-8"))
                                       })
                           )
    else:
        app.logger.error("")
    return response
from blueprints.user.resources import bp_user
from blueprints.client.resources import bp_client
from blueprints.auth import bp_auth
from blueprints.bmi.resources import bp_bmi

app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_client, url_prefix='/client')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_bmi, url_prefix='/bmi')
db.create_all()