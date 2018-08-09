"""
    Created by zltningx on 18-4-28.
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'GS&@G*SH@E}PD)AN!KF(#+@'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQL_BASE = os.path.join(basedir, 'data.sqlite')

    ADMIN = os.environ.get("ADMIN") or 'admin'

    ADMIN_PASSWORD = os.environ.get("PASSWORD") or 'admin'

    @staticmethod
    def __init__(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("TEST_DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

config = {
    'test': TestConfig,
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}