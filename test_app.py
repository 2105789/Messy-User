import unittest
import json
import os
from app import app

class UserAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        # Initialize database once
        from init_db import init_database
        init_database()
        
        cls.app = app.test_client()
        cls.app.testing = True
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_get_all_users(self):
        """Test getting all users"""
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)  # At least 3 users from sample data
    
    def test_get_user_by_id(self):
        """Test getting a specific user"""
        response = self.app.get('/user/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['email'], 'john@example.com')
        self.assertNotIn('password', data)  # Password should not be returned
    
    def test_get_nonexistent_user(self):
        """Test getting a user that doesn't exist"""
        response = self.app.get('/user/999')
        self.assertEqual(response.status_code, 404)
    
    def test_create_user(self):
        """Test creating a new user"""
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.app.post('/users', 
                                json=user_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['user']['name'], 'Test User')
    
    def test_create_user_duplicate_email(self):
        """Test creating a user with duplicate email"""
        user_data = {
            'name': 'Duplicate User',
            'email': 'john@example.com',  # Already exists
            'password': 'testpass123'
        }
        response = self.app.post('/users', 
                                json=user_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 409)
    
    def test_login_success(self):
        """Test successful login"""
        login_data = {
            'email': 'john@example.com',
            'password': 'password123'
        }
        response = self.app.post('/login',
                                json=login_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_login_failure(self):
        """Test failed login"""
        login_data = {
            'email': 'john@example.com',
            'password': 'wrongpassword'
        }
        response = self.app.post('/login',
                                json=login_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'failed')
    
    def test_search_users(self):
        """Test searching users by name"""
        response = self.app.get('/search?name=John')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['name'], 'John Doe')

if __name__ == '__main__':
    unittest.main()