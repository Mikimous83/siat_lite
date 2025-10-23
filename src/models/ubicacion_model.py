from typing import List, Dict

class UbicacionModel:
    def __init__(self, db):
        self.db = db

    def crear_ubicacion(self, departamento: str, provincia: str, distrito: str) -> int:
        """Crear nueva ubicación."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ubicaciones (departamento, provincia, distrito)
                VALUES (?, ?, ?)
            """, (departamento, provincia, distrito))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear ubicación: {str(e)}")

    def obtener_todos(self) -> List[Dict]:
        """Obtener todas las ubicaciones registradas."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ubicaciones ORDER BY departamento, provincia, distrito")
        filas = cursor.fetchall()
        return [self._dict_from_row(cursor, f) for f in filas]

    def buscar_por_distrito(self, distrito: str) -> Dict:
        """Buscar ubicación por distrito."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ubicaciones WHERE distrito = ?", (distrito,))
        fila = cursor.fetchone()
        return self._dict_from_row(cursor, fila) if fila else {}

    def _dict_from_row(self, cursor, row) -> Dict:
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
