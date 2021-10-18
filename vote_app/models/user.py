from vote_app import db

from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	roll_num = db.Column(db.Integer(8), nullable=False, unique=True)
	name = db.Column(db.String(80),nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	password_hash = db.Column(db.String, nullable=False)
	admin =  db.Column(db.Boolean(),default=False)
 
	def __init__(self, id, roll_num,name,email,password_hash,admin):
		id = id
		roll_num = roll_num
		name = name
		email = email
		password_hash = password_hash
		admin =  admin

	def json(self):
		output={
			'id': self.id,
			'roll_num': self.roll_num,
			'name': self.name,
			'email': self.email,
			'admin':  self.admin
		}
		return output

	@property
	def password(self):
		raise AttributeError('password: write-only field')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
