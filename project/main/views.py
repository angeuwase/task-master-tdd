from . import main_blueprint
from flask import render_template, abort, request, flash, current_app, redirect, url_for
from flask_login import login_required, current_user
from project.forms import NewTask, UpdateTask
from project.models import Task
from project import db
from sqlalchemy.exc import IntegrityError

@main_blueprint.route('/')
def index():
    return render_template('main/index.html')


@main_blueprint.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = NewTask()

    tasks = Task.query.order_by(Task.id).filter_by(user_id = current_user.id).all()

    if request.method == 'POST':
        if form.validate_on_submit():

            new_task = Task(form.new_task.data, user_id = current_user.id)
            try:
                db.session.add(new_task)
                db.session.commit()
                flash('New task added!')
                current_app.logger.info('New task added: {}'.format(new_task.id))
                return redirect(url_for('main.tasks'))
            except IntegrityError:
                db.session.rollback()
                flash('Task already exists!')
                current_app.logger.info('Attempt to add task that already exists')
                return redirect(url_for('main.tasks'))
        else:
           flash('Error in the form!')

        
    return render_template('main/tasks.html', form=form, tasks=tasks)

@main_blueprint.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted!')
    current_app.logger.info('Task deleted: {}'.format(task_id))
    return redirect(url_for('main.tasks'))

@main_blueprint.route('/mark_complete/<int:task_id>')
@login_required
def mark_complete(task_id):
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()
    flash('Task completed!')
    current_app.logger.info('Task completed: {}'.format(task_id))
    return redirect(url_for('main.tasks'))



@main_blueprint.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    form = UpdateTask(updated_task=task.content)
    if request.method == 'POST':
        if form.validate_on_submit():
            task.content = form.updated_task.data
            db.session.add(task)
            db.session.commit()
            flash('Task updated!')
            current_app.logger.info('Task updated: {}'.format(task_id))
            return redirect(url_for('main.tasks'))
        else:
            flash('Error in the form!')
            return redirect(url_for('main.update_task', task_id=task_id))

    return render_template('main/update_task.html', form=form, task=task)

@main_blueprint.route('/500')
def error_500():
    return abort(500)