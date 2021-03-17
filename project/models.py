from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from project import login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.hashed_password = generate_password_hash(password)

    def is_password_valid(self, password):
        return check_password_hash(self.hashed_password, password)


    def __repr__(self):
        return '<User {}>'.format(self.id)


