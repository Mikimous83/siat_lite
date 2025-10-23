from typing import List, Dict
from sqlite3 import Connection


class PersonaModel:
    """Gestión de personas involucradas en accidentes"""

    def __init__(self, db_connection):
        # db_connection es una instancia de DatabaseConnection
        self.db = db_connection

    # =====================================================
    # 🔹 CREAR PERSONA
    # =====================================================
    def crear_persona(self, datos_persona: Dict) -> int:
        """Crear nueva persona asociada a un accidente"""
        conn: Connection = self.db.get_connection()
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
                datos_persona["id_accidente"],
                datos_persona.get("tipo_persona"),
                datos_persona.get("nombre"),
                datos_persona.get("apellido"),
                datos_persona.get("dni"),
                datos_persona.get("edad"),
                datos_persona.get("sexo"),
                datos_persona.get("direccion"),
                datos_persona.get("telefono"),
                datos_persona.get("estado_salud"),
                datos_persona.get("hospital_traslado"),
                datos_persona.get("lesiones_descripcion"),
                datos_persona.get("parentesco_conductor"),
                datos_persona.get("posicion_vehiculo"),
                int(datos_persona.get("uso_cinturon", 0)),
                int(datos_persona.get("uso_casco", 0))
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear persona: {str(e)}")

    # =====================================================
    # 🔹 OBTENER PERSONAS
    # =====================================================
    def obtener_personas(self) -> List[Dict]:
        """Obtiene todas las personas con su número de caso"""
        conn: Connection = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                p.id_persona, a.numero_caso, p.tipo_persona, p.nombre, p.apellido,
                p.dni, p.edad, p.sexo, p.estado_salud, p.telefono
            FROM personas p
            JOIN accidentes a ON p.id_accidente = a.id_accidente
            ORDER BY a.numero_caso ASC
        """)

        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]

    # =====================================================
    # 🔹 ELIMINAR PERSONA
    # =====================================================
    def eliminar_persona(self, id_persona: int) -> bool:
        """Eliminar una persona del registro"""
        conn: Connection = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM personas WHERE id_persona = ?", (id_persona,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar persona: {str(e)}")
