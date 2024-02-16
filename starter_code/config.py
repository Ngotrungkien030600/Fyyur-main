import os

SECRET_KEY = os.urandom(32)
WTF_CSRF_ENABLED = False

# Enable debug mode.
DEBUG = True

# Define the base directory.
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration.
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
