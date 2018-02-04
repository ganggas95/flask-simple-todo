from flask import request, \
                render_template, redirect, \
                url_for, g, \
                flash, session 
from flask_login import LoginManager, current_user, \
                logout_user, login_required, login_user
from app import app
from app.models.models import User
from app.views.templates.authenticate.auth_form import AuthForm



login_manager = LoginManager(app=app)
login_manager.login_view = "auth_login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.before_request
def get_current_user():
    g.user = current_user

@app.route("/login", methods=['GET', 'POST'])
def auth_login():
    form = AuthForm(request.form)
    if 'logged_in' in session and session['logged_in']:
        flash("You are alredy logged in", 'success')
        return redirect(url_for('get_todo_list'))
    if request.method == 'GET':
        return render_template('login.html',
                    form=form,
                    page_title="Login User")
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        user_exist = User.query.filter(User.username==username).first()
        if not (user_exist and user_exist.check_password(password)):
            flash('Invalid username and password. Try another one!', 'danger')
            return redirect(url_for('auth_login'))
        session['username'] = user_exist.username
        session['logged_in'] = True
        login_user(user_exist, remember=False)
        next = request.args.get('next')
        flash('Login Successfully. Wellcome {}'.format(username), 'success')
        return redirect(next or url_for('get_todo_list'))
@app.route("/logout")
@login_required
def logout():
    if 'username' in session and 'logged_in' in session:
        logout_user()
        session.pop('username')
        session['logged_in'] = False
        flash('You have successfully Logged out!.', 'success')
    return redirect(url_for('auth_login'))