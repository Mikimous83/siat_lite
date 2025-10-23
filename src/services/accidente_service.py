"""
Servicio de gestión de accidentes
Contiene toda la lógica de negocio para accidentes
"""
from src.models.database_connection import DatabaseConnection as db
from datetime import datetime
from src.utils.logger import logger


class AccidenteService:
    """Servicio para operaciones CRUD y lógica de negocio de accidentes"""

    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los accidentes con información relacionada

        Returns:
            list: Lista de accidentes con datos completos
        """
        query = """
            SELECT a.*, 
                   t.nombre_tipo as tipo_accidente,
                   g.nivel as gravedad,
                   c.nombre_comisaria,
                   tv.nombre_tipo as tipo_via,
                   u.nombre || ' ' || u.apellido as usuario_registro,
                   ub.departamento,
                   ub.provincia,
                   ub.distrito
            FROM accidentes a
            LEFT JOIN tipos_accidente t ON a.id_tipo = t.id_tipo
            LEFT JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
            LEFT JOIN comisarias c ON a.id_comisaria = c.id_comisaria
            LEFT JOIN tipos_via tv ON a.id_tipo_via = tv.id_tipo_via
            LEFT JOIN usuarios u ON a.id_usuario_registro = u.id_usuario
            LEFT JOIN ubicaciones ub ON c.id_ubicacion = ub.id_ubicacion
            ORDER BY a.fecha DESC, a.hora DESC
        """

        try:
            resultados = db.execute_query(query)
            logger.info(f"Obtenidos {len(resultados)} accidentes")
            return resultados
        except Exception as e:
            logger.error(f"Error al obtener accidentes: {e}", exc_info=True)
            return []

    @staticmethod
    def obtener_por_id(id_accidente):
        """
        Obtiene un accidente específico por ID

        Args:
            id_accidente: ID del accidente

        Returns:
            dict: Datos del accidente o None si no existe
        """
        query = """
            SELECT a.*, 
                   t.nombre_tipo as tipo_accidente,
                   t.gravedad_base,
                   g.nivel as gravedad,
                   g.descripcion as gravedad_descripcion,
                   c.nombre_comisaria,
                   c.direccion as comisaria_direccion,
                   c.telefono as comisaria_telefono,
                   tv.nombre_tipo as tipo_via,
                   u.nombre || ' ' || u.apellido as usuario_registro,
                   u.email as usuario_email,
                   ub.departamento,
                   ub.provincia,
                   ub.distrito
            FROM accidentes a
            LEFT JOIN tipos_accidente t ON a.id_tipo = t.id_tipo
            LEFT JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
            LEFT JOIN comisarias c ON a.id_comisaria = c.id_comisaria
            LEFT JOIN tipos_via tv ON a.id_tipo_via = tv.id_tipo_via
            LEFT JOIN usuarios u ON a.id_usuario_registro = u.id_usuario
            LEFT JOIN ubicaciones ub ON c.id_ubicacion = ub.id_ubicacion
            WHERE a.id_accidente = ?
        """

        try:
            resultados = db.execute_query(query, (id_accidente,))
            if resultados:
                logger.info(f"Accidente obtenido: ID {id_accidente}")
                return resultados[0]
            else:
                logger.warning(f"Accidente no encontrado: ID {id_accidente}")
                return None
        except Exception as e:
            logger.error(f"Error al obtener accidente {id_accidente}: {e}", exc_info=True)
            return None

    @staticmethod
    def obtener_por_numero_caso(numero_caso):
        """
        Obtiene un accidente por su número de caso

        Args:
            numero_caso: Número de caso del accidente

        Returns:
            dict: Datos del accidente o None si no existe
        """
        query = """
            SELECT a.*, 
                   t.nombre_tipo as tipo_accidente,
                   g.nivel as gravedad,
                   c.nombre_comisaria
            FROM accidentes a
            LEFT JOIN tipos_accidente t ON a.id_tipo = t.id_tipo
            LEFT JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
            LEFT JOIN comisarias c ON a.id_comisaria = c.id_comisaria
            WHERE a.numero_caso = ?
        """

        try:
            resultados = db.execute_query(query, (numero_caso,))
            if resultados:
                return resultados[0]
            return None
        except Exception as e:
            logger.error(f"Error al obtener accidente por número caso: {e}", exc_info=True)
            return None

    @staticmethod
    def crear(datos):
        """
        Crea un nuevo accidente

        Args:
            datos: Diccionario con los datos del accidente

        Returns:
            int: ID del accidente creado o None si falla
        """
        query = """
            INSERT INTO accidentes (
                numero_caso, fecha, hora, lugar, latitud, longitud,
                id_tipo, id_comisaria, id_usuario_registro, id_gravedad,
                descripcion, condiciones_climaticas, id_tipo_via,
                iluminacion, señalizacion, estado_caso,
                heridos, fallecidos, vehiculos_involucrados,
                croquis_url, fotos_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            # Generar número de caso automático si no se proporciona
            numero_caso = datos.get('numero_caso') or AccidenteService.generar_numero_caso()

            params = (
                numero_caso,
                datos.get('fecha'),
                datos.get('hora'),
                datos.get('lugar'),
                datos.get('latitud'),
                datos.get('longitud'),
                datos.get('id_tipo'),
                datos.get('id_comisaria'),
                datos.get('id_usuario_registro', 1),
                datos.get('id_gravedad'),
                datos.get('descripcion'),
                datos.get('condiciones_climaticas'),
                datos.get('id_tipo_via'),
                datos.get('iluminacion'),
                datos.get('señalizacion'),
                datos.get('estado_caso', 'Abierto'),
                datos.get('heridos', 0),
                datos.get('fallecidos', 0),
                datos.get('vehiculos_involucrados', 0),
                datos.get('croquis_url'),
                datos.get('fotos_url')
            )

            id_accidente = db.execute_insert(query, params)

            if id_accidente:
                logger.info(f"Accidente creado: ID {id_accidente}, Caso {numero_caso}")
            else:
                logger.error("Error al crear accidente: No se retornó ID")

            return id_accidente

        except Exception as e:
            logger.error(f"Error al crear accidente: {e}", exc_info=True)
            return None

    @staticmethod
    def actualizar(id_accidente, datos):
        """
        Actualiza un accidente existente

        Args:
            id_accidente: ID del accidente
            datos: Diccionario con los datos a actualizar

        Returns:
            int: Número de filas actualizadas
        """
        query = """
            UPDATE accidentes SET
                fecha = ?, hora = ?, lugar = ?, latitud = ?, longitud = ?,
                id_tipo = ?, id_comisaria = ?, id_gravedad = ?,
                descripcion = ?, condiciones_climaticas = ?, id_tipo_via = ?,
                iluminacion = ?, señalizacion = ?, estado_caso = ?,
                heridos = ?, fallecidos = ?, vehiculos_involucrados = ?,
                croquis_url = ?, fotos_url = ?,
                fecha_actualizacion = ?
            WHERE id_accidente = ?
        """

        try:
            params = (
                datos.get('fecha'),
                datos.get('hora'),
                datos.get('lugar'),
                datos.get('latitud'),
                datos.get('longitud'),
                datos.get('id_tipo'),
                datos.get('id_comisaria'),
                datos.get('id_gravedad'),
                datos.get('descripcion'),
                datos.get('condiciones_climaticas'),
                datos.get('id_tipo_via'),
                datos.get('iluminacion'),
                datos.get('señalizacion'),
                datos.get('estado_caso', 'Abierto'),
                datos.get('heridos', 0),
                datos.get('fallecidos', 0),
                datos.get('vehiculos_involucrados', 0),
                datos.get('croquis_url'),
                datos.get('fotos_url'),
                datetime.now().isoformat(),
                id_accidente
            )

            rows = db.execute_update(query, params)

            if rows > 0:
                logger.info(f"Accidente actualizado: ID {id_accidente}")
            else:
                logger.warning(f"No se actualizó accidente: ID {id_accidente}")

            return rows

        except Exception as e:
            logger.error(f"Error al actualizar accidente {id_accidente}: {e}", exc_info=True)
            return 0

    @staticmethod
    def eliminar(id_accidente):
        """
        Elimina un accidente (y registros relacionados por CASCADE)

        Args:
            id_accidente: ID del accidente

        Returns:
            int: Número de filas eliminadas
        """
        query = "DELETE FROM accidentes WHERE id_accidente = ?"

        try:
            rows = db.execute_delete(query, (id_accidente,))

            if rows > 0:
                logger.info(f"Accidente eliminado: ID {id_accidente}")
            else:
                logger.warning(f"No se eliminó accidente: ID {id_accidente}")

            return rows

        except Exception as e:
            logger.error(f"Error al eliminar accidente {id_accidente}: {e}", exc_info=True)
            return 0

    @staticmethod
    def cambiar_estado(id_accidente, nuevo_estado):
        """
        Cambia el estado de un accidente

        Args:
            id_accidente: ID del accidente
            nuevo_estado: Nuevo estado (Abierto, En Proceso, Cerrado, Archivado)

        Returns:
            bool: True si se actualizó correctamente
        """
        query = """
            UPDATE accidentes 
            SET estado_caso = ?, fecha_actualizacion = ?
            WHERE id_accidente = ?
        """

        try:
            params = (nuevo_estado, datetime.now().isoformat(), id_accidente)
            rows = db.execute_update(query, params)

            if rows > 0:
                logger.info(f"Estado de accidente {id_accidente} cambiado a: {nuevo_estado}")
                return True
            return False

        except Exception as e:
            logger.error(f"Error al cambiar estado: {e}", exc_info=True)
            return False

    @staticmethod
    def generar_numero_caso():
        """
        Genera un número de caso único
        Formato: ACC-YYYY-NNN (ej: ACC-2025-001)

        Returns:
            str: Número de caso generado
        """
        try:
            año_actual = datetime.now().year

            # Contar casos del año actual
            query = """
                SELECT COUNT(*) as total 
                FROM accidentes 
                WHERE numero_caso LIKE ?
            """

            resultado = db.execute_query(query, (f'ACC-{año_actual}-%',))
            total = resultado[0]['total'] if resultado else 0

            # Generar número con padding de 3 dígitos
            numero = f'ACC-{año_actual}-{str(total + 1).zfill(3)}'

            logger.debug(f"Número de caso generado: {numero}")
            return numero

        except Exception as e:
            logger.error(f"Error al generar número de caso: {e}", exc_info=True)
            # Fallback con timestamp
            return f'ACC-{datetime.now().strftime("%Y%m%d%H%M%S")}'

    @staticmethod
    def obtener_estadisticas():
        """
        Obtiene estadísticas generales de accidentes

        Returns:
            dict: Diccionario con estadísticas
        """
        stats = {}

        try:
            # Total de accidentes
            query = "SELECT COUNT(*) as total FROM accidentes"
            resultado = db.execute_query(query)
            stats['total'] = resultado[0]['total'] if resultado else 0

            # Accidentes del mes actual
            query = """
                SELECT COUNT(*) as total 
                FROM accidentes 
                WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
            """
            resultado = db.execute_query(query)
            stats['mes_actual'] = resultado[0]['total'] if resultado else 0

            # Accidentes de la semana actual
            query = """
                SELECT COUNT(*) as total 
                FROM accidentes 
                WHERE fecha >= date('now', 'weekday 0', '-7 days')
            """
            resultado = db.execute_query(query)
            stats['semana_actual'] = resultado[0]['total'] if resultado else 0

            # Accidentes de hoy
            query = """
                SELECT COUNT(*) as total 
                FROM accidentes 
                WHERE fecha = date('now')
            """
            resultado = db.execute_query(query)
            stats['hoy'] = resultado[0]['total'] if resultado else 0

            # Accidentes graves
            query = """
                SELECT COUNT(*) as total 
                FROM accidentes a
                JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
                WHERE g.nivel = 'Grave'
            """
            resultado = db.execute_query(query)
            stats['graves'] = resultado[0]['total'] if resultado else 0

            # Casos pendientes (Abierto o En Proceso)
            query = """
                SELECT COUNT(*) as total 
                FROM accidentes 
                WHERE estado_caso IN ('Abierto', 'En Proceso')
            """
            resultado = db.execute_query(query)
            stats['pendientes'] = resultado[0]['total'] if resultado else 0

            # Total de heridos y fallecidos
            query = """
                SELECT 
                    SUM(heridos) as total_heridos,
                    SUM(fallecidos) as total_fallecidos
                FROM accidentes
            """
            resultado = db.execute_query(query)
            if resultado and resultado[0]['total_heridos']:
                stats['total_heridos'] = resultado[0]['total_heridos']
                stats['total_fallecidos'] = resultado[0]['total_fallecidos']
            else:
                stats['total_heridos'] = 0
                stats['total_fallecidos'] = 0

            # Promedio de vehículos por accidente
            query = "SELECT AVG(vehiculos_involucrados) as promedio FROM accidentes"
            resultado = db.execute_query(query)
            stats['promedio_vehiculos'] = round(resultado[0]['promedio'], 2) if resultado and resultado[0][
                'promedio'] else 0

            # Estadísticas por estado
            query = """
                SELECT estado_caso, COUNT(*) as cantidad
                FROM accidentes
                GROUP BY estado_caso
            """
            resultados = db.execute_query(query)
            stats['por_estado'] = {r['estado_caso']: r['cantidad'] for r in resultados}

            logger.info("Estadísticas de accidentes generadas")
            return stats

        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {e}", exc_info=True)
            return {
                'total': 0,
                'mes_actual': 0,
                'graves': 0,
                'pendientes': 0,
                'total_heridos': 0,
                'total_fallecidos': 0
            }

    @staticmethod
    def buscar(criterios):
        """
        Busca accidentes según múltiples criterios

        Args:
            criterios: Diccionario con los criterios de búsqueda
                      Ej: {'texto': 'texto_busqueda', 'fecha_desde': '2025-01-01', ...}

        Returns:
            list: Lista de accidentes que coinciden
        """
        conditions = []
        params = []

        # Búsqueda por texto (número caso o lugar)
        if criterios.get('texto'):
            conditions.append("(a.numero_caso LIKE ? OR a.lugar LIKE ?)")
            texto = f"%{criterios['texto']}%"
            params.extend([texto, texto])

        # Filtro por rango de fechas
        if criterios.get('fecha_desde'):
            conditions.append("a.fecha >= ?")
            params.append(criterios['fecha_desde'])

        if criterios.get('fecha_hasta'):
            conditions.append("a.fecha <= ?")
            params.append(criterios['fecha_hasta'])

        # Filtro por tipo
        if criterios.get('id_tipo'):
            conditions.append("a.id_tipo = ?")
            params.append(criterios['id_tipo'])

        # Filtro por gravedad
        if criterios.get('id_gravedad'):
            conditions.append("a.id_gravedad = ?")
            params.append(criterios['id_gravedad'])

        # Filtro por estado
        if criterios.get('estado_caso'):
            conditions.append("a.estado_caso = ?")
            params.append(criterios['estado_caso'])

        # Filtro por comisaría
        if criterios.get('id_comisaria'):
            conditions.append("a.id_comisaria = ?")
            params.append(criterios['id_comisaria'])

        # Construir query
        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"""
            SELECT a.*, 
                   t.nombre_tipo as tipo_accidente,
                   g.nivel as gravedad,
                   c.nombre_comisaria
            FROM accidentes a
            LEFT JOIN tipos_accidente t ON a.id_tipo = t.id_tipo
            LEFT JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
            LEFT JOIN comisarias c ON a.id_comisaria = c.id_comisaria
            WHERE {where_clause}
            ORDER BY a.fecha DESC, a.hora DESC
        """

        try:
            resultados = db.execute_query(query, params)
            logger.info(f"Búsqueda realizada: {len(resultados)} resultados")
            return resultados
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}", exc_info=True)
            return []

    @staticmethod
    def obtener_recientes(limite=10):
        """
        Obtiene los accidentes más recientes

        Args:
            limite: Número máximo de registros

        Returns:
            list: Lista de accidentes recientes
        """
        query = """
            SELECT a.*, 
                   t.nombre_tipo as tipo_accidente,
                   g.nivel as gravedad,
                   c.nombre_comisaria
            FROM accidentes a
            LEFT JOIN tipos_accidente t ON a.id_tipo = t.id_tipo
            LEFT JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
            LEFT JOIN comisarias c ON a.id_comisaria = c.id_comisaria
            ORDER BY a.fecha DESC, a.hora DESC
            LIMIT ?
        """

        try:
            resultados = db.execute_query(query, (limite,))
            return resultados
        except Exception as e:
            logger.error(f"Error al obtener accidentes recientes: {e}", exc_info=True)
            return []


# Exportar la clase
__all__ = ['AccidenteService']