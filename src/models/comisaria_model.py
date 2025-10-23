from .database_connection import DatabaseConnection
from typing import List, Dict, Optional

class ComisariaModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def crear_comisaria(self, datos_comisaria: Dict) -> int:
        """Crear una nueva comisaría"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO comisarias (
                nombre_comisaria, distrito, provincia, departamento,
                direccion, telefono, comisario_cargo, activo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(sql, (
                datos_comisaria['nombre_comisaria'],
                datos_comisaria['distrito'],
                datos_comisaria['provincia'],
                datos_comisaria['departamento'],
                datos_comisaria.get('direccion'),
                datos_comisaria.get('telefono'),
                datos_comisaria.get('comisario_cargo'),
                datos_comisaria.get('activo', 1)  # por defecto activa
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear comisaría: {str(e)}")

    def actualizar_comisaria(self, id_comisaria: int, datos_comisaria: Dict) -> None:
        """Actualizar información de una comisaría"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            UPDATE comisarias SET
                nombre_comisaria = ?,
                distrito = ?,
                provincia = ?,
                departamento = ?,
                direccion = ?,
                telefono = ?,
                comisario_cargo = ?,
                activo = ?
            WHERE id_comisaria = ?
            """

            cursor.execute(sql, (
                datos_comisaria['nombre_comisaria'],
                datos_comisaria['distrito'],
                datos_comisaria['provincia'],
                datos_comisaria['departamento'],
                datos_comisaria.get('direccion'),
                datos_comisaria.get('telefono'),
                datos_comisaria.get('comisario_cargo'),
                datos_comisaria.get('activo', 1),
                id_comisaria
            ))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar comisaría: {str(e)}")

    def obtener_comisarias_activas(self) -> List[Dict]:
        """Obtener todas las comisarías activas"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM comisarias
            WHERE activo = 1
            ORDER BY nombre_comisaria
        """)

        comisarias = cursor.fetchall()
        return [self._dict_from_row(c, cursor) for c in comisarias]

    def obtener_por_distrito(self, distrito: str) -> List[Dict]:
        """Obtener comisarías activas por distrito"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM comisarias 
            WHERE distrito = ? AND activo = 1
            ORDER BY nombre_comisaria
        """, (distrito,))

        comisarias = cursor.fetchall()
        return [self._dict_from_row(c, cursor) for c in comisarias]

    def obtener_por_id(self, id_comisaria: int) -> Optional[Dict]:
        """Obtener una comisaría por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM comisarias WHERE id_comisaria = ?
        """, (id_comisaria,))

        row = cursor.fetchone()
        return self._dict_from_row(row, cursor) if row else None

    def eliminar_comisaria(self, id_comisaria: int) -> None:
        """Eliminar (o desactivar) una comisaría"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE comisarias SET activo = 0 WHERE id_comisaria = ?
            """, (id_comisaria,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar comisaría: {str(e)}")

    def _dict_from_row(self, row, cursor) -> Dict:
        """Convierte una fila en diccionario"""
        if not row:
            return {}
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
