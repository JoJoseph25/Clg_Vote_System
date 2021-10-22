from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import NumberRange, DataRequired, Length, Email, Regexp, EqualTo,\
    ValidationError, Optional


class LoginForm(FlaskForm):
    roll_num = IntegerField('Your Roll Number:', 
                            validators=[DataRequired(), 
                            NumberRange(min=10000000, max=99999999, message="Roll Number is 8 digit number")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    roll_num = IntegerField('Roll Number: ',
                    validators=[
                    DataRequired(),
                    NumberRange(min=10000000, max=99999999, message="Roll Number is 8 digit number")])
    name = StringField('Name',
                        validators=[DataRequired(), Length(1, 120)])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])
    password = PasswordField('Password',
                    validators=[
                        DataRequired(),
                        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    admin_code =IntegerField('Enter Admin Code (if known), else leave blank: ',validators=[Optional()])

    submit = SubmitField('Register')