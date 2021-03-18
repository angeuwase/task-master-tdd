from . import auth_blueprint
from flask import render_template, request, flash, redirect, url_for, current_app
from project.forms import RegistrationForm, LoginForm
from project.models import User
from project import db
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.urls import url_parse

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        flash('You already have an account and are logged in!')
        return redirect(url_for('auth.profile'))

    if request.method == 'POST':
        if form.validate_on_submit():

     
            user = User.query.filter_by(username=form.username.data).first()

            if user:
                flash('You already have an account! Please login.')
                return redirect(url_for('auth.login'))
            else:
                new_user = User(form.username.data, form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash('You have been registered. Please sign in to access your account.')
                current_app.logger.info('A new user has been added: {}'.format(new_user.username))
                return redirect(url_for('auth.login'))
        else:
            flash("Error in form data!")


    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('auth.profile'))

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user:
                if user.is_password_valid(form.password.data):
                    flash('You are now logged in.')
                    current_app.logger.info('User signed in: {}'.format(user.username))
                    login_user(user)

                    #find next path user wants to be redirected to after logging in
                    next_path = request.args.get('next')

                    #if next_path is not provided or is invalid (a full path) redirect user to profile page. If it valid redirect to next_path
                    if not next_path or url_parse(next_path).netloc != '':
                        return redirect(url_for('auth.profile'))
                    return redirect(next_path)
            form.username.data = ''
            flash('Invalid credentials. Please try again or sign up for an account.')
            current_app.logger.info('Invalid attempted login.')
            return redirect(url_for('auth.login'))

        else:
            flash("Error in form data!")
            
    return render_template('auth/login.html', form=form)

@auth_blueprint.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    flash('You are now logged out.')
    current_app.logger.info('User signed out: {}'.format(current_user.username))
    logout_user()
    return redirect(url_for('main.index'))
