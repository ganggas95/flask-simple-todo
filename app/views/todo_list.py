import logging
import datetime
from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required
from app import app
from app.models.models import Todo, User
from app.views.templates.todo.todo_form import TodoForm

@app.route("/todo/list", methods=['GET', 'POST'])
@login_required
def get_todo_list():
    form = TodoForm(request.form)
    if request.method == 'GET':
        todos = Todo.query.all()
        return render_template('todo_list.html', 
                    todos=todos, 
                    page_title="Data Todos",
                    form=form, 
                    mode="add")
    if request.method == 'POST' and 'username' in session and form.validate():
        todo_form = request.form.get('todo')
        cur_user = User.query.filter(User.username==session['username'])\
                    .first()
        todo = Todo()
        todo.todo = todo_form
        todo.create_by_id = cur_user.id 
        todo.save()
        flash('Data successfully added!!', 'success')
        return redirect(url_for('get_todo_list'))
    if form.errors:
        for error in form.errors:
            flash(form.errors[error], 'danger')
    return redirect(url_for('get_todo_list'))

@app.route("/todo/<int:id>/edit", methods=['GET','POST'])
@login_required
def change_todo_list(id):
    form = TodoForm(request.form)
    todo = Todo.query.get(id)
    if request.method == 'GET':
        todos = Todo.query.all()
        return render_template('todo_list.html', 
                    todos=todos,
                    todo=todo, 
                    page_title="Data Todos",
                    form=form, 
                    mode="edit")
    if request.method == 'POST' and form.validate():
        todo_form = request.form.get('todo')
        todo.todo = todo_form
        todo.save()
        flash('Data successfully changed!!', 'success')
        return redirect(url_for('get_todo_list'))

@app.route("/todo/<int:id>/delete")
@login_required
def delete_todo_list(id):
    todo = Todo.query.get(id)
    if request.method == 'GET':
        todo.delete()
        return redirect(url_for('get_todo_list'))