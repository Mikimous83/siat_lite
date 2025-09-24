from .database_connection import DatabaseConnection
from typing import List, Dict, Optional


class PersonaModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def crear_persona(self, datos_persona: Dict) -> int:
        """Crear nueva persona asociada a un accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO personas (
                id_accidente, tipo_persona, nombre, apellido, dni, edad, sexo,
                direccion, telefono, estado_salud, hospital_traslado,
                lesiones_descripcion, parentesco_conductor, posicion_vehiculo,
                uso_cinturon, uso_casco
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(sql, (
                datos_persona['id_accidente'], datos_persona['tipo_persona'],
                datos_persona['nombre'], datos_persona['apellido'],
                datos_persona.get('dni'), datos_persona.get('edad'),
                datos_persona.get('sexo'), datos_persona.get('direccion'),
                datos_persona.get('telefono'), datos_persona.get('estado_salud'),
                datos_persona.get('hospital_traslado'), datos_persona.get('lesiones_descripcion'),
                datos_persona.get('parentesco_conductor'), datos_persona.get('posicion_vehiculo'),
                datos_persona.get('uso_cinturon'), datos_persona.get('uso_casco')
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear persona: {str(e)}")

    def obtener_personas_por_accidente(self, id_accidente: int) -> List[Dict]:
        """Obtener todas las personas de un accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM personas WHERE id_accidente = ? 
            ORDER BY tipo_persona, nombre
        """, (id_accidente,))

        personas = cursor.fetchall()
        return [self._dict_from_row(p) for p in personas]

    def obtener_personas_por_tipo(self, id_accidente: int, tipo_persona: str) -> List[Dict]:
        """Obtener personas por tipo (herido, fallecido, testigo, etc.)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM personas 
            WHERE id_accidente = ? AND tipo_persona = ?
            ORDER BY nombre
        """, (id_accidente, tipo_persona))

        personas = cursor.fetchall()
        return [self._dict_from_row(p) for p in personas]

    def actualizar_persona(self, id_persona: int, datos: Dict) -> bool:
        """Actualizar datos de una persona"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            UPDATE personas SET
                nombre = ?, apellido = ?, dni = ?, edad = ?, sexo = ?,
                estado_salud = ?, hospital_traslado = ?, lesiones_descripcion = ?
            WHERE id_persona = ?
            """

            cursor.execute(sql, (
                datos['nombre'], datos['apellido'], datos.get('dni'),
                datos.get('edad'), datos.get('sexo'), datos.get('estado_salud'),
                datos.get('hospital_traslado'), datos.get('lesiones_descripcion'),
                id_persona
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar persona: {str(e)}")

    def buscar_por_dni(self, dni: str) -> List[Dict]:
        """Buscar persona por DNI en todos los accidentes"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*, a.numero_caso, a.fecha
            FROM personas p
            JOIN accidentes a ON p.id_accidente = a.id_accidente
            WHERE p.dni = ?
            ORDER BY a.fecha DESC
        """, (dni,))

        personas = cursor.fetchall()
        return [self._dict_from_row(p) for p in personas]

    def obtener_estadisticas_lesiones(self) -> Dict:
        """Obtener estadísticas de lesiones"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                tipo_persona,
                COUNT(*) as total,
                COUNT(CASE WHEN estado_salud = 'grave' THEN 1 END) as graves
            FROM personas 
            WHERE tipo_persona IN ('herido', 'fallecido')
            GROUP BY tipo_persona
        """)

        return dict(cursor.fetchall())

    def _dict_from_row(self, row) -> Dict:
        """Convertir fila de BD a diccionario"""
        if not row:
            return {}

        columns = [desc[0] for desc in self.db.get_connection().cursor().description]
        return dict(zip(columns, row))