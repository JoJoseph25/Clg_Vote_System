import re
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import jwt_required, get_jwt
import requests


from . import choose
from .forms import VoteForm

@choose.route("/cast_vote", methods=['GET','POST'])
# @jwt_required()
def cast_vote():
	form = VoteForm()
	voted = requests.get('http://localhost:5000/vote')
	if voted is not None:
		if voted.status_code==200:
			flash("Already Casted Your Vote")
			return redirect(url_for("home.index"))

	r1 = requests.get('http://localhost:5000/post/1')
	r2 = requests.get('http://localhost:5000/post/2')
	if r1.status_code==200 and r2.status_code==200:
		r1_dict=r1.json()
		post1_candidates = r1_dict['candidates']
		post1_options=[]
		for post1_candi in post1_candidates:
			post1_options.append((post1_candi['id'],'{}: {} {}'.format(post1_candi['roll_num'],post1_candi['first_name'],post1_candi['last_name'])))

		r2_dict=r2.json()
		post2_candidates = r2_dict['candidates']
		post2_options=[]
		for post2_candi in post2_candidates:
			post2_options.append((post2_candi['id'],'{}: {} {}'.format(post2_candi['roll_num'],post2_candi['first_name'],post2_candi['last_name'])))

	else:
		flash("Could not find any candidates from DB!")
		redirect(url_for('home.index'))

	form.post1_choice.choices = post1_options
	form.post2_choice.choices = post2_options
	
	if form.validate_on_submit():
		post_1 = request.form.get('post1_choice')
		post_2 = request.form.get('post1_choice')

		label_1 = post1_options[int(post_1)-1]
		label_2 = post2_options[int(post_2)-1]
		data = {"post_1": label_1[0],
				"post_2": label_2[0]
				}
		flash("Post_1: {} and Post_2: {}".format(label_1[1], label_2[1]))
		return redirect(url_for('choose.confirm_vote', vote_data=data))
	
	return render_template("cast_vote.html", form=form)

@choose.route("/confirm_vote", methods=['GET','POST'])
# @jwt_required()
def confirm_vote():
    
	vote_confirm = request.form.get('confirm')
	print(vote_confirm)
	if vote_confirm!=None and vote_confirm!='':
		if int(vote_confirm)==1:
			vote_data = request.args.get('vote_data')
			r = requests.post('http://localhost:5000/vote',json=vote_data,
                      headers={'Content-Type': 'application/json'})
			if r.status_code==200:
				flash("Vote Uploaded")
			else:
				flash("Vote Invalid")
		else:
			flash("Vote Cancelled")

		return redirect(url_for('home.index'))

	return render_template('confirm_vote.html')