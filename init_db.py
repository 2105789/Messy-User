import sqlite3
import os
from models import User

def init_database():
    # Remove existing database to start fresh
    if os.path.exists('users.db'):
        os.remove('users.db')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

    # Create sample users with hashed passwords
    sample_users = [
        User(name='John Doe', email='john@example.com', password='password123'),
        User(name='Jane Smith', email='jane@example.com', password='secret456'),
        User(name='Bob Johnson', email='bob@example.com', password='qwerty789')
    ]

    for user in sample_users:
        user.save()

    print("Database initialized with sample data")
    print("Sample login credentials:")
    print("- john@example.com / password123")
    print("- jane@example.com / secret456")
    print("- bob@example.com / qwerty789")

if __name__ == '__main__':
    init_database()