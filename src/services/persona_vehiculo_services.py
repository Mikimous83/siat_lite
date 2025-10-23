
from src.models.database_connection import DatabaseConnection as db
from src.models.accidente_model import Persona, Vehiculo


class PersonaService:
    """Servicio para gestión de personas involucradas"""

    @staticmethod
    def obtener_todas():
        """Obtiene todas las personas"""
        query = """
            SELECT p.*,
                   a.numero_caso
            FROM personas p
            LEFT JOIN accidentes a ON p.id_accidente = a.id_accidente
            ORDER BY p.id_persona DESC
        """
        return db.execute_query(query)

    @staticmethod
    def obtener_por_accidente(id_accidente):
        """Obtiene todas las personas de un accidente"""
        query = """
            SELECT * FROM personas
            WHERE id_accidente = ?
            ORDER BY tipo_persona, apellido, nombre
        """
        return db.execute_query(query, (id_accidente,))

    @staticmethod
    def obtener_por_id(id_persona):
        """Obtiene una persona por ID"""
        query = "SELECT * FROM personas WHERE id_persona = ?"
        results = db.execute_query(query, (id_persona,))
        return results[0] if results else None

    @staticmethod
    def crear(datos):
        """Crea una nueva persona"""
        query = """
            INSERT INTO personas (
                id_accidente, tipo_persona, nombre, apellido, dni, edad, sexo,
                direccion, telefono, estado_salud, hospital_traslado,
                lesiones_descripcion, parentesco_conductor, posicion_vehiculo,
                uso_cinturon, uso_casco
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            datos.get('id_accidente'),
            datos.get('tipo_persona'),
            datos.get('nombre'),
            datos.get('apellido'),
            datos.get('dni'),
            datos.get('edad'),
            datos.get('sexo'),
            datos.get('direccion'),
            datos.get('telefono'),
            datos.get('estado_salud'),
            datos.get('hospital_traslado'),
            datos.get('lesiones_descripcion'),
            datos.get('parentesco_conductor'),
            datos.get('posicion_vehiculo'),
            datos.get('uso_cinturon'),
            datos.get('uso_casco')
        )

        return db.execute_insert(query, params)

    @staticmethod
    def actualizar(id_persona, datos):
        """Actualiza una persona"""
        query = """
            UPDATE personas SET
                tipo_persona = ?, nombre = ?, apellido = ?, dni = ?,
                edad = ?, sexo = ?, direccion = ?, telefono = ?,
                estado_salud = ?, hospital_traslado = ?,
                lesiones_descripcion = ?, parentesco_conductor = ?,
                posicion_vehiculo = ?, uso_cinturon = ?, uso_casco = ?
            WHERE id_persona = ?
        """

        params = (
            datos.get('tipo_persona'),
            datos.get('nombre'),
            datos.get('apellido'),
            datos.get('dni'),
            datos.get('edad'),
            datos.get('sexo'),
            datos.get('direccion'),
            datos.get('telefono'),
            datos.get('estado_salud'),
            datos.get('hospital_traslado'),
            datos.get('lesiones_descripcion'),
            datos.get('parentesco_conductor'),
            datos.get('posicion_vehiculo'),
            datos.get('uso_cinturon'),
            datos.get('uso_casco'),
            id_persona
        )

        return db.execute_update(query, params)

    @staticmethod
    def eliminar(id_persona):
        """Elimina una persona"""
        query = "DELETE FROM personas WHERE id_persona = ?"
        return db.execute_delete(query, (id_persona,))

    @staticmethod
    def buscar_por_dni(dni):
        """Busca personas por DNI"""
        query = """
            SELECT p.*, a.numero_caso
            FROM personas p
            LEFT JOIN accidentes a ON p.id_accidente = a.id_accidente
            WHERE p.dni LIKE ?
        """
        return db.execute_query(query, (f"%{dni}%",))

    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de personas"""
        stats = {}

        # Total de personas registradas
        query = "SELECT COUNT(*) as total FROM personas"
        result = db.execute_query(query)
        stats['total'] = result[0]['total'] if result else 0

        # Por tipo de persona
        query = """
            SELECT tipo_persona, COUNT(*) as cantidad
            FROM personas
            GROUP BY tipo_persona
        """
        stats['por_tipo'] = db.execute_query(query)

        # Por estado de salud
        query = """
            SELECT estado_salud, COUNT(*) as cantidad
            FROM personas
            GROUP BY estado_salud
        """
        stats['por_estado_salud'] = db.execute_query(query)

        return stats


