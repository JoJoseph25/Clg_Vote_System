import re
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import jwt_required, get_jwt

from . import graph


@graph.route('/')
def graph():
    
	return render_template('index.html')