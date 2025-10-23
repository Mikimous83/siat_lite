from typing import List, Dict

class RolModel:
    def __init__(self, db):
        self.db = db

    def crear_rol(self, nombre_rol: str, descripcion: str) -> int:
        """Crear un nuevo rol."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO roles (nombre_rol, descripcion)
                VALUES (?, ?)
            """, (nombre_rol, descripcion))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear rol: {str(e)}")

    def obtener_todos(self) -> List[Dict]:
        """Obtener todos los roles."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM roles ORDER BY nombre_rol")
        filas = cursor.fetchall()
        return [self._dict_from_row(cursor, f) for f in filas]

    def eliminar_rol(self, id_rol: int) -> bool:
        """Eliminar rol."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM roles WHERE id_rol = ?", (id_rol,))
        conn.commit()
        return cursor.rowcount > 0

    def _dict_from_row(self, cursor, row) -> Dict:
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
