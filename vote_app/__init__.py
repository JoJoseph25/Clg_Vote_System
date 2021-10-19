from flask import Flask
from .runtime.extensions import db, toolbar, jwt, api
from .runtime.config import config_by_name
from .resources.user import User, UserSingup, UserLogin, TokenRefresh




def create_app(config_name):
	app = Flask(__name__)

	with app.app_context():
		# to make commnads work
  
		app.config.from_object(config_by_name[config_name])
		db.init_app(app)
		toolbar.init_app(app)
		jwt.init_app(app)

		api.init_app(app)
		api.add_resource(User, '/user/<int:roll_num>')
		api.add_resource(UserSingup, '/signup')
		api.add_resource(UserLogin, '/login')
		api.add_resource(TokenRefresh, '/refresh')

	return app