from typing import List, Dict

class TipoDocumentoModel:
    def __init__(self, db):
        self.db = db

    def crear_tipo(self, nombre_tipo: str, descripcion: str) -> int:
        """Crear un nuevo tipo de documento."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO tipos_documento (nombre_tipo, descripcion)
                VALUES (?, ?)
            """, (nombre_tipo, descripcion))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear tipo de documento: {str(e)}")

    def obtener_todos(self) -> List[Dict]:
        """Obtener todos los tipos de documentos."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipos_documento ORDER BY nombre_tipo")
        filas = cursor.fetchall()
        return [self._dict_from_row(cursor, f) for f in filas]

    def actualizar_tipo(self, id_tipo_doc: int, datos: Dict) -> bool:
        """Actualizar tipo de documento."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tipos_documento
            SET nombre_tipo = ?, descripcion = ?
            WHERE id_tipo_doc = ?
        """, (datos.get("nombre_tipo"), datos.get("descripcion"), id_tipo_doc))
        conn.commit()
        return cursor.rowcount > 0

    def eliminar_tipo(self, id_tipo_doc: int) -> bool:
        """Eliminar tipo de documento."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipos_documento WHERE id_tipo_doc = ?", (id_tipo_doc,))
        conn.commit()
        return cursor.rowcount > 0

    def _dict_from_row(self, cursor, row) -> Dict:
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
