from src.models.usuario_model import UsuarioModel
from src.views.main_window import MainWindow
from src.controllers.accidente_controller import AccidenteController
from src.controllers.consulta_controller import ConsultaController
from src.controllers.reporte_controller import ReporteController
class MainController:
    def __init__(self):
        self.usuario_actual = None
        self.usuario_model = UsuarioModel()
        self.main_window = None

    def iniciar_aplicacion(self):
        """Punto de entrada principal"""
        if self.autenticar_usuario():
            self.mostrar_ventana_principal()
        else:
            print("Autenticación fallida")

    def autenticar_usuario(self):
        """Proceso de autenticación"""
        # Aquí iría el login, por ahora simulamos
        self.usuario_actual = {
            'id': 1,
            'nombre': 'Admin',
            'nivel_acceso': 'administrador'
        }
        return True

    def mostrar_ventana_principal(self):
        """Mostrar ventana principal"""
        self.main_window = MainWindow(self)
        self.main_window.run()

    def abrir_registro_accidente(self):
        """Abrir formulario de registro"""
        accidente_controller = AccidenteController(self.main_window.root)
        accidente_controller.mostrar_formulario_registro()

    def abrir_consulta(self):
        """Abrir módulo de consulta"""
        consulta_controller = ConsultaController(self.main_window.root)
        consulta_controller.mostrar_ventana_consulta()

    def abrir_reportes(self):
        """Abrir módulo de reportes"""
        reporte_controller = ReporteController(self.main_window.root)
        reporte_controller.mostrar_ventana_reportes()