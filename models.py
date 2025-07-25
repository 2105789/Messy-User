import bcrypt
from database import db_manager
from typing import Optional, List, Dict, Any

class User:
    def __init__(self, id: int = None, name: str = None, email: str = None, password: str = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    
    @classmethod
    def get_all(cls) -> List['User']:
        """Get all users from database"""
        with db_manager.get_cursor() as cursor:
            cursor.execute("SELECT id, name, email FROM users")
            rows = cursor.fetchall()
            return [cls(id=row['id'], name=row['name'], email=row['email']) for row in rows]
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID"""
        with db_manager.get_cursor() as cursor:
            cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], name=row['name'], email=row['email'])
            return None
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Get user by email (for login)"""
        with db_manager.get_cursor() as cursor:
            cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], name=row['name'], email=row['email'], password=row['password'])
            return None
    
    def save(self) -> bool:
        """Save user to database"""
        try:
            with db_manager.get_cursor() as cursor:
                if self.id is None:
                    # Create new user
                    hashed_password = self.hash_password(self.password)
                    cursor.execute(
                        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                        (self.name, self.email, hashed_password)
                    )
                    self.id = cursor.lastrowid
                else:
                    # Update existing user
                    cursor.execute(
                        "UPDATE users SET name = ?, email = ? WHERE id = ?",
                        (self.name, self.email, self.id)
                    )
            return True
        except Exception:
            return False
    
    def delete(self) -> bool:
        """Delete user from database"""
        if self.id is None:
            return False
        
        try:
            with db_manager.get_cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
                return cursor.rowcount > 0
        except Exception:
            return False
    
    @classmethod
    def search_by_name(cls, name: str) -> List['User']:
        """Search users by name"""
        with db_manager.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email FROM users WHERE name LIKE ?",
                (f"%{name}%",)
            )
            rows = cursor.fetchall()
            return [cls(id=row['id'], name=row['name'], email=row['email']) for row in rows]