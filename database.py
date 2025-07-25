import sqlite3
import threading
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self._local = threading.local()
    
    def get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def close_connections(self):
        """Close all thread-local connections"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')

db_manager = DatabaseManager()