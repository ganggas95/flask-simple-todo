import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.secret_key = 'bismillahirrohmanirrohim_1khl45_1571q0m4h'
app.config['WTF_CSRF_SECRET_KEY'] = 'bismillahirrohmanirrohim_1khl45_1571q0m4h'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}{}app.db'.format(app.root_path, os.path.sep)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True

CSRFProtect(app=app)

from app import models, views