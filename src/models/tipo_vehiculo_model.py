from typing import List, Dict
from .database_connection import DatabaseConnection


class TipoVehiculoModel:
    """Modelo para la tabla tipos_vehiculo"""

    def __init__(self):
        self.db = DatabaseConnection()

    def crear_tipo(self, datos: Dict) -> int:
        """Crea un nuevo tipo de vehículo"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO tipos_vehiculo (nombre_tipo, descripcion)
            VALUES (?, ?)
            """
            cursor.execute(sql, (datos['nombre_tipo'], datos.get('descripcion')))
            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear tipo de vehículo: {str(e)}")

    def obtener_todos(self) -> List[Dict]:
        """Obtiene todos los tipos de vehículo"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipos_vehiculo ORDER BY id_tipo_vehiculo")
        filas = cursor.fetchall()
        return [self._dict_from_row(row, cursor) for row in filas]

    def obtener_por_id(self, id_tipo_vehiculo: int) -> Dict:
        """Obtiene un tipo de vehículo por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipos_vehiculo WHERE id_tipo_vehiculo = ?", (id_tipo_vehiculo,))
        row = cursor.fetchone()
        return self._dict_from_row(row, cursor) if row else {}

    def actualizar(self, id_tipo_vehiculo: int, datos: Dict) -> bool:
        """Actualiza un tipo de vehículo"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE tipos_vehiculo
                SET nombre_tipo = ?, descripcion = ?
                WHERE id_tipo_vehiculo = ?
            """, (datos['nombre_tipo'], datos.get('descripcion'), id_tipo_vehiculo))
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar tipo de vehículo: {str(e)}")

    def eliminar(self, id_tipo_vehiculo: int) -> bool:
        """Elimina un tipo de vehículo"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipos_vehiculo WHERE id_tipo_vehiculo = ?", (id_tipo_vehiculo,))
        conn.commit()
        return cursor.rowcount > 0

    def _dict_from_row(self, row, cursor) -> Dict:
        """Convierte una fila en diccionario"""
        if not row:
            return {}
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
