import logging
import datetime
from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app import app
from app.models.models import User
from app.views.templates.user.user_form import AddUserForm, EditUserForm

@app.route("/user/list", methods=['GET', 'POST'])
@login_required
def get_users():
    form = AddUserForm(request.form)
    if request.method == 'GET':
        users = User.query.all()
        return render_template('users.html', 
                    users=users, 
                    page_title="Data Users",
                    form=form, 
                    mode="add")
    if request.method == 'POST' and 'username' in session and form.validate():
        username_form = request.form.get('username')
        password_form = request.form.get('password')
        user_exist = User.query.filter(User.username==username_form).first()
        if user_exist:
            flash("User has already taken!. Please try another!", 'danger')
            return redirect(url_for('get_users'))
        user = User()
        user.username = username_form
        user.password = user.create_password(password_form) 
        user.save()
        flash('Data successfully added!!', 'success')
        return redirect(url_for('get_users'))
    if form.errors:
        for error in form.errors:
            flash(form.errors[error], 'danger')
    return redirect(url_for('get_users'))

@app.route("/user/<int:id>/edit", methods=['GET','POST'])
@login_required
def change_user(id):
    form = EditUserForm(request.form)
    user = User.query.get(id)
    if request.method == 'GET':
        users = User.query.all()
        return render_template('users.html', 
                    users=users,
                    page_title="Data Users",
                    user=user, 
                    form=form, 
                    mode="edit")
    if request.method == 'POST' and form.validate():
        username_form = request.form.get('username')
        old_pass_form = request.form.get('old_password')
        new_pass_form = request.form.get('new_password')
        if not user.check_password(old_pass_form):
            flash("Password is wrong. Please try another pass key.", "danger")
            return redirect(url_for('change_user', id=id))
        user.username = username_form
        user.password = user.create_password(new_pass_form)
        user.save()
        flash('Data successfully changed!!', 'success')
        return redirect(url_for('change_user', id=id))

@app.route("/user/<int:id>/delete")
@login_required
def delete_user(id):
    user = User.query.get(id)
    if request.method == 'GET':
        if user != current_user:
            user.delete()
            flash("User has been deleted!", "success")
        else:
            flash("Users currently active.", "warning")
        return redirect(url_for('get_users'))