import hashlib
from .database_connection import DatabaseConnection


class UsuarioModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def autenticar_usuario(self, email, password):
        """Autenticar usuario con email y contraseña"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        password_hash = self._hash_password(password)

        cursor.execute("""
            SELECT id_usuario, nombre, apellido, nivel_acceso
            FROM usuarios 
            WHERE email = ? AND password_hash = ? AND activo = 1
        """, (email, password_hash))

        return cursor.fetchone()

    def crear_usuario(self, datos_usuario):
        """Crear nuevo usuario"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        password_hash = self._hash_password(datos_usuario['password'])

        sql = """
        INSERT INTO usuarios (
            codigo_usuario, nombre, apellido, dni, cargo, 
            institucion, email, password_hash, nivel_acceso
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql, (
            datos_usuario['codigo_usuario'], datos_usuario['nombre'],
            datos_usuario['apellido'], datos_usuario['dni'],
            datos_usuario['cargo'], datos_usuario['institucion'],
            datos_usuario['email'], password_hash, datos_usuario['nivel_acceso']
        ))

        conn.commit()
        return cursor.lastrowid

    def _hash_password(self, password):
        """Hashear contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()