class VehiculoService:
    """Servicio para gestión de vehículos"""

    @staticmethod
    def obtener_todos():
        """Obtiene todos los vehículos"""
        query = """
            SELECT v.*,
                   a.numero_caso,
                   tv.nombre_tipo as tipo_nombre,
                   aseg.nombre as aseguradora_nombre
            FROM vehiculos v
            LEFT JOIN accidentes a ON v.id_accidente = a.id_accidente
            LEFT JOIN tipos_vehiculo tv ON v.id_tipo_vehiculo = tv.id_tipo_vehiculo
            LEFT JOIN aseguradoras aseg ON v.id_aseguradora = aseg.id_aseguradora
            ORDER BY v.id_vehiculo DESC
        """
        return db.execute_query(query)

    @staticmethod
    def obtener_por_accidente(id_accidente):
        """Obtiene todos los vehículos de un accidente"""
        query = """
            SELECT v.*,
                   tv.nombre_tipo as tipo_nombre,
                   aseg.nombre as aseguradora_nombre
            FROM vehiculos v
            LEFT JOIN tipos_vehiculo tv ON v.id_tipo_vehiculo = tv.id_tipo_vehiculo
            LEFT JOIN aseguradoras aseg ON v.id_aseguradora = aseg.id_aseguradora
            WHERE v.id_accidente = ?
        """
        return db.execute_query(query, (id_accidente,))

    @staticmethod
    def obtener_por_id(id_vehiculo):
        """Obtiene un vehículo por ID"""
        query = """
            SELECT v.*,
                   tv.nombre_tipo as tipo_nombre,
                   aseg.nombre as aseguradora_nombre
            FROM vehiculos v
            LEFT JOIN tipos_vehiculo tv ON v.id_tipo_vehiculo = tv.id_tipo_vehiculo
            LEFT JOIN aseguradoras aseg ON v.id_aseguradora = aseg.id_aseguradora
            WHERE v.id_vehiculo = ?
        """
        results = db.execute_query(query, (id_vehiculo,))
        return results[0] if results else None

    @staticmethod
    def crear(datos):
        """Crea un nuevo vehículo"""
        query = """
            INSERT INTO vehiculos (
                id_accidente, id_tipo_vehiculo, id_aseguradora, tipo_vehiculo,
                marca, modelo, placa, año, color, numero_motor, numero_chasis,
                estado_vehiculo, daños_descripcion, conductor_nombre,
                conductor_apellido, conductor_dni, conductor_licencia,
                conductor_telefono, propietario_nombre
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            datos.get('id_accidente'),
            datos.get('id_tipo_vehiculo'),
            datos.get('id_aseguradora'),
            datos.get('tipo_vehiculo'),
            datos.get('marca'),
            datos.get('modelo'),
            datos.get('placa'),
            datos.get('año'),
            datos.get('color'),
            datos.get('numero_motor'),
            datos.get('numero_chasis'),
            datos.get('estado_vehiculo'),
            datos.get('daños_descripcion'),
            datos.get('conductor_nombre'),
            datos.get('conductor_apellido'),
            datos.get('conductor_dni'),
            datos.get('conductor_licencia'),
            datos.get('conductor_telefono'),
            datos.get('propietario_nombre')
        )

        return db.execute_insert(query, params)

    @staticmethod
    def actualizar(id_vehiculo, datos):
        """Actualiza un vehículo"""
        query = """
            UPDATE vehiculos SET
                id_tipo_vehiculo = ?, id_aseguradora = ?, tipo_vehiculo = ?,
                marca = ?, modelo = ?, placa = ?, año = ?, color = ?,
                numero_motor = ?, numero_chasis = ?, estado_vehiculo = ?,
                daños_descripcion = ?, conductor_nombre = ?,
                conductor_apellido = ?, conductor_dni = ?,
                conductor_licencia = ?, conductor_telefono = ?,
                propietario_nombre = ?
            WHERE id_vehiculo = ?
        """

        params = (
            datos.get('id_tipo_vehiculo'),
            datos.get('id_aseguradora'),
            datos.get('tipo_vehiculo'),
            datos.get('marca'),
            datos.get('modelo'),
            datos.get('placa'),
            datos.get('año'),
            datos.get('color'),
            datos.get('numero_motor'),
            datos.get('numero_chasis'),
            datos.get('estado_vehiculo'),
            datos.get('daños_descripcion'),
            datos.get('conductor_nombre'),
            datos.get('conductor_apellido'),
            datos.get('conductor_dni'),
            datos.get('conductor_licencia'),
            datos.get('conductor_telefono'),
            datos.get('propietario_nombre'),
            id_vehiculo
        )

        return db.execute_update(query, params)

    @staticmethod
    def eliminar(id_vehiculo):
        """Elimina un vehículo"""
        query = "DELETE FROM vehiculos WHERE id_vehiculo = ?"
        return db.execute_delete(query, (id_vehiculo,))

    @staticmethod
    def buscar_por_placa(placa):
        """Busca vehículos por placa"""
        query = """
            SELECT v.*, a.numero_caso
            FROM vehiculos v
            LEFT JOIN accidentes a ON v.id_accidente = a.id_accidente
            WHERE v.placa LIKE ?
        """
        return db.execute_query(query, (f"%{placa}%",))

    @staticmethod
    def obtener_historial_placa(placa):
        """Obtiene el historial de accidentes de una placa"""
        query = """
            SELECT v.*, a.numero_caso, a.fecha, a.hora, a.lugar, a.estado_caso
            FROM vehiculos v
            JOIN accidentes a ON v.id_accidente = a.id_accidente
            WHERE v.placa = ?
            ORDER BY a.fecha DESC, a.hora DESC
        """
        return db.execute_query(query, (placa,))

    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de vehículos"""
        stats = {}

        # Total de vehículos registrados
        query = "SELECT COUNT(*) as total FROM vehiculos"
        result = db.execute_query(query)
        stats['total'] = result[0]['total'] if result else 0

        # Por tipo de vehículo
        query = """
            SELECT tipo_vehiculo, COUNT(*) as cantidad
            FROM vehiculos
            GROUP BY tipo_vehiculo
            ORDER BY cantidad DESC
        """
        stats['por_tipo'] = db.execute_query(query)

        # Por estado del vehículo
        query = """
            SELECT estado_vehiculo, COUNT(*) as cantidad
            FROM vehiculos
            GROUP BY estado_vehiculo
        """
        stats['por_estado'] = db.execute_query(query)

        # Marcas más involucradas
        query = """
            SELECT marca, COUNT(*) as cantidad
            FROM vehiculos
            GROUP BY marca
            ORDER BY cantidad DESC
            LIMIT 10
        """
        stats['marcas_top'] = db.execute_query(query)

        return stats