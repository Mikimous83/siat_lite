"""
Controlador para la gestión de accidentes
Conecta las vistas con los servicios
"""
from PyQt6.QtWidgets import QMessageBox
from src.services.accidente_service import AccidenteService
from src.models.accidente_model import Accidente
from src.utils.validators import Validators
from src.utils.logger import logger, OperacionContext
from src.utils.constants import MENSAJES


class AccidenteController:
    """Controlador para operaciones de accidentes"""

    def __init__(self, view=None):
        self.view = view
        self.service = AccidenteService
        self.usuario_actual = None

    def set_usuario(self, usuario):
        """Establece el usuario actual"""
        self.usuario_actual = usuario

    def cargar_accidentes(self):
        """Carga todos los accidentes en la vista"""
        try:
            with OperacionContext("Cargar accidentes", self.usuario_actual.get('username', 'Sistema')):
                accidentes = self.service.obtener_todos()

                if self.view:
                    self.view.mostrar_accidentes(accidentes)

                logger.info(f"Cargados {len(accidentes)} accidentes")
                return accidentes

        except Exception as e:
            logger.error(f"Error al cargar accidentes: {e}", exc_info=True)
            if self.view:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    f"Error al cargar accidentes: {str(e)}"
                )
            return []

    def cargar_accidente(self, id_accidente):
        """Carga un accidente específico"""
        try:
            accidente = self.service.obtener_por_id(id_accidente)

            if accidente:
                logger.info(f"Accidente cargado: {accidente['numero_caso']}")
                return Accidente.from_dict(dict(accidente))
            else:
                logger.warning(f"Accidente no encontrado: ID {id_accidente}")
                return None

        except Exception as e:
            logger.error(f"Error al cargar accidente {id_accidente}: {e}", exc_info=True)
            return None

    def crear_accidente(self, datos):
        """Crea un nuevo accidente"""
        try:
            with OperacionContext("Crear accidente", self.usuario_actual.get('username', 'Sistema')):
                # Crear objeto Accidente
                accidente = Accidente.from_dict(datos)

                # Validar datos
                errores = accidente.validar()
                if errores:
                    if self.view:
                        QMessageBox.warning(
                            self.view,
                            "Validación",
                            "Errores de validación:\n" + "\n".join(errores)
                        )
                    return None

                # Agregar usuario de registro
                datos['id_usuario_registro'] = self.usuario_actual.get('id_usuario', 1)

                # Crear en base de datos
                id_accidente = self.service.crear(datos)

                if id_accidente:
                    logger.log_operacion(
                        self.usuario_actual.get('username', 'Sistema'),
                        'CREAR',
                        'accidentes',
                        f"ID: {id_accidente}"
                    )

                    if self.view:
                        QMessageBox.information(
                            self.view,
                            "Éxito",
                            MENSAJES['exito_crear']
                        )

                    return id_accidente
                else:
                    raise Exception("No se pudo crear el accidente")

        except Exception as e:
            logger.error(f"Error al crear accidente: {e}", exc_info=True)
            if self.view:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    MENSAJES['error_crear'] + f"\n{str(e)}"
                )
            return None

    def actualizar_accidente(self, id_accidente, datos):
        """Actualiza un accidente existente"""
        try:
            with OperacionContext("Actualizar accidente", self.usuario_actual.get('username', 'Sistema')):
                # Crear objeto Accidente
                accidente = Accidente.from_dict(datos)

                # Validar datos
                errores = accidente.validar()
                if errores:
                    if self.view:
                        QMessageBox.warning(
                            self.view,
                            "Validación",
                            "Errores de validación:\n" + "\n".join(errores)
                        )
                    return False

                # Actualizar en base de datos
                rows = self.service.actualizar(id_accidente, datos)

                if rows > 0:
                    logger.log_operacion(
                        self.usuario_actual.get('username', 'Sistema'),
                        'ACTUALIZAR',
                        'accidentes',
                        f"ID: {id_accidente}"
                    )

                    if self.view:
                        QMessageBox.information(
                            self.view,
                            "Éxito",
                            MENSAJES['exito_actualizar']
                        )

                    return True
                else:
                    raise Exception("No se actualizó ningún registro")

        except Exception as e:
            logger.error(f"Error al actualizar accidente {id_accidente}: {e}", exc_info=True)
            if self.view:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    MENSAJES['error_actualizar'] + f"\n{str(e)}"
                )
            return False

    def eliminar_accidente(self, id_accidente):
        """Elimina un accidente"""
        try:
            # Confirmar eliminación
            if self.view:
                respuesta = QMessageBox.question(
                    self.view,
                    "Confirmar Eliminación",
                    MENSAJES['confirmar_eliminar'],
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if respuesta != QMessageBox.StandardButton.Yes:
                    return False

            with OperacionContext("Eliminar accidente", self.usuario_actual.get('username', 'Sistema')):
                rows = self.service.eliminar(id_accidente)

                if rows > 0:
                    logger.log_operacion(
                        self.usuario_actual.get('username', 'Sistema'),
                        'ELIMINAR',
                        'accidentes',
                        f"ID: {id_accidente}"
                    )

                    if self.view:
                        QMessageBox.information(
                            self.view,
                            "Éxito",
                            MENSAJES['exito_eliminar']
                        )

                    return True
                else:
                    raise Exception("No se eliminó ningún registro")

        except Exception as e:
            logger.error(f"Error al eliminar accidente {id_accidente}: {e}", exc_info=True)
            if self.view:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    MENSAJES['error_eliminar'] + f"\n{str(e)}"
                )
            return False

    def buscar_accidentes(self, criterios):
        """Busca accidentes según criterios"""
        try:
            # TODO: Implementar búsqueda avanzada en el servicio
            logger.info(f"Búsqueda de accidentes con criterios: {criterios}")

            # Por ahora, retornar todos y filtrar en memoria
            accidentes = self.service.obtener_todos()

            # Aplicar filtros básicos
            if criterios.get('busqueda'):
                texto = criterios['busqueda'].lower()
                accidentes = [
                    a for a in accidentes
                    if texto in str(a['numero_caso']).lower() or
                       texto in str(a['lugar']).lower()
                ]

            return accidentes

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}", exc_info=True)
            return []

    def obtener_estadisticas(self):
        """Obtiene estadísticas de accidentes"""
        try:
            stats = self.service.obtener_estadisticas()
            logger.info("Estadísticas obtenidas")
            return stats
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {e}", exc_info=True)
            return {}

    def exportar_accidentes(self, formato='CSV'):
        """Exporta accidentes a un archivo"""
        try:
            with OperacionContext("Exportar accidentes", self.usuario_actual.get('username', 'Sistema')):
                accidentes = self.service.obtener_todos()

                # TODO: Implementar exportación real
                logger.info(f"Exportando {len(accidentes)} accidentes a {formato}")

                if self.view:
                    QMessageBox.information(
                        self.view,
                        "Exportación",
                        f"Funcionalidad de exportación a {formato} en desarrollo"
                    )

                return True

        except Exception as e:
            logger.error(f"Error al exportar: {e}", exc_info=True)
            return False


