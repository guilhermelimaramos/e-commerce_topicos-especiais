from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignUpForm(FlaskForm):
  username = StringField(label='Username:')
  email = StringField(label='Email:')
  password1 = StringField(label='Password:')
  password2 = StringField(label='Confirm Password:')
  submit = SubmitField(label='Sign up')