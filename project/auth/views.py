from . import auth_blueprint
from flask import render_template, request, flash, redirect, url_for
from project.forms import RegistrationForm
from project.models import User
from project import db

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

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
                return redirect(url_for('auth.login'))
        else:
            flash("Error in form data!")


    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/login')
def login():
    return render_template('auth/login.html')