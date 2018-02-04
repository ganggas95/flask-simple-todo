from flask import request, render_template, redirect, url_for, g, flash, session
from app import app
from app.models.models import User
from app.views.templates.authenticate.auth_form import RegisterForm


@app.route("/reg", methods=['GET', 'POST'])
def register_user():
    form = RegisterForm(request.form)
    if session['logged_in']:
        flash("You are alredy logged in", 'success')
        return redirect(url_for('get_todo_list'))
    if request.method == 'GET':
        return render_template('register.html', 
                form=form,
                page_title="Register User")
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        user_exist = User.query.filter(User.username==username).first()
        if user_exist:
            flash('User has been already taken!. Please try another one..', 'danger')
            return redirect(url_for('register_user'))    
        user = User()
        user.username = username
        user.password = user.create_password(password)
        user.save()
        flash('Sign up Successfully.', 'success')
        return redirect(url_for('auth_login'))
    if form.errors:
        for error in form.errors:
            flash(form.errors[error], 'danger')
    return render_template('register.html',
                form=form,
                page_title="Register User")