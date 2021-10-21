from vote_app import db

from werkzeug.security import check_password_hash, generate_password_hash

class CandidateModel(db.Model):
	__tablename__ = 'candidates'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	roll_num = db.Column(db.Integer, nullable=False, unique=True)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80))
	batch = db.Column(db.Integer, nullable=False)
	course = db.Column(db.Integer, nullable=False)
	department = db.Column(db.Integer, nullable=False)
	post = db.Column(db.Integer, nullable=False)
	pic_path = db.Column(db.String(120), default='deafult/pic/path')
	agenda =  db.Column(db.String(300), default="No agenda")

	# def __init__(self, roll_num,first_name,last_name,
	# 			batch,course,department,
	# 			post,pic_path='deafult/pic/path',agenda="No agenda"):
	# 	self.roll_num = roll_num
	# 	self.first_name = first_name
	# 	self.last_name = last_name
	# 	self.batch = batch
	# 	self.course = course
	# 	self.department = department
	# 	self.post = post
	# 	self.pic_path = pic_path
	# 	self.agenda = agenda

	def json(self):
		output={
			'id': self.id,
			'roll_num': self.roll_num,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'batch': self.batch,
			'course': self.course,
			'department': self.department,
			'post': self.post,
			'pic_path': self.pic_path,
			'agenda': self.agenda
		}
		return output

	def db_write(self):
		db.session.add(self)
		db.session.commit()

	def db_pop(self):
		db.session.delete(self)
		db.session.commit()

	# First candidate of each post is Nil
	@classmethod
	def null_candidate(cls, post):
		return cls.query.filter_by(post=post).first()

	@classmethod
	def find_all(cls):
		return cls.query.all()

	@classmethod
	def find_by_post(cls, post):
		return cls.query.filter_by(post=post).all()

	@classmethod
	def find_by_id(cls, candidate_id):
		return cls.query.filter_by(id=candidate_id).first()

	@classmethod
	def find_by_rollnum(cls, roll_num):
		return cls.query.filter_by(roll_num=roll_num).first()

	def num_of_post():
		return [posts.post for posts in db.session.query(CandidateModel.post).distinct()]

