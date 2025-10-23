"""
Servicio de generación de reportes y estadísticas
"""
from src.models.database_connection import DatabaseConnection as db
from datetime import datetime, timedelta


class ReporteService:
    """Servicio para generación de reportes"""

    @staticmethod
    def reporte_por_periodo(fecha_inicio, fecha_fin):
        """Genera reporte de accidentes por periodo"""
        query = """
            SELECT a.*,
                   t.nombre_tipo as tipo_accidente,
                   g.nivel as gravedad,
                   c.nombre_comisaria,
                   tv.nombre_tipo as tipo_via
            FROM accidentes a
            LEFT JOIN tipos_accidente t ON a.id_tipo = t.id_tipo
            LEFT JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
            LEFT JOIN comisarias c ON a.id_comisaria = c.id_comisaria
            LEFT JOIN tipos_via tv ON a.id_tipo_via = tv.id_tipo_via
            WHERE a.fecha BETWEEN ? AND ?
            ORDER BY a.fecha DESC, a.hora DESC
        """
        return db.execute_query(query, (fecha_inicio, fecha_fin))

    @staticmethod
    def reporte_por_tipo():
        """Genera reporte de accidentes por tipo"""
        query = """
            SELECT 
                t.nombre_tipo,
                COUNT(a.id_accidente) as total_accidentes,
                SUM(a.heridos) as total_heridos,
                SUM(a.fallecidos) as total_fallecidos,
                ROUND(AVG(a.heridos), 2) as promedio_heridos,
                ROUND(AVG(a.fallecidos), 2) as promedio_fallecidos
            FROM tipos_accidente t
            LEFT JOIN accidentes a ON t.id_tipo = a.id_tipo
            GROUP BY t.id_tipo, t.nombre_tipo
            ORDER BY total_accidentes DESC
        """
        return db.execute_query(query)

    @staticmethod
    def reporte_por_gravedad():
        """Genera reporte de accidentes por gravedad"""
        query = """
            SELECT 
                g.nivel,
                COUNT(a.id_accidente) as total_accidentes,
                SUM(a.heridos) as total_heridos,
                SUM(a.fallecidos) as total_fallecidos,
                ROUND(COUNT(a.id_accidente) * 100.0 / (SELECT COUNT(*) FROM accidentes), 2) as porcentaje
            FROM niveles_gravedad g
            LEFT JOIN accidentes a ON g.id_gravedad = a.id_gravedad
            GROUP BY g.id_gravedad, g.nivel
            ORDER BY 
                CASE g.nivel
                    WHEN 'Grave' THEN 1
                    WHEN 'Moderado' THEN 2
                    WHEN 'Leve' THEN 3
                END
        """
        return db.execute_query(query)

    @staticmethod
    def puntos_criticos():
        """Identifica puntos críticos de accidentes"""
        query = """
            SELECT 
                lugar,
                COUNT(*) as total_accidentes,
                SUM(heridos) as total_heridos,
                SUM(fallecidos) as total_fallecidos,
                MAX(fecha) as ultimo_accidente
            FROM accidentes
            GROUP BY lugar
            HAVING COUNT(*) >= 2
            ORDER BY total_accidentes DESC, total_fallecidos DESC
            LIMIT 20
        """
        return db.execute_query(query)

    @staticmethod
    def reporte_por_ubicacion():
        """Genera reporte por ubicación (departamento, provincia, distrito)"""
        query = """
            SELECT 
                u.departamento,
                u.provincia,
                u.distrito,
                COUNT(a.id_accidente) as total_accidentes,
                SUM(a.heridos) as total_heridos,
                SUM(a.fallecidos) as total_fallecidos
            FROM ubicaciones u
            JOIN comisarias c ON u.id_ubicacion = c.id_ubicacion
            JOIN accidentes a ON c.id_comisaria = a.id_comisaria
            GROUP BY u.departamento, u.provincia, u.distrito
            ORDER BY total_accidentes DESC
        """
        return db.execute_query(query)

    @staticmethod
    def conductores_recurrentes():
        """Identifica conductores con múltiples accidentes"""
        query = """
            SELECT 
                v.conductor_dni,
                v.conductor_nombre || ' ' || v.conductor_apellido as nombre_completo,
                v.conductor_licencia,
                COUNT(DISTINCT v.id_accidente) as total_accidentes,
                GROUP_CONCAT(DISTINCT a.numero_caso) as casos
            FROM vehiculos v
            JOIN accidentes a ON v.id_accidente = a.id_accidente
            WHERE v.conductor_dni IS NOT NULL AND v.conductor_dni != ''
            GROUP BY v.conductor_dni, v.conductor_nombre, v.conductor_apellido, v.conductor_licencia
            HAVING COUNT(DISTINCT v.id_accidente) > 1
            ORDER BY total_accidentes DESC
        """
        return db.execute_query(query)

    @staticmethod
    def reporte_por_condiciones():
        """Genera reporte por condiciones climáticas e iluminación"""
        query = """
            SELECT 
                condiciones_climaticas,
                iluminacion,
                COUNT(*) as total_accidentes,
                SUM(heridos) as total_heridos,
                SUM(fallecidos) as total_fallecidos
            FROM accidentes
            WHERE condiciones_climaticas IS NOT NULL
            GROUP BY condiciones_climaticas, iluminacion
            ORDER BY total_accidentes DESC
        """
        return db.execute_query(query)

    @staticmethod
    def tendencias_temporales():
        """Analiza tendencias temporales de accidentes"""
        # Por mes
        query_mes = """
            SELECT 
                strftime('%Y-%m', fecha) as mes,
                COUNT(*) as total_accidentes,
                SUM(heridos) as total_heridos,
                SUM(fallecidos) as total_fallecidos
            FROM accidentes
            WHERE fecha >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', fecha)
            ORDER BY mes
        """

        # Por día de la semana
        query_dia = """
            SELECT 
                CASE CAST(strftime('%w', fecha) AS INTEGER)
                    WHEN 0 THEN 'Domingo'
                    WHEN 1 THEN 'Lunes'
                    WHEN 2 THEN 'Martes'
                    WHEN 3 THEN 'Miércoles'
                    WHEN 4 THEN 'Jueves'
                    WHEN 5 THEN 'Viernes'
                    WHEN 6 THEN 'Sábado'
                END as dia_semana,
                COUNT(*) as total_accidentes
            FROM accidentes
            GROUP BY strftime('%w', fecha)
            ORDER BY CAST(strftime('%w', fecha) AS INTEGER)
        """

        # Por hora del día
        query_hora = """
            SELECT 
                CASE 
                    WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 0 AND 5 THEN '00:00-05:59'
                    WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 6 AND 11 THEN '06:00-11:59'
                    WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 12 AND 17 THEN '12:00-17:59'
                    ELSE '18:00-23:59'
                END as rango_hora,
                COUNT(*) as total_accidentes
            FROM accidentes
            GROUP BY rango_hora
            ORDER BY rango_hora
        """

        return {
            'por_mes': db.execute_query(query_mes),
            'por_dia': db.execute_query(query_dia),
            'por_hora': db.execute_query(query_hora)
        }

    @staticmethod
    def reporte_vehiculos():
        """Genera reporte de vehículos involucrados"""
        query = """
            SELECT 
                tipo_vehiculo,
                marca,
                COUNT(*) as total_involucrados,
                COUNT(DISTINCT id_accidente) as accidentes_distintos,
                SUM(CASE WHEN estado_vehiculo LIKE '%Grave%' THEN 1 ELSE 0 END) as daños_graves,
                SUM(CASE WHEN estado_vehiculo LIKE '%Total%' THEN 1 ELSE 0 END) as perdidas_totales
            FROM vehiculos
            GROUP BY tipo_vehiculo, marca
            ORDER BY total_involucrados DESC
        """
        return db.execute_query(query)

    @staticmethod
    def estadisticas_generales():
        """Obtiene estadísticas generales del sistema"""
        stats = {}

        # Total de accidentes
        query = "SELECT COUNT(*) as total FROM accidentes"
        result = db.execute_query(query)
        stats['total_accidentes'] = result[0]['total'] if result else 0

        # Total de personas involucradas
        query = "SELECT COUNT(*) as total FROM personas"
        result = db.execute_query(query)
        stats['total_personas'] = result[0]['total'] if result else 0

        # Total de vehículos
        query = "SELECT COUNT(*) as total FROM vehiculos"
        result = db.execute_query(query)
        stats['total_vehiculos'] = result[0]['total'] if result else 0

        # Total de heridos y fallecidos
        query = "SELECT SUM(heridos) as heridos, SUM(fallecidos) as fallecidos FROM accidentes"
        result = db.execute_query(query)
        if result and result[0]['heridos']:
            stats['total_heridos'] = result[0]['heridos']
            stats['total_fallecidos'] = result[0]['fallecidos']
        else:
            stats['total_heridos'] = 0
            stats['total_fallecidos'] = 0

        # Promedio de vehículos por accidente
        query = "SELECT AVG(vehiculos_involucrados) as promedio FROM accidentes"
        result = db.execute_query(query)
        stats['promedio_vehiculos'] = round(result[0]['promedio'], 2) if result and result[0]['promedio'] else 0

        # Casos abiertos vs cerrados
        query = """
            SELECT 
                SUM(CASE WHEN estado_caso = 'Abierto' THEN 1 ELSE 0 END) as abiertos,
                SUM(CASE WHEN estado_caso = 'En Proceso' THEN 1 ELSE 0 END) as en_proceso,
                SUM(CASE WHEN estado_caso = 'Cerrado' THEN 1 ELSE 0 END) as cerrados
            FROM accidentes
        """
        result = db.execute_query(query)
        if result:
            stats['casos_abiertos'] = result[0]['abiertos'] or 0
            stats['casos_en_proceso'] = result[0]['en_proceso'] or 0
            stats['casos_cerrados'] = result[0]['cerrados'] or 0

        # Comparativa con mes anterior
        query = """
            SELECT 
                SUM(CASE WHEN strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now') THEN 1 ELSE 0 END) as mes_actual,
                SUM(CASE WHEN strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now', '-1 month') THEN 1 ELSE 0 END) as mes_anterior
            FROM accidentes
        """
        result = db.execute_query(query)
        if result:
            mes_actual = result[0]['mes_actual'] or 0
            mes_anterior = result[0]['mes_anterior'] or 0
            stats['mes_actual'] = mes_actual
            stats['mes_anterior'] = mes_anterior

            if mes_anterior > 0:
                variacion = ((mes_actual - mes_anterior) / mes_anterior) * 100
                stats['variacion_mensual'] = round(variacion, 2)
            else:
                stats['variacion_mensual'] = 0

        return stats

    @staticmethod
    def reporte_completo():
        """Genera un reporte ejecutivo completo"""
        return {
            'estadisticas_generales': ReporteService.estadisticas_generales(),
            'por_tipo': ReporteService.reporte_por_tipo(),
            'por_gravedad': ReporteService.reporte_por_gravedad(),
            'puntos_criticos': ReporteService.puntos_criticos(),
            'tendencias': ReporteService.tendencias_temporales(),
            'conductores_recurrentes': ReporteService.conductores_recurrentes(),
            'por_condiciones': ReporteService.reporte_por_condiciones()
        }