from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
	username = StringField('Username: ', validators=[DataRequired()])
	password = StringField('Pasword: ', validators=[DataRequired()])
	submit = SubmitField('Login')
class PostForm(FlaskForm):
	title = StringField('Title: ', validators=[DataRequired()])
	post = TextAreaField('Post', validators=[DataRequired()])
	submit = SubmitField('Submit')
class JoinForm(FlaskForm):
	username = StringField('Username: ', validators=[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match!'), Length(min=5, message='Password must be at least 5 characters long!')])
	password2 = PasswordField('Confirm password: ')
	submit = SubmitField('Create an account')