class PersonaController:
    """Controlador para gestión de personas"""

    def __init__(self, view=None):
        self.view = view
        from services.persona_vehiculo_services import PersonaService
        self.service = PersonaService
        self.usuario_actual = None

    def set_usuario(self, usuario):
        self.usuario_actual = usuario

    def cargar_personas(self, id_accidente=None):
        """Carga personas (todas o de un accidente específico)"""
        try:
            if id_accidente:
                personas = self.service.obtener_por_accidente(id_accidente)
            else:
                personas = self.service.obtener_todas()

            if self.view:
                self.view.mostrar_personas(personas)

            return personas
        except Exception as e:
            logger.error(f"Error al cargar personas: {e}", exc_info=True)
            return []

    def crear_persona(self, datos):
        """Crea una nueva persona"""
        try:
            # Validar DNI
            if datos.get('dni'):
                valido, mensaje = Validators.validar_dni(datos['dni'])
                if not valido:
                    if self.view:
                        QMessageBox.warning(self.view, "Validación", mensaje)
                    return None

            id_persona = self.service.crear(datos)

            if id_persona:
                logger.log_operacion(
                    self.usuario_actual.get('username', 'Sistema'),
                    'CREAR',
                    'personas',
                    f"ID: {id_persona}"
                )

                if self.view:
                    QMessageBox.information(self.view, "Éxito", MENSAJES['exito_crear'])

                return id_persona

        except Exception as e:
            logger.error(f"Error al crear persona: {e}", exc_info=True)
            if self.view:
                QMessageBox.critical(self.view, "Error", str(e))
            return None


