from .database_connection import DatabaseConnection
from typing import List, Dict, Optional


class ComisariaModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def crear_comisaria(self, datos_comisaria: Dict) -> int:
        """Crear nueva comisaría"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO comisarias (
                nombre_comisaria, distrito, provincia, departamento,
                direccion, telefono, comisario_cargo
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(sql, (
                datos_comisaria['nombre_comisaria'], datos_comisaria['distrito'],
                datos_comisaria['provincia'], datos_comisaria['departamento'],
                datos_comisaria.get('direccion'), datos_comisaria.get('telefono'),
                datos_comisaria.get('comisario_cargo')
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear comisaría: {str(e)}")

    def obtener_comisarias_activas(self) -> List[Dict]:
        """Obtener todas las comisarías activas"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM comisarias WHERE activo = 1 
            ORDER BY nombre_comisaria
        """)

        comisarias = cursor.fetchall()
        return [self._dict_from_row(c) for c in comisarias]

    def obtener_por_distrito(self, distrito: str) -> List[Dict]:
        """Obtener comisarías por distrito"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM comisarias 
            WHERE distrito = ? AND activo = 1
            ORDER BY nombre_comisaria
        """, (distrito,))

        comisarias = cursor.fetchall()
        return [self._dict_from_row(c) for c in comisarias]

    def _dict_from_row(self, row) -> Dict:
        """Convertir fila de BD a diccionario"""
        if not row:
            return {}

        columns = [desc[0] for desc in self.db.get_connection().cursor().description]
        return dict(zip(columns, row))