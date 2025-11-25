from flask import Flask, jsonify, request, abort
from models import db, User, Task
from functools import wraps
from datetime import datetime

# Reference: Flask API Development
# https://flask.palletsprojects.com/

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_v2.db'

db.init_app(app)

# User Endpoints 

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """
    Fetch all users.
    """
    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id, 
            'username': user.username,
            'email': user.email
        }
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Task Endpoints 

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Fetch all tasks. Optional filters: status, priority, user_id.
    """
    status = request.args.get('status')
    priority = request.args.get('priority')
    user_id = request.args.get('user_id')
    
    query = Task.query
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if user_id:
        query = query.filter_by(user_id=user_id)
        
    tasks = query.all()
    output = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'user_id': task.user_id,
            'assigned_to_id': task.assigned_to_id
        }
        output.append(task_data)
    return jsonify({'tasks': output})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.
    """
    data = request.get_json()
    if not data or not 'title' in data or not 'user_id' in data:
        return jsonify({'message': 'Missing required fields (title, user_id)'}), 400
        
    due_date = None
    if 'due_date' in data and data['due_date']:
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'To-Do'),
        due_date=due_date,
        user_id=data['user_id'],
        assigned_to_id=data.get('assigned_to_id')
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({'message': 'Task created successfully', 'task_id': new_task.id}), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a single task by ID.
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
        
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        'user_id': task.user_id,
        'assigned_to_id': task.assigned_to_id
    }
    return jsonify({'task': task_data})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update a task.
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
        
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'priority' in data:
        task.priority = data['priority']
    if 'status' in data:
        task.status = data['status']
    if 'assigned_to_id' in data:
        task.assigned_to_id = data['assigned_to_id']
    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                 return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            task.due_date = None
            
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task.
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
        
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
