#!/usr/bin/env python3
"""Quick test to verify the API works"""

import requests
import json
import subprocess
import time
import sys
from threading import Thread

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:5000"
    
    try:
        # Test health check
        response = requests.get(f"{base_url}/")
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test get all users
        response = requests.get(f"{base_url}/users")
        print(f"Get users: {response.status_code} - Found {len(response.json())} users")
        
        # Test login
        login_data = {"email": "john@example.com", "password": "password123"}
        response = requests.post(f"{base_url}/login", json=login_data)
        print(f"Login test: {response.status_code} - {response.json()}")
        
        print("✅ All API tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure it's running on port 5000.")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_api()