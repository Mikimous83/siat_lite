import os
import sqlite3
from sqlite3 import Error


class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self):
        try:
            # 📁 Ruta base: 2 niveles arriba desde este archivo
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(base_dir, 'data', 'siatlite.db')

            if not os.path.exists(db_path):
                raise FileNotFoundError(f"❌ La base de datos no existe en: {db_path}")

            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA foreign_keys = 1")

            print(f"✅ Conectado correctamente a la base de datos:\n{db_path}")

            # 🔍 Mostrar todas las tablas disponibles
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tablas = [row[0] for row in cursor.fetchall()]

            if tablas:
                print("📋 Tablas detectadas en la base de datos:")
                for t in tablas:
                    print(f"   • {t}")
            else:
                print("⚠️ No se encontraron tablas en la base de datos.")

            self._connection = conn
            return conn

        except FileNotFoundError as e:
            print(f"❌ {e}")
            return None
        except Error as e:
            print(f"❌ Error al conectar con la base de datos: {e}")
            return None

    def get_connection(self):
        """Obtiene la conexión activa o la crea si no existe."""
        if self._connection is None:
            return self.connect()
        return self._connection

    def close(self):
        """Cierra la conexión si está activa."""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("🔒 Conexión cerrada correctamente.")
