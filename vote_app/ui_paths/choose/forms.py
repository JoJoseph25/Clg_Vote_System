from flask_wtf import FlaskForm
from wtforms.fields import SelectField, SubmitField


class VoteForm(FlaskForm):
    post1_choice = SelectField('Post 1: President ')
    post2_choice = SelectField('Post 2: Vice-President ')
    submit_button = SubmitField('Vote')
