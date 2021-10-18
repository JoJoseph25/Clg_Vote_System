from vote_app import db

from werkzeug.security import check_password_hash, generate_password_hash

class Candidate(db.Model):
	__tablename__ = 'candidates'

	id = db.Column(db.Integer, primary_key=True)
	roll_num = db.Column(db.Integer, nullable=False, unique=True)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80))
	batch = db.Column(db.Integer, nullable=False)
	department = db.Column(db.Integer, nullable=False)
	course = db.Column(db.Integer, nullable=False)
	post = db.Colum(db.String(120), nullable=False)
	pic_path = db.Column(db.String(120), default='deafult/pic/path')
	agenda =  db.Column(db.Boolean, default=False)

	def __init__(self, id, roll_num, first_name, last_name, batch, department, course, post, pic_path, agenda):
		id = id
		roll_num = roll_num
		first_name = first_name
		last_name = last_name
		batch = batch
		department = department
		course = course
		post = post
		pic_path = pic_path
		agenda = agenda

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
