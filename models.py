from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Reference: Flask-SQLAlchemy Documentation
# https://flask-sqlalchemy.palletsprojects.com/

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User model for storing user details.
    Inherits from UserMixin for Flask-Login integration.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    # Explicitly specify foreign_keys to avoid ambiguity with assigned_to_id
    tasks = db.relationship('Task', foreign_keys='Task.user_id', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    """
    Task model for storing task details.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium') # Low, Medium, High
    status = db.Column(db.String(20), nullable=False, default='To-Do') # To-Do, In Progress, Done, Cancelled
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_tasks', lazy=True)

    def __repr__(self):
        return f'<Task {self.title}>'
