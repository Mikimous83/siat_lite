from .database_connection import DatabaseConnection
from typing import List, Dict, Optional


class VehiculoModel:
    def __init__(self,db):
        self.db = db

    def crear_vehiculo(self, datos_vehiculo: Dict) -> int:
        """Crear nuevo vehículo asociado a un accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO vehiculos (
                id_accidente, tipo_vehiculo, marca, modelo, placa, año, color,
                numero_motor, numero_chasis, seguro_soat, estado_vehiculo,
                daños_descripcion, conductor_nombre, conductor_apellido,
                conductor_dni, conductor_licencia, conductor_telefono,
                propietario_nombre, propietario_dni
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(sql, (
                datos_vehiculo['id_accidente'], datos_vehiculo['tipo_vehiculo'],
                datos_vehiculo['marca'], datos_vehiculo['modelo'],
                datos_vehiculo['placa'], datos_vehiculo.get('año'),
                datos_vehiculo.get('color'), datos_vehiculo.get('numero_motor'),
                datos_vehiculo.get('numero_chasis'), datos_vehiculo.get('seguro_soat'),
                datos_vehiculo.get('estado_vehiculo'), datos_vehiculo.get('daños_descripcion'),
                datos_vehiculo['conductor_nombre'], datos_vehiculo['conductor_apellido'],
                datos_vehiculo['conductor_dni'], datos_vehiculo.get('conductor_licencia'),
                datos_vehiculo.get('conductor_telefono'), datos_vehiculo.get('propietario_nombre'),
                datos_vehiculo.get('propietario_dni')
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear vehículo: {str(e)}")

    def obtener_vehiculos_por_accidente(self, id_accidente: int) -> List[Dict]:
        """Obtener todos los vehículos de un accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM vehiculos WHERE id_accidente = ?
        """, (id_accidente,))

        vehiculos = cursor.fetchall()
        return [self._dict_from_row(v) for v in vehiculos]

    def actualizar_vehiculo(self, id_vehiculo: int, datos: Dict) -> bool:
        """Actualizar datos de un vehículo"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            UPDATE vehiculos SET
                tipo_vehiculo = ?, marca = ?, modelo = ?, placa = ?,
                año = ?, color = ?, estado_vehiculo = ?, daños_descripcion = ?
            WHERE id_vehiculo = ?
            """

            cursor.execute(sql, (
                datos['tipo_vehiculo'], datos['marca'], datos['modelo'],
                datos['placa'], datos.get('año'), datos.get('color'),
                datos.get('estado_vehiculo'), datos.get('daños_descripcion'),
                id_vehiculo
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar vehículo: {str(e)}")

    def eliminar_vehiculo(self, id_vehiculo: int) -> bool:
        """Eliminar vehículo"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
        conn.commit()
        return cursor.rowcount > 0

    def buscar_por_placa(self, placa: str) -> Optional[Dict]:
        """Buscar vehículo por placa"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v.*, a.numero_caso, a.fecha 
            FROM vehiculos v
            JOIN accidentes a ON v.id_accidente = a.id_accidente
            WHERE v.placa = ?
        """, (placa,))

        result = cursor.fetchone()
        return self._dict_from_row(result) if result else None

    def _dict_from_row(self, row) -> Dict:
        """Convertir fila de BD a diccionario"""
        if not row:
            return {}

        columns = [desc[0] for desc in self.db.get_connection().cursor().description]
        return dict(zip(columns, row))