class VehiculoController:
    """Controlador para gestión de vehículos"""

    def __init__(self, view=None):
        self.view = view
        from services.persona_vehiculo_services import VehiculoService
        self.service = VehiculoService
        self.usuario_actual = None

    def set_usuario(self, usuario):
        self.usuario_actual = usuario

    def cargar_vehiculos(self, id_accidente=None):
        """Carga vehículos (todos o de un accidente específico)"""
        try:
            if id_accidente:
                vehiculos = self.service.obtener_por_accidente(id_accidente)
            else:
                vehiculos = self.service.obtener_todos()

            if self.view:
                self.view.mostrar_vehiculos(vehiculos)

            return vehiculos
        except Exception as e:
            logger.error(f"Error al cargar vehículos: {e}", exc_info=True)
            return []

    def crear_vehiculo(self, datos):
        """Crea un nuevo vehículo"""
        try:
            # Validar placa
            if datos.get('placa'):
                valido, mensaje = Validators.validar_placa(datos['placa'])
                if not valido:
                    if self.view:
                        QMessageBox.warning(self.view, "Validación", mensaje)
                    return None

            id_vehiculo = self.service.crear(datos)

            if id_vehiculo:
                logger.log_operacion(
                    self.usuario_actual.get('username', 'Sistema'),
                    'CREAR',
                    'vehiculos',
                    f"ID: {id_vehiculo}, Placa: {datos.get('placa')}"
                )

                if self.view:
                    QMessageBox.information(self.view, "Éxito", MENSAJES['exito_crear'])

                return id_vehiculo

        except Exception as e:
            logger.error(f"Error al crear vehículo: {e}", exc_info=True)
            if self.view:
                QMessageBox.critical(self.view, "Error", str(e))
            return None

    def buscar_por_placa(self, placa):
        """Busca vehículos por placa"""
        try:
            vehiculos = self.service.buscar_por_placa(placa)
            logger.info(f"Búsqueda por placa '{placa}': {len(vehiculos)} resultados")
            return vehiculos
        except Exception as e:
            logger.error(f"Error en búsqueda por placa: {e}", exc_info=True)
            return []

    def obtener_historial(self, placa):
        """Obtiene historial de accidentes de una placa"""
        try:
            historial = self.service.obtener_historial_placa(placa)
            logger.info(f"Historial de placa '{placa}': {len(historial)} accidentes")
            return historial
        except Exception as e:
            logger.error(f"Error al obtener historial: {e}", exc_info=True)
            return []


class ReporteController:
    """Controlador para generación de reportes"""

    def __init__(self, view=None):
        self.view = view
        from services.reporte_service import ReporteService
        self.service = ReporteService
        self.usuario_actual = None

    def set_usuario(self, usuario):
        self.usuario_actual = usuario

    def generar_reporte(self, tipo_reporte, parametros=None):
        """Genera un reporte según el tipo especificado"""
        try:
            with OperacionContext(f"Generar reporte {tipo_reporte}",
                                  self.usuario_actual.get('username', 'Sistema')):

                if tipo_reporte == 'periodo':
                    datos = self.service.reporte_por_periodo(
                        parametros['fecha_inicio'],
                        parametros['fecha_fin']
                    )

                elif tipo_reporte == 'tipo':
                    datos = self.service.reporte_por_tipo()

                elif tipo_reporte == 'gravedad':
                    datos = self.service.reporte_por_gravedad()

                elif tipo_reporte == 'puntos_criticos':
                    datos = self.service.puntos_criticos()

                elif tipo_reporte == 'conductores':
                    datos = self.service.conductores_recurrentes()

                elif tipo_reporte == 'completo':
                    datos = self.service.reporte_completo()

                else:
                    raise ValueError(f"Tipo de reporte no válido: {tipo_reporte}")

                logger.info(f"Reporte '{tipo_reporte}' generado exitosamente")
                return datos

        except Exception as e:
            logger.error(f"Error al generar reporte: {e}", exc_info=True)
            if self.view:
                QMessageBox.critical(self.view, "Error", f"Error al generar reporte: {str(e)}")
            return None