from vote_app import db

class Votes(db.Model):
	__tablename__ = 'votes'

	id = db.Column(db.Integer, primary_key=True)
	roll_num = db.Column(db.Integer, nullable=False, unique=True)
	post_1 = db.Column(db.Integer, nullable=False, default=1)
	post_2 = db.Coulmn(db.Integer, nullable=False, default=1)
 
	def __init__(self, id, roll_num, post_1, post_2):
		id = id
		roll_num = roll_num
		post_1 = post_1
		post_2 = post_2

	@staticmethod
	def count_votes_for_candidate(post,candidate):
		if post==1:
			count = Votes.query.filter_by(post1=candidate).count()
		elif post==2:
			count = Votes.query.filter_by(post1=candidate).count()	
		else:
			count = -1
			print("Wierd Should not come here")
		return count

	# ## Count the votes for all candidates  
 	# @staticmethod
	# def count_votes_for_post(post):
	# 	if 