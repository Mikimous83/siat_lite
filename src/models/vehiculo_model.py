from typing import List, Dict

class VehiculoModel:
    def __init__(self, db):
        self.db = db

    # =====================================================
    # 🔹 CREAR VEHÍCULO
    # =====================================================
    def crear_vehiculo(self, datos: Dict) -> int:
        """Registrar un vehículo asociado a un accidente."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # Verificar existencia del accidente
            cursor.execute("SELECT COUNT(*) FROM accidentes WHERE id_accidente = ?", (datos["id_accidente"],))
            if cursor.fetchone()[0] == 0:
                raise Exception(f"❌ No existe un accidente con ID {datos['id_accidente']}")

            # Insertar vehículo
            sql = """
            INSERT INTO vehiculos (
                id_accidente, id_tipo_vehiculo, id_aseguradora, tipo_vehiculo, marca, modelo, placa,
                anio, color, numero_motor, numero_chasis, estado_vehiculo, daños_descripcion,
                conductor_nombre, conductor_apellido, conductor_dni, conductor_licencia,
                conductor_telefono, propietario_nombre
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(sql, (
                datos["id_accidente"],
                datos.get("id_tipo_vehiculo"),
                datos.get("id_aseguradora"),
                datos.get("tipo_vehiculo"),
                datos.get("marca"),
                datos.get("modelo"),
                datos.get("placa"),
                datos.get("anio"),
                datos.get("color"),
                datos.get("numero_motor"),
                datos.get("numero_chasis"),
                datos.get("estado_vehiculo"),
                datos.get("daños_descripcion"),
                datos.get("conductor_nombre"),
                datos.get("conductor_apellido"),
                datos.get("conductor_dni"),
                datos.get("conductor_licencia"),
                datos.get("conductor_telefono"),
                datos.get("propietario_nombre")
            ))

            conn.commit()
            print(f"✅ Vehículo registrado correctamente (Accidente ID {datos['id_accidente']})")
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar vehículo: {str(e)}")

    # =====================================================
    # 🔹 OBTENER VEHÍCULOS POR ACCIDENTE
    # =====================================================
    def obtener_por_accidente(self, id_accidente: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM vehiculos 
            WHERE id_accidente = ?
            ORDER BY tipo_vehiculo, marca
        """, (id_accidente,))
        rows = cursor.fetchall()
        return [self._dict_from_row(cursor, r) for r in rows]

    # =====================================================
    # 🔹 OBTENER VEHÍCULO POR ID
    # =====================================================
    def obtener_por_id(self, id_vehiculo: int) -> Dict:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
        row = cursor.fetchone()
        return self._dict_from_row(cursor, row) if row else {}

    # =====================================================
    # 🔹 ACTUALIZAR VEHÍCULO
    # =====================================================
    def actualizar_vehiculo(self, id_vehiculo: int, datos: Dict) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            UPDATE vehiculos SET
                id_tipo_vehiculo = ?, id_aseguradora = ?, tipo_vehiculo = ?, marca = ?, modelo = ?, 
                placa = ?, anio = ?, color = ?, numero_motor = ?, numero_chasis = ?, 
                estado_vehiculo = ?, daños_descripcion = ?, conductor_nombre = ?, 
                conductor_apellido = ?, conductor_dni = ?, conductor_licencia = ?, 
                conductor_telefono = ?, propietario_nombre = ?
            WHERE id_vehiculo = ?
            """

            cursor.execute(sql, (
                datos.get("id_tipo_vehiculo"),
                datos.get("id_aseguradora"),
                datos.get("tipo_vehiculo"),
                datos.get("marca"),
                datos.get("modelo"),
                datos.get("placa"),
                datos.get("anio"),
                datos.get("color"),
                datos.get("numero_motor"),
                datos.get("numero_chasis"),
                datos.get("estado_vehiculo"),
                datos.get("daños_descripcion"),
                datos.get("conductor_nombre"),
                datos.get("conductor_apellido"),
                datos.get("conductor_dni"),
                datos.get("conductor_licencia"),
                datos.get("conductor_telefono"),
                datos.get("propietario_nombre"),
                id_vehiculo
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar vehículo: {str(e)}")

    # =====================================================
    # 🔹 ELIMINAR VEHÍCULO
    # =====================================================
    def eliminar_vehiculo(self, id_vehiculo: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar vehículo: {str(e)}")
    # =====================================================
    # 🔹 BUSCAR PERSONA
    # =====================================================
    def buscar_persona_por_dni(self, dni: str) -> dict:
        """Busca en la tabla personas un registro por DNI."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_persona, nombre, apellido, dni, telefono
            FROM personas
            WHERE dni = ?
        """, (dni,))
        row = cursor.fetchone()
        return self._dict_from_row(cursor, row) if row else {}

    # =====================================================
    # 🔹 UTILIDAD: convertir fila en dict
    # =====================================================
    def _dict_from_row(self, cursor, row) -> Dict:
        if not row:
            return {}
        cols = [desc[0] for desc in cursor.description]
        return dict(zip(cols, row))
