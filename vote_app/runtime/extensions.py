from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# Database
db = SQLAlchemy()

# Debug toolbar
toolbar = DebugToolbarExtension()

# JWT Manager
jwt = JWTManager()

# create API
api = Api()