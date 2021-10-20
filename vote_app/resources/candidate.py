from datetime import timedelta

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt


from vote_app.models.candidate import CandidateModel


_add_candidate_parse = reqparse.RequestParser()
_add_candidate_parse.add_argument('roll_num',
						type=int,
						required=True,
						help="roll_num-field cannot be blank."
						)
_add_candidate_parse.add_argument('first_name',
						type=str,
						required=True,
						help="first_name-field cannot be blank."
						)
_add_candidate_parse.add_argument('last_name',
						type=str,
						required=True,
						help="last_name-field cannot be blank."
						)
_add_candidate_parse.add_argument('batch',
						type=int,
						required=True,
						help="batch-field cannot be blank."
						)
_add_candidate_parse.add_argument('course',
						type=int,
						required=True,
						help="course-field cannot be blank."
						)
_add_candidate_parse.add_argument('department',
						type=int,
						required=True,
						help="department-field cannot be blank."
						)
_add_candidate_parse.add_argument('post',
						type=int,
						required=True,
						help="post-field cannot be blank."
						)
_add_candidate_parse.add_argument('pic_path',
						type=str,
						required=False,
						)
_add_candidate_parse.add_argument('agenda',
						type=str,
						required=False,
						)



_update_candidate_parse = reqparse.RequestParser()
_update_candidate_parse.add_argument('first_name',
						type=str,
						required=False,
						)
_update_candidate_parse.add_argument('last_name',
						type=str,
						required=False,
						)
_update_candidate_parse.add_argument('post',
						type=int,
						required=False,
						)
_update_candidate_parse.add_argument('pic_path',
						type=str,
						required=False,
						)
_update_candidate_parse.add_argument('agenda',
						type=str,
						required=False,
						)



class CandidateRegister(Resource):
	@jwt_required()
	def post(self):
		"""
		Registers a candiate for a post but needs admin access 
		"""

		data  = _add_candidate_parse.parse_args()

		# Check Roll Num Unique
		candidate = CandidateModel.find_by_rollnum(data['roll_num'])
		if candidate is not None:
			output = {'message':'Roll num already registered by another candidate'}
			return output, 400 # Status-Bad Request

		# Check post valid

		claims = get_jwt()
		# If user is admin give ability to register
		if claims['admin_access']==1:
			try:
				candidate = CandidateModel(roll_num=data['roll_num'], first_name=data['first_name'], last_name=data['last_name'],
								batch=data['batch'], course=data['course'], department=data['department'],
								post=data['post'],pic_path=data['pic_path'],agenda=data['agenda'])
				candidate.db_write()

				output = {'message': 'Candidate Registered Sucessfully'}
				return output, 200 # Status-OK
			except:
				output = {'message': 'Something went wrong'}
				return output, 500 # Status-Internal Server Error
		else:
			output = {'message': 'Admin Access required'}
			return output, 401 # Status-Unauthorized



class Candidate(Resource):
	def get(self, candidate_id):
		"""
		Fetches candidate info based on candidate_id
		"""
		
		candidate = CandidateModel.find_by_id(candidate_id)
		if candidate is None:
			output = {'message': 'Candidate Not Found'}
			return output, 404 # Status-Not Found

		output = candidate.json() # get candidate data
		return output, 200 # Status-OK
	
	@jwt_required()
	def delete(self, candidate_id: int):
		"""
		Deletes Candidate based on candidate_id but needs admin access
		"""

		candidate = CandidateModel.find_by_id(candidate_id)

		claims = get_jwt()
		
		if candidate is None:
			output = {'message': 'Candidate Not Found'}
			return output, 404 # Status-Not Found

		# If user is admin give ability to delete
		if claims['admin_access']==1:
			try:
				candidate.db_pop()
				output = {'message': 'Candidate deleted.'}
				return output, 200 # Status-OK
			except:
				output = {'message': 'Something went wrong'}
				return output, 500 # Status-Internal Server Error
		else:
			output = {'message': 'Admin Access required'}
			return output, 401 # Status-Unauthorized

	@jwt_required()
	def put(self, candidate_id: int):
		"""
		Updates Candidate info if candidate present
		and current user has adnin access
		Only updates first_name, last_name, post, pic_path, agenda
		"""
		
		data = _update_candidate_parse.parse_args()

		claims = get_jwt()
		candidate = CandidateModel.find_by_id(candidate_id)

		if candidate is None:
			output = {'message': 'Candidate not found'}
			return output, 404 # Status-Not Found
		
		# If user is admin give ability to delete
		elif claims['admin_access']==1:
			for attr in data:
				if data[attr] is not None:
					# Row, Column, New Value
					setattr(candidate,attr, data[attr])
			try:
				candidate.db_write()
				output = {'message': 'Candidate Data Updated'}
				return output, 200 # Status-OK
			except:
				output = {'message': 'Something went wrong'}
				return output, 500 # Status-Internal Server Error
		else:
			output = {'message': 'Admin Access required'}
			return output, 500 # Status-Internal Server Error
			




		pass



class CandidateList(Resource):
	def get(self):
		"""
		Get list of information regarding all candidates irrespective of post 
		"""

		candidates = [candidate.json() for candidate in CandidateModel.find_all()]

		output = {'candidates': candidates}
		return output, 200 # Status-OK



class Post(Resource):
	def get(self,post_num):
		"""
		Returns candidates based on post id
		"""
		
		candidate_by_post = CandidateModel.find_by_post(post_num)

		if len(candidate_by_post) == 0:
			output = {'message': 'Not a valid Post Number'}
			return output, 404 # Status-Not Found

		candidates = [candidate.json() for candidate in candidate_by_post]

		output = {'candidates': candidates}
		return output, 200 # Status-Ok



class PostList(Resource):
	def get(self):
		"""
		Get list of information posts with candidates nested by post
		"""
		distinct_posts = CandidateModel.num_of_post()
		
		posts = dict()
		for post in distinct_posts:
			candidates = [candidate.json() for candidate in CandidateModel.find_by_post(post)]			
			posts[post] = candidates

		output = {'posts': posts}
		return output, 200 # Status-OK
