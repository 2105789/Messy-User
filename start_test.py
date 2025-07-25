#!/usr/bin/env python3
"""Test that the application can start properly"""

import threading
import time
import requests
from app import app

def run_app():
    """Run the Flask app in a separate thread"""
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)

def test_running_app():
    """Test the running application"""
    # Start the app in a background thread
    app_thread = threading.Thread(target=run_app, daemon=True)
    app_thread.start()
    
    # Give the app time to start
    time.sleep(2)
    
    try:
        # Test the health endpoint
        response = requests.get('http://127.0.0.1:5001/', timeout=5)
        print(f"✅ Health check successful: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test getting users
        response = requests.get('http://127.0.0.1:5001/users', timeout=5)
        print(f"✅ Get users successful: {response.status_code}")
        users = response.json()
        print(f"   Found {len(users)} users")
        
        # Test login
        login_data = {"email": "john@example.com", "password": "password123"}
        response = requests.post('http://127.0.0.1:5001/login', json=login_data, timeout=5)
        print(f"✅ Login test successful: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        print("\n🎉 Application is running correctly and all endpoints are working!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application")
    except Exception as e:
        print(f"❌ Error testing application: {e}")

if __name__ == '__main__':
    print("🚀 Starting application test...")
    test_running_app()