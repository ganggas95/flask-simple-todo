from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, EqualTo 

class AuthForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])

class RegisterForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [
                InputRequired(),
                EqualTo('confirm', message="Password must match")])
    confirm = PasswordField('Confirm Password', [InputRequired()])
