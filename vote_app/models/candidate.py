from vote_app import db

from werkzeug.security import check_password_hash, generate_password_hash

class CandidateModel(db.Model):
	__tablename__ = 'candidates'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	roll_num = db.Column(db.Integer, nullable=False, unique=True)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80))
	batch = db.Column(db.Integer, nullable=False)
	department = db.Column(db.Integer, nullable=False)
	course = db.Column(db.Integer, nullable=False)
	post = db.Column(db.String(120), nullable=False)
	pic_path = db.Column(db.String(120), default='deafult/pic/path')
	agenda =  db.Column(db.Boolean, default=False)

	def __init__(self,  roll_num,first_name,last_name,batch,department,course,post,pic_path,agenda):
		self.roll_num = roll_num
		self.first_name = first_name
		self.last_name = last_name
		self.batch = batch
		self.department = department
		self.course = course
		self.post = post
		self.pic_path = pic_path
		self.agenda = agenda

	def json(self):
		output={
			'id': self.id,
			'roll_num': self.roll_num,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'batch': self.batch,
			'department': self.department,
			'course': self.course,
			'pic_path': self.pic_path,
			'agenda': self.agenda
		}
		return output
