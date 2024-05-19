import unittest
from flask import Flask, g, redirect, url_for

class MockUser:
    def __init__(self, is_active=None, has_permission=None):
        self.is_active = is_active
        self.has_permission = has_permission

def login_required(f):
    def wrapped_function(*args, **kwargs):
        if not g.user or not g.user.is_active:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapped_function.__name__ = f.__name__
    return wrapped_function

def permission_required(f):
    def wrapped_function(*args, **kwargs):
        if not g.user or not g.user.has_permission:
            return redirect(url_for('no_permission'))
        return f(*args, **kwargs)
    wrapped_function.__name__ = f.__name__
    return wrapped_function

class TestDecorators(unittest.TestCase):
    def setUp(self):
        # Set up a Flask test app
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Create valid routes to prevent 404 errors
        @self.app.route('/login')
        def login():
            return 'Login Page', 200

        @self.app.route('/no_permission')
        def no_permission():
            return 'No Permission Page', 200
        
        @self.app.route('/')
        @login_required
        def index():
            return 'Protected View', 200
        
        @self.app.route('/permission')
        @permission_required
        def permission():
            return 'Permission Protected View', 200

    def tearDown(self):
        # Clean up the app context
        pass

    def test_login_required_inactive_user(self):
        with self.app.test_request_context("/"):
            g.user = MockUser(is_active=False)
            
            response = self.client.get('/')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.headers['Location'], "http://localhost/login")
            delattr(g, "user")

    def test_login_required_logged_in(self):
        with self.app.test_request_context("/"):
            g.user = MockUser(is_active=True)
            
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Protected View", response.data)
            delattr(g, "user")

    def test_login_required_not_logged_in(self):
        with self.app.test_request_context("/"):
            g.user = None
            
            response = self.client.get('/')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.headers['Location'], "http://localhost/login")
            delattr(g, "user")

    def test_permission_required_has_permission(self):
        with self.app.test_request_context("/"):
            g.user = MockUser(has_permission=True)
            
            response = self.client.get('/permission')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Permission Protected View", response.data)
            delattr(g, "user")

    def test_permission_required_no_permission(self):
        with self.app.test_request_context("/"):
            g.user = MockUser(has_permission=False)
            
            response = self.client.get('/permission')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.headers['Location'], "http://localhost/no_permission")
            delattr(g, "user")

if __name__ == '__main__':
    unittest.main()
