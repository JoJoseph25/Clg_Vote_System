from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity, jwt_required


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
_user_parse.add_argument('password_hash',
						type=str,
						required=True,
						help="This field cannot be blank."
						)
_user_parse.add_argument('admin',
						type=int,
						required=False
						)


class UserSingup(Resource):
	def post(self):
		data = _user_parse.parse_args()
		
		if UserModel.find_by_rollnum(data['roll_num']):
			output = {"message":"Roll num already registered by another user"}
			return output, 400 #Status-Bad Request
		
		user = UserModel(roll_num=data['roll_num'], name=data['name'], email=data['email'], password_hash=['password_hash'])
		user.db_write()
		
		output = {"message":"User Registered Sucessfully"}
		return output, 200 # Status-OK

class UserLogin(Resource):
	def post(self):
		data = _user_parse.parse_args()

		user = UserModel.find_by_rollnum(data['roll_num'])

		# User Present and password correct
		if user is not None and UserModel.check_password(data['password']):          
			access_token = create_access_token(identity=user.id, fresh=True) 
			refresh_token = create_refresh_token(user.id)
			output = {
				'access_token': access_token,
				'refresh_token': refresh_token
			}
			return output, 200 # Status-OK
		
		output = {"message": "Invalid User Credentials!"}
		return output, 401 # Status-Unauthorized

class TokenRefresh(Resource):
	@jwt_required(refresh=True)
	def post(self):
		"""
		Return a new acess token without logging in again with the 'refresh token'
		stored during inital login.
		"""

		current_user = get_jwt_identity()
		new_token = create_access_token(identity=current_user, fresh=False)
		output = {'access_token': new_token}

		return output, 200 # Status-OK


class User(Resource):
	
	@classmethod
	def get(cls, roll_num: int):
		user = UserModel.find_by_rollnum(roll_num)
		
		if user is None:
			output = {'message': 'User Not Found'}
			return output, 404 # Status-Not Found

		output = user.json() # get user data
		return output, 200 # Status-OK

	@jwt_required()
	def delete(roll_num: int):
		user = UserModel.find_by_rollnum(roll_num)
		
		if user is None:
			output = {'message': 'User Not Found'}
			return output, 404 # Status-Not Found
		
		user.db_pop()
		output = {'message': 'User deleted.'}
		return output, 200 # Status-OK

	# only used for update
	@jwt_required()
	def put(roll_num: int):
		data = _user_parse.parser.parse_args()

		user = UserModel.find_by_rollnum(roll_num)

		if user is None:
			output = {'message': 'User Not Found'}
			return output, 404 # Status-Not Found

		# User present in Db and update only name or password
		else: 
			user.name = data['name']
			user.password_hash = data['password_hash']

		user.db_write()
		output = user.json()

		return output, 200 # Status-OK


		