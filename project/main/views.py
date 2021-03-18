from . import main_blueprint
from flask import render_template, abort
from flask_login import login_required

@main_blueprint.route('/')
def index():
    return render_template('main/index.html')


@main_blueprint.route('/tasks')
@login_required
def tasks():
    return render_template('main/tasks.html')

@main_blueprint.route('/update_task')
@login_required
def update_task():
    return render_template('main/update_task.html')

@main_blueprint.route('/500')
def error_500():
    return abort(500)