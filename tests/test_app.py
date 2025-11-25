import unittest
import warnings
from sqlalchemy.exc import SAWarning
from app import app, db, User, Task

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Suppress SQLAlchemy Legacy API warnings for cleaner output
        warnings.simplefilter('ignore', category=SAWarning)
        
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False 
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_redirect(self):
        print("\n[TEST] Checking Index Redirect (Unauthenticated)...")
        # Should redirect to login if not authenticated
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Login', response.data)
        print(" -> PASSED: Successfully redirected to Login page.")

    def test_register_and_login(self):
        print("\n[TEST] Checking User Registration and Login...")
        # Register
        response = self.app.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Account created!', response.data)
        print(" -> Registration PASSED.")

        # Login
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'My Tasks', response.data)
        print(" -> Login PASSED.")

    def test_create_task(self):
        print("\n[TEST] Checking Task Creation...")
        # Register and Login first
        self.app.post('/register', data=dict(username='testuser', email='test@example.com', password='password123'), follow_redirects=True)
        self.app.post('/login', data=dict(username='testuser', password='password123'), follow_redirects=True)

        # Create Task
        response = self.app.post('/task/new', data=dict(
            title='Test Task',
            description='This is a test task',
            priority='High',
            status='To-Do',
            due_date='2023-12-31'
        ), follow_redirects=True)
        self.assertIn(b'Your task has been created!', response.data)
        self.assertIn(b'Test Task', response.data)
        print(" -> PASSED: Task created successfully.")

    def test_assignee_update_status(self):
        print("\n[TEST] Checking Assignee Status Update Permission...")
        # Create two users
        self.app.post('/register', data=dict(username='author', email='author@example.com', password='password'), follow_redirects=True)
        self.app.post('/register', data=dict(username='assignee', email='assignee@example.com', password='password'), follow_redirects=True)
        
        # Login as Author and create task assigned to Assignee
        self.app.post('/login', data=dict(username='author', password='password'), follow_redirects=True)
        self.app.post('/task/new', data=dict(
            title='Assigned Task',
            priority='Medium',
            status='To-Do',
            assigned_to='2' # ID of assignee
        ), follow_redirects=True)
        self.app.get('/logout', follow_redirects=True)

        # Login as Assignee and update status
        self.app.post('/login', data=dict(username='assignee', password='password'), follow_redirects=True)
        response = self.app.post('/task/1/status', data=dict(status='Done'), follow_redirects=True)
        
        self.assertIn(b'Task status updated!', response.data)
        
        # Verify status change
        with app.app_context():
            task = Task.query.get(1)
            self.assertEqual(task.status, 'Done')
        print(" -> PASSED: Assignee successfully updated task status.")

if __name__ == '__main__':
    unittest.main()