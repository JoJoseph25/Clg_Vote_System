from flask import render_template, flash, redirect, url_for, request
import requests
import json

from . import candi
# from .. import db
# from .forms import LoginForm, SignupForm

from flask import current_app

@candi.route("/candidate_view")
def candidate_view():
    candi_post_1 = requests.get('http://localhost:5000/post/1')
    candi1_dict = candi_post_1.json()
    candi_list_post_1 = candi1_dict['candidates']
    
    candi_post_2 = requests.get('http://localhost:5000/post/2')
    candi2_dict = candi_post_2.json()
    candi_list_post_2 = candi2_dict['candidates']
    
    
    return render_template('candidate_view.html', candidates_post_1=candi_list_post_1 ,candidates_post_2=candi_list_post_2)