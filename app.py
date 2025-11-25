from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task
from datetime import datetime
import os

# Reference: Flask Documentation
# https://flask.palletsprojects.com/

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_v2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    # Fetch tasks where user is author OR assigned_to
    from sqlalchemy import or_
    tasks = Task.query.filter(or_(Task.user_id == current_user.id, Task.assigned_to_id == current_user.id)).order_by(Task.date_posted.desc()).all()
    return render_template('dashboard.html', tasks=tasks)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already exists. Please choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! You can now log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        status = request.form.get('status')
        due_date_str = request.form.get('due_date')
        assigned_to_id = request.form.get('assigned_to')
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                pass # Handle invalid date format if necessary

        task = Task(title=title, description=description, priority=priority, status=status, due_date=due_date, author=current_user)
        
        if assigned_to_id:
            task.assigned_to_id = int(assigned_to_id)

        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('task_form.html', title='New Task', users=users)

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    
    users = User.query.all()
        
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.priority = request.form.get('priority')
        task.status = request.form.get('status')
        due_date_str = request.form.get('due_date')
        assigned_to_id = request.form.get('assigned_to')
        
        if due_date_str:
             try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
             except ValueError:
                pass
        else:
            task.due_date = None
            
        if assigned_to_id:
            task.assigned_to_id = int(assigned_to_id)
        else:
            task.assigned_to_id = None

        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('task_form.html', title='Edit Task', task=task, users=users)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/task/<int:task_id>/status', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    # Allow Author OR Assignee to update status
    if task.author != current_user and task.assigned_to != current_user:
        abort(403)
    
    new_status = request.form.get('status')
    if new_status:
        task.status = new_status
        db.session.commit()
        flash('Task status updated!', 'success')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
