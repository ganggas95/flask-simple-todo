from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, EqualTo 

class AddUserForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [
                InputRequired(),
                EqualTo('confirm', message="Password must match")])
    confirm = PasswordField('Confirm Password', [InputRequired()])

class EditUserForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    old_password = PasswordField('Old Password', [InputRequired()])
    new_password = PasswordField('New Password', [InputRequired()])