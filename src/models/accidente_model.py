from .database_connection import DatabaseConnection
from datetime import datetime


class AccidenteModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def crear_accidente(self, datos_accidente):
        """Crear nuevo accidente en la base de datos"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO accidentes (
                numero_caso, fecha, hora, lugar, distrito, tipo_accidente,
                gravedad, heridos, fallecidos, vehiculos_involucrados,
                descripcion, id_usuario_registro
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            numero_caso = self._generar_numero_caso()

            cursor.execute(sql, (
                numero_caso, datos_accidente['fecha'], datos_accidente['hora'],
                datos_accidente['lugar'], datos_accidente['distrito'],
                datos_accidente['tipo_accidente'], datos_accidente['gravedad'],
                datos_accidente['heridos'], datos_accidente['fallecidos'],
                datos_accidente['vehiculos_involucrados'],
                datos_accidente['descripcion'], datos_accidente['id_usuario']
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear accidente: {str(e)}")

    def obtener_accidentes(self, filtros=None):
        """Obtener lista de accidentes con filtros opcionales"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM accidentes WHERE 1=1"
        params = []

        if filtros:
            if filtros.get('fecha_desde'):
                sql += " AND fecha >= ?"
                params.append(filtros['fecha_desde'])
            if filtros.get('fecha_hasta'):
                sql += " AND fecha <= ?"
                params.append(filtros['fecha_hasta'])
            if filtros.get('tipo_accidente'):
                sql += " AND tipo_accidente = ?"
                params.append(filtros['tipo_accidente'])

        cursor.execute(sql, params)
        return cursor.fetchall()

    def _generar_numero_caso(self):
        """Generar número único de caso"""
        año = datetime.now().year
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM accidentes 
            WHERE strftime('%Y', fecha_registro) = ?
        """, (str(año),))

        count = cursor.fetchone()[0]
        return f"ACC-{año}-{(count + 1):06d}"