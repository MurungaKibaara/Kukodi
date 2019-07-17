'''App Configurations'''
import os

class Config(object):
    """Main Configurations"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(24)


class DevelopmentConfig(Config):
    """Development Configurations"""
    DEBUG = True
    DATABASE_NAME = "kukodi"
    DATABASE_URL = os.getenv("DATABASE")

class ProductionConfig(Config):
    """Production Configurations"""
    DEBUG = False

APP_CONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}