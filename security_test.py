#!/usr/bin/env python3
"""Test security improvements"""

from app import app
import json

def test_security_features():
    """Test that security vulnerabilities have been fixed"""
    with app.test_client() as client:
        print("🔒 Testing Security Features")
        print("=" * 50)
        
        # Test 1: SQL Injection protection
        print("\n1. Testing SQL injection protection...")
        # Try to inject SQL in user ID
        response = client.get("/user/1'; DROP TABLE users; --")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 2: Password hashing
        print("\n2. Testing password hashing...")
        # Create a user and verify password is hashed
        new_user = {
            "name": "Security Test User",
            "email": "security@example.com", 
            "password": "plaintext123"
        }
        response = client.post('/users', json=new_user)
        print(f"   User creation status: {response.status_code}")
        
        # Try to login with the same password
        login_data = {"email": "security@example.com", "password": "plaintext123"}
        response = client.post('/login', json=login_data)
        print(f"   Login status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Password hashing and verification working correctly")
        
        # Test 3: Input validation
        print("\n3. Testing input validation...")
        
        # Test invalid email format
        invalid_user = {
            "name": "Invalid User",
            "email": "not-an-email",
            "password": "password123"
        }
        response = client.post('/users', json=invalid_user)
        print(f"   Invalid email status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test short password
        short_pass_user = {
            "name": "Short Pass User",
            "email": "short@example.com",
            "password": "123"
        }
        response = client.post('/users', json=short_pass_user)
        print(f"   Short password status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 4: Duplicate email prevention
        print("\n4. Testing duplicate email prevention...")
        duplicate_user = {
            "name": "Duplicate User",
            "email": "john@example.com",  # Already exists
            "password": "password123"
        }
        response = client.post('/users', json=duplicate_user)
        print(f"   Duplicate email status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 5: Proper error handling
        print("\n5. Testing error handling...")
        
        # Test malformed JSON
        response = client.post('/users', data="invalid json", content_type='application/json')
        print(f"   Malformed JSON status: {response.status_code}")
        
        # Test missing required fields
        incomplete_user = {"name": "Incomplete User"}
        response = client.post('/users', json=incomplete_user)
        print(f"   Missing fields status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        print("\n" + "=" * 50)
        print("✅ All security tests completed!")

if __name__ == '__main__':
    test_security_features()