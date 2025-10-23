from typing import List, Dict

class AuditoriaModel:
    def __init__(self, db):
        self.db = db

    def registrar_accion(self, id_usuario: int, accion: str, tabla: str) -> int:
        """Registrar acción de usuario."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, accion, tabla_afectada)
                VALUES (?, ?, ?)
            """, (id_usuario, accion, tabla))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar auditoría: {str(e)}")

    def obtener_historial(self, limite: int = 50) -> List[Dict]:
        """Obtener las últimas acciones registradas."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, u.nombre, u.apellido
            FROM auditoria a
            LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario
            ORDER BY a.fecha_hora DESC
            LIMIT ?
        """, (limite,))
        filas = cursor.fetchall()
        return [self._dict_from_row(cursor, f) for f in filas]

    def limpiar_historial(self):
        """Vaciar la tabla de auditoría."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM auditoria")
        conn.commit()

    def _dict_from_row(self, cursor, row) -> Dict:
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
