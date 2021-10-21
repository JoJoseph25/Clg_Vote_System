from datetime import timedelta

from flask import current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity, jwt_required, get_jwt

from vote_app.runtime.config import Config
from vote_app.models.user import UserModel


_user_parse = reqparse.RequestParser()
_user_parse.add_argument('roll_num',
						type=int,
						required=True,
						help="This field cannot be blank."
						)
_user_parse.add_argument('name',
						type=str,
						required=True,
						help="This field cannot be blank."
						)
_user_parse.add_argument('email',
						type=str,
						required=True,
						help="This field cannot be blank."
						)
_user_parse.add_argument('password',
						type=str,
						required=True,
						help="This field cannot be blank."
						)
_user_parse.add_argument('admin',
						type=int,
						required=False
						)


_user_update_parse = reqparse.RequestParser()
_user_update_parse.add_argument('name',
						type=str,
						required=False,
						help="This field cannot be blank."
						)
_user_update_parse.add_argument('password',
						type=str,
						required=False,
						help="This field cannot be blank."
						)


_login_parse = reqparse.RequestParser()
_login_parse.add_argument('roll_num',
						type=int,
						required=True,
						help="This field cannot be blank."
						)
_login_parse.add_argument('password',
						type=str,
						required=True,
						help="This field cannot be blank."
						)



class UserSingup(Resource):
	def post(self):
		"""
		If roll_num and email are not already registered by another user
		register the user else return Bad Request and message
		"""

		data = _user_parse.parse_args()
		
		# Check Roll Num Unique
		user = UserModel.find_by_rollnum(data['roll_num'])
		if user is not None:
			output = {"message":"Roll num already registered by another user"}
			return output, 400 #Status-Bad Request
		
		# Check Email Unique
		user = UserModel.find_by_email(data['email'])
		if user is not None:
			output = {"message":"Email already used by another user"}
			return output, 400 #Status-Bad Request

		try:
			user = UserModel(roll_num=data['roll_num'], name=data['name'], email=data['email'], password=data['password'])
			user.db_write()

			output = {"message":"User Registered Sucessfully"}
			return output, 200 # Status-OK
		except:
			output = {"message":"Something went wrong"}
			return output, 500 # Status-Internal Server Error
			


class UserLogin(Resource):
	def post(self):
		"""
		If user roll_num and password correct create a new access and refresh token
		else return invalid credentials 401 error
		"""

		data = _login_parse.parse_args()

		user = UserModel.find_by_rollnum(data['roll_num'])

		# User Present and password correct
		if user is not None and user.check_password(data['password']) and user.roll_num==data['roll_num']:
			additional_claims = {"admin_access":user.admin}
			access_token = create_access_token(identity=user.roll_num, additional_claims=additional_claims,fresh=True) 
			refresh_token = create_refresh_token(user.roll_num)
			
			output = {
				'access_token': access_token,
				'refresh_token': refresh_token
			}
			return output, 200 # Status-OK
		
		output = {"message": "Invalid User Credentials!"}
		return output, 401 # Status-Unauthorized



class UserLogout(Resource):
	@jwt_required()
	def delete(self):
		"""
		If user logs out add jwt identifier (jti) to redis
		Set time to live (TTL) to clear out of redis automatically after expires.
		"""

		jti = get_jwt()["jti"]
		try:
			current_app.jwt_redis_blocklist.set(jti, "", ex=Config.JWT_REVOKE_TOKEN_EXPIRES)
			output = {'access_token': " ",
					'refresh_token': " ",
					'message':'Access token revoked'}
			return output, 200 # Status-OK
		except:
			output = {"message":"Something went wrong"}
			return output, 500 # Status-Internal Server Error



class TokenRefresh(Resource):
	@jwt_required(refresh=True)
	def post(self):
		"""
		Return a new access token without logging in again with the 'refresh token'
		stored during inital login.
		"""

		current_user = get_jwt_identity()
		claims = get_jwt()
		new_token = create_access_token(identity=current_user, additional_claims=claims, fresh=False)
		output = {'access_token': new_token}

		return output, 200 # Status-OK



class User(Resource):
	
	@classmethod
	def get(cls, roll_num: int):
		"""
		Returns user based on roll_num if it exist in DB
		else returns status status not found
		"""

		user = UserModel.find_by_rollnum(roll_num)
		
		if user is None:
			output = {'message': 'User Not Found'}
			return output, 404 # Status-Not Found

		output = user.json() # get user data
		return output, 200 # Status-OK

	@jwt_required()
	def delete(self, roll_num: int):
		"""
		Deletes User based on roll_num if present and 
		current user has admin access 
  		else return Not found if user not in DB
		If no admin Acess does not give you ability to delete
		"""

		user = UserModel.find_by_rollnum(roll_num)
		
		if user is None:
			output = {'message': 'User Not Found'}
			return output, 404 # Status-Not Found

		claims = get_jwt()
		if len(claims)!=0:
		# If user is admin give ability to delete
			if claims['admin_access']==1:
				try:
					user.db_pop()
					output = {'message': 'User deleted.'}
					return output, 200 # Status-OK
				except:
					output = {'message': 'Something went wrong'}
					return output, 500 # Status-Internal Server Error
		
		output = {'message': 'Admin Access required'}
		return output, 401 # Status-Unauthorized

	# only used for update
	@jwt_required()
	def put(self, roll_num: int):
		"""
		Updates User based on roll_num if present 
		and current user has same roll_num.
		only updates name or password
		"""
		data = _user_update_parse.parse_args()
		
		user_rollnum = get_jwt_identity()
		user = UserModel.find_by_rollnum(user_rollnum)

		if user is None:
			output = {'message': 'User Not Found'}
			return output, 404 # Status-Not Found
		
		elif user_rollnum!=roll_num:
			output = {'message': 'Can only make changes to your data not other'}
			return output, 401 # Status-Unauthorized
		
		# User present in Db
		else: 
			for attr in data:
				if data[attr] is not None: 
					# Row, Column, New Value
					setattr(user,attr,data[attr])
		try:
			user.db_write()
			output = {'message': 'User data updated'}
			return output, 200 # Status-OK
		except:
			output = {"message":"Something went wrong"}
			return output, 500 # Status-Internal Server Error



class UserList(Resource):
	@jwt_required(optional=True)
	def get(self):
		"""
		If user not logged in only shown name of registered users,
		If logged in show roll_num,name,email of registered users,
		If user has admin acess show everythin related to user except password.
		"""
		
		users = [user.json() for user in UserModel.find_all()]

		claims = get_jwt()
		user_rollnum = get_jwt_identity()
		if user_rollnum:
			# If user is admin show admin view
			if claims['admin_access']==1:
				users = [user.admin_json() for user in UserModel.find_all()]
			# if user not admin use normal view
			output = {'users': users}
			return output, 200 # Status-OK
	
		else:
			output = {'users': [user['name'] for user in users],
					'message': 'More data available if you log in.'}
			return output, 200 # Status-OK