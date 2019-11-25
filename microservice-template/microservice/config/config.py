# Configuration script
# Retrieves the hidden variables from the .env
# file and creates the configuration objects -
# one for each environment.

from dotenv import load_dotenv
load_dotenv()

import os

class Config(object):
    DEBUG = False
    TESTING = False
    CORS = {
        'origins': os.getenv('CORS_ORIGINS').split(',') if os.getenv('CORS_ORIGINS') else None
    }


class ProductionConfig(Config):
    """Production configuration"""


    # done
    ENV='production'
    SECRET_KEY=os.getenv('PROD_SECRET_KEY')
    DATABASE={
        'database': os.getenv('PROD_PG_DATABASE'),
        'password': os.getenv('PROD_PG_PASSWORD')
    }


class DevelopmentConfig(Config):
    """Development configuration"""

    # done
    ENV='development'
    DEBUG = True
    SECRET_KEY=os.getenv('DEV_SECRET_KEY')
    DATABASE={
        'database': os.getenv('DEV_PG_DATABASE'),
        'password': os.getenv('DEV_PG_PASSWORD')
    }


class TestingConfig(Config):
    """Testing configuration"""

    # done
    ENV='testing'
    TESTING = True
    SECRET_KEY=os.getenv('TEST_SECRET_KEY')
    DATABASE={
        'database': os.getenv('TEST_PG_DATABASE'),
        'password': os.getenv('TEST_PG_PASSWORD')
