import configparser
from datetime import timedelta 

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

#variabel envirometn yg urgent bnget
class Config():
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = cfg['jwt']['secret_key']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    X_RAPIDAPI_HOST =  cfg['bmi']['bmi_host']
    X_RAPIDAPI_APIKEY = cfg['bmi']['bmi_apikey']
    X_RAPIDAPI_HOST_2 =  cfg['resep']['resep_host']
    X_RAPIDAPI_APIKEY_2 = cfg['resep']['resep_apikey']

#variabel environment yg nggak urgent bngetss  
class DevelopmentConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000
    APP_PORT = 9090
    
class ProductionConfig(Config):
    APP_DEBUG = False
    DEBUG = False
    MAX_BYTES = 10000
    APP_PORT = 5050
    
# class WeatherConfig(Config)
