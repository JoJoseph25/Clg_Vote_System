import redis


import redis
from flask import Flask

from .runtime.extensions import db, toolbar, jwt, api
from .runtime.config import config_by_name
from .resources.user import User, UserList, UserLogout, UserSingup, UserLogin, TokenRefresh
from .resources.candidate import Candidate, CandidateRegister, CandidateList, Post, PostList



def create_app(config_name):
	app = Flask(__name__)

	with app.app_context():
		# to make commnads work
  
		app.config.from_object(config_by_name[config_name])
		db.init_app(app)
		toolbar.init_app(app)
		
		jwt.init_app(app)
		
		# redis databse
		# Setup our redis connection for storing the blocklisted tokens. You will probably
		# want your redis instance configured to persist data to disk, so that a restart
		# does not cause your application to forget that a JWT was revoked.
		app.jwt_redis_blocklist = redis.StrictRedis(
			host=app.config["REDDIS_HOST"], port=app.config["REDIS_PORT"], db=0, decode_responses=True
		)


		# Callback function to check if a JWT exists in the redis blocklist
		@jwt.token_in_blocklist_loader
		def check_if_token_is_revoked(jwt_header, jwt_payload):
			jti = jwt_payload["jti"]
			token_in_redis = app.jwt_redis_blocklist.get(jti)
			return token_in_redis is not None
		
		# The following callbacks are used for customizing jwt response/error messages.
		# The original ones may not be in a very pretty format (opinionated)
		@jwt.expired_token_loader
		def expired_token_callback():
			output = {
				'message': 'The token has expired.',
				'error': 'token_expired'
				}
			return output, 401 # Staus-Unauthorized


		@jwt.invalid_token_loader
		def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
			output = {
				'message': 'Signature verification failed.',
				'error': 'invalid_token'
				}
			return output, 401 # Staus-Unauthorized

		@jwt.unauthorized_loader
		def missing_token_callback(error):
			output = {
				"description": "Request does not contain an access token.",
				'error': 'authorization_required'
				}
			return output, 401 # Staus-Unauthorized

		@jwt.needs_fresh_token_loader
		def token_not_fresh_callback():
			output = {
				"description": "The token is not fresh.",
				'error': 'fresh_token_required'
				}
			return output, 401 # Staus-Unauthorized

		@jwt.revoked_token_loader
		def revoked_token_callback(jwt_header, jwt_payload):
			output = {
				"description": "The token has been revoked.",
				'error': 'token_revoked'
				}
			return output, 401 # Staus-Unauthorized

		# Define API's endpoints

		# User API endpoints
		api.add_resource(UserList,'/users')
		api.add_resource(User, '/user/<int:roll_num>')
		api.add_resource(UserSingup, '/signup')
		api.add_resource(UserLogin, '/login')
		api.add_resource(UserLogout, '/logout')
		api.add_resource(TokenRefresh, '/refresh')

		# Candidate API endpoints
		api.add_resource(Post,'/post/<int:post_num>')
		api.add_resource(PostList,'/posts')
		api.add_resource(Candidate,'/candidate/<int:candidate_id>')
		api.add_resource(CandidateRegister,'/reg_candidate')
		api.add_resource(CandidateList, '/candidates')

		api.init_app(app)
	return app