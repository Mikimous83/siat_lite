import sqlite3
from sqlite3 import Error
import os


class DatabaseConnection:
    """Singleton para manejar conexión a la base de datos"""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self):
        try:
            db_path = os.path.join('data', 'siatlite.db')
            self._connection = sqlite3.connect(db_path)
            self._connection.execute("PRAGMA foreign_keys = 1")
            return self._connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def get_connection(self):
        if self._connection is None:
            return self.connect()
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None