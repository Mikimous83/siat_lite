from src.models.accidente_model import AccidenteModel
from src.views.accidente_form_view import AccidenteFormView
from src.services.validation_service import ValidationService
from src.models.database_connection import DatabaseConnection

class AccidenteController:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        db = DatabaseConnection()
        self.accidente_model = AccidenteModel(db)
        self.validation_service = ValidationService()
        self.current_view = None

    def mostrar_formulario_registro(self):
        """Mostrar formulario de registro de accidente"""
        self.current_view = AccidenteFormView(self.parent_window, self)

    def guardar_accidente(self, datos_formulario):
        """Procesar guardado de accidente"""
        try:
            # 1. Validar datos
            errores = self.validation_service.validar_accidente(datos_formulario)
            if errores:
                self._mostrar_errores(errores)
                return False

            # 2. Procesar y guardar
            datos_procesados = self._procesar_datos(datos_formulario)
            id_accidente = self.accidente_model.crear_accidente(datos_procesados)

            # 3. Confirmar éxito
            self._mostrar_exito(f"Accidente registrado con ID: {id_accidente}")
            self.current_view.window.destroy()

            return True

        except Exception as e:
            self._mostrar_error(f"Error al guardar: {str(e)}")
            return False

    def _procesar_datos(self, datos):
        """Procesar datos antes de guardar"""
        # Agregar datos adicionales como usuario actual, timestamp, etc.
        datos['id_usuario'] = 1  # Usuario actual
        datos['heridos'] = 0  # Por defecto
        datos['fallecidos'] = 0  # Por defecto
        datos['vehiculos_involucrados'] = 1  # Por defecto
        return datos

    def _mostrar_errores(self, errores):
        """Mostrar errores de validación"""
        from ttkbootstrap.dialogs import Messagebox
        mensaje = "\\n".join(errores)
        Messagebox.show_error("Errores de Validación", mensaje)

    def _mostrar_exito(self, mensaje):
        """Mostrar mensaje de éxito"""
        from ttkbootstrap.dialogs import Messagebox
        Messagebox.show_info("Éxito", mensaje)

    def _mostrar_error(self, mensaje):
        """Mostrar mensaje de error"""
        from ttkbootstrap.dialogs import Messagebox
        Messagebox.show_error("Error", mensaje)