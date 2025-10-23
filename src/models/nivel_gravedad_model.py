from typing import List, Dict
import sqlite3


class NivelGravedadModel:
    """Modelo para la tabla niveles_gravedad"""

    def __init__(self, conn: sqlite3.Connection):
        """Recibe una conexión existente (no crea una nueva)"""
        self.conn = conn

    # ---------------------- CRUD ----------------------

    def crear(self, datos: Dict) -> int:
        """Crea un nuevo nivel de gravedad"""
        cursor = self.conn.cursor()
        try:
            sql = """
            INSERT INTO niveles_gravedad (nivel, descripcion)
            VALUES (?, ?)
            """
            cursor.execute(sql, (datos["nivel"], datos.get("descripcion")))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al crear nivel de gravedad: {str(e)}")

    def listar(self) -> List[Dict]:
        """Obtiene todos los niveles de gravedad"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM niveles_gravedad ORDER BY id_gravedad")
        filas = cursor.fetchall()
        return [self._dict_from_row(row, cursor) for row in filas]

    def obtener(self, id_gravedad: int) -> Dict:
        """Obtiene un nivel de gravedad por ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM niveles_gravedad WHERE id_gravedad = ?", (id_gravedad,))
        row = cursor.fetchone()
        return self._dict_from_row(row, cursor) if row else {}

    def actualizar(self, id_gravedad: int, datos: Dict) -> bool:
        """Actualiza un nivel de gravedad"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE niveles_gravedad
                SET nivel = ?, descripcion = ?
                WHERE id_gravedad = ?
                """,
                (datos["nivel"], datos.get("descripcion"), id_gravedad),
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al actualizar nivel de gravedad: {str(e)}")

    def eliminar(self, id_gravedad: int) -> bool:
        """Elimina un nivel de gravedad"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM niveles_gravedad WHERE id_gravedad = ?", (id_gravedad,))
        self.conn.commit()
        return cursor.rowcount > 0

    # ---------------------- Helper ----------------------

    def _dict_from_row(self, row, cursor) -> Dict:
        """Convierte una fila en diccionario"""
        if not row:
            return {}
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
