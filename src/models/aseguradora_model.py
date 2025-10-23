from typing import List, Dict

class AseguradoraModel:
    def __init__(self, db):
        self.db = db

    def crear_aseguradora(self, nombre: str, telefono: str, direccion: str) -> int:
        """Registrar nueva aseguradora."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO aseguradoras (nombre, telefono, direccion)
                VALUES (?, ?, ?)
            """, (nombre, telefono, direccion))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar aseguradora: {str(e)}")

    def obtener_todas(self) -> List[Dict]:
        """Obtener todas las aseguradoras registradas."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aseguradoras ORDER BY nombre")
        filas = cursor.fetchall()
        return [self._dict_from_row(cursor, f) for f in filas]

    def eliminar_aseguradora(self, id_aseguradora: int) -> bool:
        """Eliminar una aseguradora."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aseguradoras WHERE id_aseguradora = ?", (id_aseguradora,))
        conn.commit()
        return cursor.rowcount > 0

    def _dict_from_row(self, cursor, row) -> Dict:
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
