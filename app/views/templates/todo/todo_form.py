from flask_wtf import FlaskForm
from wtforms import TextField, DateField
from wtforms.validators import InputRequired

class TodoForm(FlaskForm):
    todo = TextField('Todo', [InputRequired()])