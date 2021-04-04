import os

# load the environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_ENV = 'development'
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='A very terrible secret key.')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    

    #SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.getenv('PROD_DATABASE_USERNAME')}:{os.getenv('PROD_DATABASE_PASSWORD')}@{os.getenv('PROD_DATABASE_ENDPOINT')}/'taskmasterproduction'"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'dev.sqlite')
    

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'test.sqlite')

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.getenv('PROD_DATABASE_USERNAME')}:{os.getenv('PROD_DATABASE_PASSWORD')}@{os.getenv('PROD_DATABASE_ENDPOINT')}/taskmasterproduction"

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
}
