from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from project import login_manager
from datetime import date

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)
    to_do = db.relationship('Task', backref='owner', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.hashed_password = generate_password_hash(password)

    def is_password_valid(self, password):
        return check_password_hash(self.hashed_password, password)


    def __repr__(self):
        return '<User {}>'.format(self.id)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=True)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content,  user_id, completed=False, date_created=None):
        self.content = content
        self.completed = completed
        self.date_created = date_created
        self.user_id = user_id

    def __repr__(self):
        return '<Task {}>'.format(self.id)

