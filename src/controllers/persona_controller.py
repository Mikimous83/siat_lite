from src.models.persona_model import PersonaModel
from src.services.validation_service import ValidationService
from ttkbootstrap.dialogs import Messagebox


class PersonaController:
    def __init__(self):
        self.persona_model = PersonaModel()
        self.validation_service = ValidationService()

    def registrar_persona(self, datos_persona):
        """Registrar nueva persona en accidente"""
        try:
            # Validar datos
            errores = self.validation_service.validar_persona(datos_persona)
            if errores:
                return {'success': False, 'errores': errores}

            # Registrar persona
            id_persona = self.persona_model.crear_persona(datos_persona)

            return {
                'success': True,
                'id_persona': id_persona,
                'mensaje': f'Persona registrada con ID: {id_persona}'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'mensaje': 'Error al registrar persona'
            }

    def obtener_personas_accidente(self, id_accidente):
        """Obtener personas de un accidente"""
        try:
            return self.persona_model.obtener_personas_por_accidente(id_accidente)
        except Exception as e:
            print(f"Error al obtener personas: {str(e)}")
            return []

    def buscar_por_dni(self, dni):
        """Buscar persona por DNI"""
        try:
            return self.persona_model.buscar_por_dni(dni)
        except Exception as e:
            print(f"Error en búsqueda por DNI: {str(e)}")
            return []

    def obtener_heridos_fallecidos(self, id_accidente):
        """Obtener solo heridos y fallecidos de un accidente"""
        try:
            heridos = self.persona_model.obtener_personas_por_tipo(id_accidente, 'herido')
            fallecidos = self.persona_model.obtener_personas_por_tipo(id_accidente, 'fallecido')
            return {'heridos': heridos, 'fallecidos': fallecidos}
        except Exception as e:
            print(f"Error al obtener heridos/fallecidos: {str(e)}")
            return {'heridos': [], 'fallecidos': []}