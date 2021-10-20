import os
import click
from flask.cli import with_appcontext
from flask import current_app as app
from sqlalchemy.orm import defaultload

from vote_app.runtime.extensions import db
from vote_app.models.user import UserModel
from vote_app.models.candidate import CandidateModel
from vote_app.models.votes import VotesModel


# Main App Command Manager Groups 
@click.group()
def app_manager():
    pass


app_manager.group()
@app_manager.command(name="fresh_run")
@click.option('--host', default="localhost", help="IP address to host application")
@click.option('--port', default=5000, help="Port")
@click.pass_context
def auto_run(ctx,host,port):
    '''
    Check if DB exist if not creates and the runs the app
    '''
    # Delete Database by invoking dropdb command
    ctx.invoke(dropdb,y='y')
    # Create Databe by invoking insert data command
    ctx.invoke(insert_data)
    # Runserver by invoking runserver command
    ctx.invoke(runserver,host=host,port=port)


app_manager.group()
@app_manager.command(name="auto_run")
@click.option('--host', default="localhost", help="IP address to host application")
@click.option('--port', default=5000, help="Port")
@click.pass_context
def auto_run(ctx,host,port):
    '''
    Check if DB exist if not creates and the runs the app
    '''
    db_filepath = app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1]
    # Check if DB not present
    if os.path.isfile(db_filepath)!=True:
        print("DB not present")
        # Create Databe by invoking insert data command
        ctx.invoke(insert_data)
    # Runserver by invoking runserver command
    ctx.invoke(runserver,host=host,port=port)
    

app_manager.group()
@app_manager.command(name="runserver")
@click.option('--host', default="localhost", help="IP address to host application")
@click.option('--port', default=5000, help="Port")
def runserver(host,port):
    '''
    Runs the Vote App on specified host and port
    '''
    app.run(host=host,port=port)


app_manager.group()
@app_manager.command(name="insert_data")
def insert_data():
    '''
    Inserts Default User Values To SQL Database for Vote App
    '''
    db.create_all()
    
    # Add super admin and test user
    super_admin = UserModel(roll_num=17000000, name='admin', email="admin@gmail.com", password="pass", admin=1)
    db.session.add(super_admin)
    anonymous = UserModel(roll_num=17513011, name='test', email="test@gmail.com", password="1234")
    db.session.add(anonymous)
    
    # Add test candidates to DB
    # POST 1
    candidate0 = CandidateModel(roll_num=20000000, first_name='No', last_name='Vote', 
                                batch=20, course=00, department=00, post=1)
    db.session.add(candidate0)
    candidate1 = CandidateModel(roll_num=17110011, first_name='Cristiano', last_name='Ronaldo', 
                                batch=17, course=11, department=00, post=1, 
                                pic_path='deafult/pic/path',agenda="Will try to win Champions League")
    db.session.add(candidate1)
    candidate2 = CandidateModel(roll_num=17315211, first_name='Robert', last_name='Lewandowski', 
                                batch=17, course=31, department=15, post=1, 
                                pic_path='deafult/pic/path',agenda="Will Score 40 goals a season")
    db.session.add(candidate2)
    candidate3 = CandidateModel(roll_num=16225611, first_name='Zlatan', last_name='Ibrahimovic', 
                                batch=16, course=22, department=56, post=1, 
                                pic_path='deafult/pic/path',agenda="I'm Zlatan.")
    db.session.add(candidate3)
    
    # POST 2
    candidate0 = CandidateModel(roll_num=20000001, first_name='No', last_name='Vote', 
                                batch=20, course=00, department=00, post=2)
    db.session.add(candidate0)
    candidate1 = CandidateModel(roll_num=20420031, first_name='Bruno', last_name='Fernandes', 
                                batch=20, course=42, department=00, post=2, 
                                pic_path='deafult/pic/path',agenda="I will assist Cristiano")
    db.session.add(candidate1)
    candidate2 = CandidateModel(roll_num=18315211, first_name='Harry', last_name='Kane', 
                                batch=18, course=31, department=52, post=2, 
                                pic_path='deafult/pic/path',agenda="I'm staying at Tottenham and will try to win the league")
    db.session.add(candidate2)
    candidate3 = CandidateModel(roll_num=20225611, first_name='Megan', last_name='Rapinoe', 
                                batch=20, course=22, department=56, post=2, 
                                pic_path='deafult/pic/path',agenda="Equal pay for US Womens team")
    db.session.add(candidate3)
    candidate4 = CandidateModel(roll_num=18312411, first_name='Lionel', last_name='Messi', 
                                batch=18, course=31, department=24, post=2, 
                                pic_path='deafult/pic/path',agenda="Equal pay for US Womens team")
    db.session.add(candidate4)
    
    db.session.commit()

    print('Database Initialized.')

app_manager.group()
@app_manager.command(name="dropdb")
@click.option('--y', default="default", help="Port")
def dropdb(y):
    '''
    Deletes the Databse for Vote App
    '''
    
    yes_response =  ["yes","YES","Yes","Y","y"]
    no_response = ["no","NO","No","N","n"]
    if y in yes_response:
        db.drop_all() # Drop DB
        # Delete DB
        db_filepath = app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1]
        os.remove(db_filepath)
        print("Dropped the Database!")
    else:
        user_input=input("Are you sure you want to loose all your data?\nChoose [Y/n] to continue: ")
        while not((user_input in yes_response) or (user_input in no_response)):
            print("Your response ('{}') was not one of the expected responses: y, n ".format(user_input),end=" ")
            user_input=input()

        if user_input in yes_response:
            db.drop_all() # Drop DB
            # Delete DB
            db_filepath = app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1]
            os.remove(db_filepath)
            print("Dropped the Database!")
        else:
            print("Database Drop Cancelled")