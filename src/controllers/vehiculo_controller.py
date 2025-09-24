from models.vehiculo_model import VehiculoModel
from services.validation_service import ValidationService


class VehiculoController:
    def __init__(self):
        self.vehiculo_model = VehiculoModel()
        self.validation_service = ValidationService()

    def registrar_vehiculo(self, datos_vehiculo):
        """Registrar nuevo vehículo"""
        try:
            # Validar datos
            errores = self.validation_service.validar_vehiculo(datos_vehiculo)
            if errores:
                return {'success': False, 'errores': errores}

            # Registrar vehículo
            id_vehiculo = self.vehiculo_model.crear_vehiculo(datos_vehiculo)

            return {
                'success': True,
                'id_vehiculo': id_vehiculo,
                'mensaje': f'Vehículo registrado con ID: {id_vehiculo}'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'mensaje': 'Error al registrar vehículo'
            }

    def obtener_vehiculos_accidente(self, id_accidente):
        """Obtener vehículos de un accidente"""
        try:
            return self.vehiculo_model.obtener_vehiculos_por_accidente(id_accidente)
        except Exception as e:
            print(f"Error al obtener vehículos: {str(e)}")
            return []

    def buscar_por_placa(self, placa):
        """Buscar vehículo por placa"""
        try:
            return self.vehiculo_model.buscar_por_placa(placa.upper())
        except Exception as e:
            print(f"Error en búsqueda por placa: {str(e)}")
            return None

    def actualizar_vehiculo(self, id_vehiculo, datos):
        """Actualizar datos de vehículo"""
        try:
            errores = self.validation_service.validar_vehiculo(datos)
            if errores:
                return {'success': False, 'errores': errores}

            success = self.vehiculo_model.actualizar_vehiculo(id_vehiculo, datos)

            return {
                'success': success,
                'mensaje': 'Vehículo actualizado correctamente' if success else 'Error al actualizar'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'mensaje': 'Error al actualizar vehículo'
            }