import requests
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import jwt_required, get_jwt

from . import graph


@graph.route('/')
def graph():
	count_req_data = {"count_method": "all",
						"method_id": 1}
	r = requests.get('http://localhost:5000/count',json=count_req_data,  
							headers={'Content-Type': 'application/json'})
	c = requests.get('http://localhost:5000/candidates')
	if r.status_code==200 and c.status_code==200:
		
		count_dict=r.json()
		count_votes = count_dict['vote_count']
		post1_votes = count_votes["1"]
		print("Post1: ",post1_votes)
		post2_votes = count_votes["2"]
		print("Post2: ",post2_votes)

		# Mapping candidate id votes to candidate roll number
		# for display purposes
		post1_candi_votes=[]
		post1_candi_rollnum=[]
		post2_candi_votes=[]
		post2_candi_rollnum=[]

		candi_dict=c.json()
		canndidates = candi_dict['candidates']
		candi_name = dict()
		for candi in canndidates:
			if candi['post']==1:
				post1_candi_votes.append(post1_votes[str(candi['id'])])
				post1_candi_rollnum.append(candi['roll_num'])
			else:
				post2_candi_votes.append(post2_votes[str(candi['id'])])
				post2_candi_rollnum.append(candi['roll_num'])
    	
			candi_name[candi['roll_num']]='{} {}'.format(candi['first_name'],candi['last_name'])
		print("Candidates:", canndidates)
		print("Post1 Votes:", post1_candi_votes)
		print("Post2 Votes:", post2_candi_votes)
		

	return render_template('graph.html', post1_labels=post1_candi_rollnum, post1_votes= post1_candi_votes,
                        post2_labels=post2_candi_rollnum, post2_votes= post2_candi_votes,
                        candidate_names = candi_name)