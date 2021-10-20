from vote_app import db

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	roll_num = db.Column(db.Integer, nullable=False, unique=True)
	name = db.Column(db.String(80),nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	_password = db.Column(db.String(), nullable=False)
	admin =  db.Column(db.Integer,default=0)
 

	@hybrid_property
	def password(self):
		raise self._password

	@password.setter
	def password(self, password_plain):
		self._password = generate_password_hash(password_plain)
	
	def check_password(self, password_plain):
		return check_password_hash(self._password, password_plain)

	def __init__(self, roll_num,name,password,email,admin=0):
		self.roll_num = roll_num
		self.name = name
		self.email = email
		self.password = password
		self.admin = admin
	
	def json(self):
		output={
			'roll_num': self.roll_num,
			'name': self.name,
			'email': self.email,
		}
		return output
	
	def admin_json(self):
		output={
			'id': self.id,
			'roll_num': self.roll_num,
			'name': self.name,
			'email': self.email,
			'admin':  self.admin
		}
		return output

	def db_write(self):
		db.session.add(self)
		db.session.commit()

	def db_pop(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_rollnum(cls, roll_num):
		return cls.query.filter_by(roll_num=roll_num).first()

	@classmethod
	def find_by_email(cls, email):
		return cls.query.filter_by(email=email).first()

	@classmethod
	def find_all(cls):
		return cls.query.all()