from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
from flask_debugtoolbar import DebugToolbarExtension

# Database
db = SQLAlchemy()


# Debug toolbar
toolbar = DebugToolbarExtension()

# create API
api = Api()

# JWT Manager
jwt = JWTManager()

# API Docs
docs = FlaskApiSpec()

