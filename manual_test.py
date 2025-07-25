#!/usr/bin/env python3
"""Manual test script to verify API functionality"""

import json
from app import app

def test_endpoints():
    """Test all API endpoints manually"""
    with app.test_client() as client:
        print("🧪 Testing User Management API")
        print("=" * 50)
        
        # Test 1: Health check
        print("\n1. Testing health check...")
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 2: Get all users
        print("\n2. Testing get all users...")
        response = client.get('/users')
        users = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Found {len(users)} users")
        
        # Test 3: Get specific user
        print("\n3. Testing get user by ID...")
        response = client.get('/user/1')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            user = response.get_json()
            print(f"   User: {user['name']} ({user['email']})")
        
        # Test 4: Login test
        print("\n4. Testing login...")
        login_data = {"email": "john@example.com", "password": "password123"}
        response = client.post('/login', json=login_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 5: Create new user
        print("\n5. Testing create user...")
        new_user = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        response = client.post('/users', json=new_user)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            result = response.get_json()
            print(f"   Created user: {result['user']['name']}")
        
        # Test 6: Search users
        print("\n6. Testing search users...")
        response = client.get('/search?name=John')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            results = response.get_json()
            print(f"   Found {len(results)} users matching 'John'")
        
        # Test 7: Invalid login
        print("\n7. Testing invalid login...")
        bad_login = {"email": "john@example.com", "password": "wrongpassword"}
        response = client.post('/login', json=bad_login)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 8: Get non-existent user
        print("\n8. Testing non-existent user...")
        response = client.get('/user/999')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        print("\n" + "=" * 50)
        print("✅ All manual tests completed successfully!")

if __name__ == '__main__':
    test_endpoints()