from typing import List, Dict
import sqlite3


class TipoViaModel:
    """Modelo para la tabla tipos_via"""

    def __init__(self, conn: sqlite3.Connection):
        """Recibe la conexión SQLite desde DataService"""
        self.conn = conn

    # --------------------------------------------------
    # 🧱 CRUD
    # --------------------------------------------------

    def crear(self, datos: Dict) -> int:
        """Crea un nuevo tipo de vía"""
        cursor = self.conn.cursor()
        try:
            sql = """
            INSERT INTO tipos_via (nombre_tipo, descripcion)
            VALUES (?, ?)
            """
            cursor.execute(sql, (datos["nombre_tipo"], datos.get("descripcion")))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al crear tipo de vía: {str(e)}")

    def listar(self) -> List[Dict]:
        """Obtiene todos los tipos de vía"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tipos_via ORDER BY id_tipo_via")
        filas = cursor.fetchall()
        return [self._dict_from_row(row, cursor) for row in filas]

    def obtener(self, id_tipo_via: int) -> Dict:
        """Obtiene un tipo de vía por ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tipos_via WHERE id_tipo_via = ?", (id_tipo_via,))
        row = cursor.fetchone()
        return self._dict_from_row(row, cursor) if row else {}

    def actualizar(self, id_tipo_via: int, datos: Dict) -> bool:
        """Actualiza un tipo de vía"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE tipos_via
                SET nombre_tipo = ?, descripcion = ?
                WHERE id_tipo_via = ?
                """,
                (datos["nombre_tipo"], datos.get("descripcion"), id_tipo_via),
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al actualizar tipo de vía: {str(e)}")

    def eliminar(self, id_tipo_via: int) -> bool:
        """Elimina un tipo de vía"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tipos_via WHERE id_tipo_via = ?", (id_tipo_via,))
        self.conn.commit()
        return cursor.rowcount > 0

    # --------------------------------------------------
    # 🔧 Helper
    # --------------------------------------------------

    def _dict_from_row(self, row, cursor) -> Dict:
        """Convierte una fila en diccionario"""
        if not row:
            return {}
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
