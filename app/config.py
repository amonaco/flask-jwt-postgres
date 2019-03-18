import os, datetime

DEBUG = False
ENV = 'development'

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/auth'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads
THREADS_PER_PAGE = 2

# Cross-site request forgery
CSRF_ENABLED = True

# Unique secret key
CSRF_SESSION_KEY = "fba668b2aa341c660032aa9492840ecf"

# Secret key for signing cookies
SECRET_KEY = "d41d8cd98f00b204e9800998ecf8427e"

# JWT stuff
JWT_SECRET_KEY = 'f9a5112f32a14a39aeef19e8874a9ee7'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=5)
