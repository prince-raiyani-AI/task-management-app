import unittest
import warnings
from sqlalchemy.exc import SAWarning
from api import app, db
from models import User, Task

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        # Suppress SQLAlchemy Legacy API warnings
        warnings.simplefilter('ignore', category=SAWarning)

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            user = User(username='apiuser', email='api@example.com', password_hash='hash')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users(self):
        print("\n[TEST] API: Fetching All Users...")
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'apiuser', response.data)
        self.assertIn(b'api@example.com', response.data)
        print(" -> PASSED: Users retrieved successfully.")

    def test_create_task(self):
        print("\n[TEST] API: Creating a New Task...")
        response = self.app.post('/api/tasks', 
                                 json={'title': 'New Task', 'user_id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Task created successfully', response.data)
        print(" -> PASSED: Task created successfully.")

    def test_get_tasks(self):
        print("\n[TEST] API: Fetching Tasks...")
        self.app.post('/api/tasks', 
                      json={'title': 'Task 1', 'user_id': 1})
        
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task 1', response.data)
        print(" -> PASSED: Tasks retrieved successfully.")

    def test_delete_user(self):
        print("\n[TEST] API: Deleting a User...")
        response = self.app.delete('/api/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted successfully', response.data)
        print(" -> PASSED: User deleted successfully.")
