#!/usr/bin/python
"""Configuration loader"""

import os
import logging


class Config(object):
    """Defaults"""
    DEBUG=False
    TESTING=False
    SERVER_NAME = os.environ['SERVER_NAME']
    PERMANENT_SESSION = os.environ['PERMANENT_SESSION']
    PERMANENT_SESSION_LIFETIME = int(os.environ['PERMANENT_SESSION_LIFETIME'])
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    LOGGER_NAME = "jeffbryner.com"
    PREFERRED_URL_SCHEME = 'https'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
