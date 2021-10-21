from flask_jwt_extended.utils import get_jwt_identity

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from vote_app.models.user import UserModel
from vote_app.models.votes import VotesModel
from vote_app.resources.candidate import CandidateModel


_vote_parse = reqparse.RequestParser()
_vote_parse.add_argument('post_1',
						type=int,
						required=True,
						help="This field cannot be blank."
						)
_vote_parse.add_argument('post_2',
						type=int,
						required=True,
						help="This field cannot be blank."
						)

_vote_count_parse =reqparse.RequestParser()
_vote_count_parse.add_argument('count_method',
                               type=str,
                               required=True,
                               help="This field cannot be blank"
                               )
_vote_count_parse.add_argument('method_id',
                               type=int,
                               required=True,
                               help="This field cannot be blank"
                               )



class Vote(Resource):
	@jwt_required(optional=True)
	def get(self):
		"""
		Fetch vote of the current user.
		If not logged in return msg to vote.
		"""
		user_rollnum = get_jwt_identity()
		
		if user_rollnum is not None:
			voted = VotesModel.find_by_rollnum(user_rollnum)
			if voted is not None:
				output = {"vote":voted.json()}
				return output, 200 # Status-OK
			else:
				output = {"message":"Please caste vote to view it"}
				return output, 404 # Status-Not Found
		output = {"message":"Please log-in to view your vote"}
		return output, 401 # Status-Unauthorized
	
 
	@jwt_required()
	def post(self):
		"""
		Registers vote for the candidate
		"""

		data  = _vote_parse.parse_args()

		user_rollnum = get_jwt_identity()
		
		voted = VotesModel.find_by_rollnum(user_rollnum)

		# If User has not voted (roll_num not in votes table)
		if voted is None:
			try:
				user = UserModel.find_by_rollnum(user_rollnum)
				vote = VotesModel(roll_num=user_rollnum, voter_id=user.id,
							post_1=data['post_1'], post_2=data['post_2'])

				vote.db_write()

				output = {'message': 'Vote Casted'}
				return output, 200 # Status-OK
			except:
				output = {'message':'Something went wrong'}
				return output, 500 # Status-Internal Server Errror
		else:
			output = {'message': 'Already Casted your vote'}
			return output, 401 # Status-Unauthorized



class VoteList(Resource):
	
	@jwt_required(optional=True)
	def get(self):
		"""
		Get list of all casted votes
		"""
		
		votes_all = VotesModel.find_all()
		
		claims = get_jwt()
		if len(claims)!=0:
			if claims['admin_access']==1:
				votes = [vote.admin_json() for vote in votes_all]
				output = {"votes": votes}
				return output, 200 # Status-OK

		votes = [vote.json() for vote in votes_all]
		output = {"votes":votes,
				"message": "need admin-acess to view more"}
		return output, 200 # Status-OK



class VoteCount(Resource):
	def get(self):
		"""
		Returns the count of votes based on the count method.
		
		count_method = all returns vote count based on nested posts 
		and candidates sub_nested. Method_id is used for this method.
		
		count_method = candidate returns vote count of specific candidate 
		based on method_id==cadndidate_id
		
		count_method = post returns vote count of specific post 
		based on method_id==post_id
		
		"""
		
		data = _vote_count_parse.parse_args()

		try:
			if data['count_method']=='all':
				# Iterate over all possible posts
				posts = CandidateModel.num_of_post()
				out_post = dict()
				
				for post in posts:
					
					# Iterate over all candidates
					candidates = CandidateModel.find_by_post(post)
					out_candidate = dict()
					
					for candidate in candidates:
					
						# Count votes for candiate and post
						candidate_count = VotesModel.countby_candidate_post(candidate=candidate.id, post=post)
						out_candidate[candidate.id] = candidate_count
					
					out_post[post] = out_candidate
				
				output = {'vote_count':out_post}
				return output, 200 # Status-OK

			elif data['count_method']=='candidate':
				
				#If Candidate Present Check
				candidate = CandidateModel.find_by_id(data['method_id'])
				
				if candidate is not None:
					candidate_count = VotesModel.countby_candidate_post(candidate=candidate.id,post=candidate.post)
					
					output = {'candidate_count':candidate_count}
					return output, 200 # Status-OK
				else:
					output ={"message":"Candiate not valid"}
					return output, 404 # Not-Found
			
			elif data['count_method']=='post':
				
				#If Post num Present Check
				posts = CandidateModel.num_of_post()

				if data['method_id'] in posts:
					candidates = CandidateModel.find_by_post(data['method_id'])
					print(candidates)
					out_candidate = dict()

					for candidate in candidates:
						candidate_count = VotesModel.countby_candidate_post(candidate=candidate.id,post=data['method_id'])
						
						out_candidate[candidate.id] = candidate_count				
					
					output = {"post_count":out_candidate}
					return output, 200 # Status-OK
					
				else:
					output ={"message":"Candiate not valid"}
					return output, 404 # Not-Found
			
			else:
				output ={"message":"Not a valid count method"}
				return output, 400 # Bad-Request
		except:
			output = {'message': 'Something went wrong'}
			return output, 500 # Status-Internal Server Error
