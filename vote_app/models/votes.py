from sqlalchemy.sql.schema import ForeignKey
from vote_app import db

class VotesModel(db.Model):
	__tablename__ = 'votes'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	roll_num = db.Column(db.Integer, nullable=False, unique=True)
	voter_id = db.Column(db.Integer, ForeignKey('users.id'))
	post_1 = db.Column(db.Integer, nullable=False, default=1)
	post_2 = db.Column(db.Integer, nullable=False, default=1)
 
	def __init__(self, roll_num, voter_id, post_1, post_2):
		self.roll_num = roll_num
		self.post_1 = post_1
		self.post_2 = post_2
		self.voter_id = voter_id

	def db_write(self):
		db.session.add(self)
		db.session.commit()

	def db_pop(self):
		db.session.delete(self)
		db.session.commit()
	
	def json(self):
		output={
			'id': self.id,
			'post_1': self.post_1,
			'post_2':  self.post_2
		}
		return output
	
	def admin_json(self):
		output={
			'id': self.id,
			'roll_num': self.roll_num,
			'voter_id': self.voter_id,
			'post_1': self.post_1,
			'post_2':  self.post_2
		}
		return output


	@classmethod
	def find_by_rollnum(cls, roll_num):
		return cls.query.filter_by(roll_num=roll_num).first()

	@classmethod
	def find_all(cls):
		return cls.query.all()

	@classmethod
	def find_by_candidate(cls, candidate, post):
		if post==1:
			return cls.query.filter_by(post_1=candidate).all()
		elif post==2:
			return cls.query.filter_by(post_2=candidate).all()
		else:
			print("Wierd Should not come here")
			return None

	@classmethod
	def countby_candidate_post(cls, candidate, post):

		if post==1:
			count = VotesModel.query.filter_by(post_1=candidate).count()
		elif post==2:
			count = VotesModel.query.filter_by(post_2=candidate).count()	
		else:
			count = -1
			print("Wierd Should not come here")
		return count