from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import jwt_required, get_jwt
import requests

from . import auth
# from .. import db
from .forms import LoginForm, SignupForm
# from ...resources.user import UserLogin


from flask import current_app

@auth.route("/user_login", methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {"roll_num": form.roll_num.data,
                "password": form.password.data}
        # send request to login API
        r = requests.post('http://localhost:5000/login',json=data,  
                          headers={'Content-Type': 'application/json'})
        if r.status_code==401:
            flash("Wrong Roll Number or Password")
        elif r.status_code==200:
            print("Login correct")
            flash("Log In successful")
            return redirect(url_for('home.index'))
        # data = UserLogin.post(roll_num=form.roll_num.data,pass_word=form.password.data,headers={'Content-Type': 'application/json'})
        print('Login_response',r)
        print('Status Code',r.status_code)
        print('data',r.text)
        # flash('Incorrect username or password.')
    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        
        if form.admin_code==1225:
            admin=1
        else:
            admin=0
            
        data = {"roll_num": form.roll_num.data,
                "name": form.name.data,
                "email": form.email.data,
                "password": form.password.data,
                "admin": admin}
        # send request to login API
        r = requests.post('http://localhost:5000/signup',json=data,  
                          headers={'Content-Type': 'application/json'})
        if r.status_code==404:
            if 'Roll Num' in r['message']:
                flash("Roll num already registered by another user")
            elif 'Email' in r['message']:
                flash("Email already used by another user")
            return redirect(url_for('auth.register'))
        elif r.status_code==200:
            flash("Registerd successful")
        return redirect(url_for('home.index'))
       
    return render_template("register.html", form=form)


@auth.route("/user_logout")
@jwt_required(optional=True)
def user_logout():
    logged_in = 0
    admin = 0
    claims = get_jwt()
    print('claims:', claims)
    if len(claims)!=0:
        logged_in = 1
        # If user is admin give ability to register
        if claims['admin_access']==1:
            admin = 1
    r = requests.delete('http://localhost:5000/logout')
    if r.status_code==200:
        admin=0
        logged_in=0
        flash("Log Out successful")
    else:
        flash("Unable to Logout")
    return render_template('index.html', admin=admin, logged_in=logged_in)
