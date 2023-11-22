from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from commerce.models import User

class SignUpForm(FlaskForm):
  def validate_username(self, check_user):
    user = User.query.filter_by(username=check_user.data).first()
    if user: 
      raise ValidationError("Username already exists! Try another username")
  def validate_email(self, check_email):
    email = User.query.filter_by(email=check_email.data).first()
    if email:
      raise ValidationError("Email already exists! Try another email")
  username = StringField(label='Username:', validators=[Length(min=3, max=30), DataRequired()])
  email = StringField(label='Email:', validators=[Email(), DataRequired()])
  password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
  password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1', 'Passwords do not match.'), DataRequired()])
  submit = SubmitField(label='Sign up') 

class SignInForm(FlaskForm):
  username = StringField(label='Username:', validators=[DataRequired()])
  password = PasswordField(label='Password:', validators=[DataRequired()])
  submit = SubmitField(label='Sign in') 