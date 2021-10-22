from flask import Flask, render_template

from vote_app import create_app
from vote_app.runtime.commands import app_manager

# ##Development Server
app = create_app('dev')

# ## Production Server
# app = create_app('prod')

# @app.route('/')
# def index():
#     return render_template('index.html')




if __name__=="__main__":
    # Run the App manager commandline interface within application context
    with app.app_context():
        app_manager()
