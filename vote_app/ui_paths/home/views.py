from flask import render_template, request

from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from flask_jwt_extended.utils import get_jwt_header

from . import home


@home.route('/')
@home.route('/index')
@jwt_required(optional=True)
def index():
	logged_in = 0
	admin = 0
	head = get_jwt_header()
	print(head)
	identity = get_jwt_identity()
	print(identity)
	claims = get_jwt()
	print('claims:', claims)
	if len(claims)!=0:
		logged_in = 1
		# If user is admin give ability to register
		if claims['admin_access']==1:
			admin = 1
	print("Logged In: ", logged_in)
	print("Admin: ", admin)
			
	return render_template('index.html', admin=admin, logged_in=logged_in)