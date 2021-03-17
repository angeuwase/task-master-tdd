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
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}")

class ProductionConfig(Config):
    FLASK_ENV = 'production'