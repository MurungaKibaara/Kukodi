'''App Configurations'''
import os

class Config(object):
    """Main Configurations"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'xac,oj\xd4$\xee\x13\xdezZI\xf2\x9b\xd6`\x1e_"\xb1\x1ey\xc1I'


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