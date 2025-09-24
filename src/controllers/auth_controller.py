from src.controllers.usuario_controller import UsuarioController
from src.views.login_view import LoginView
from src.views.main_window import MainWindow

class AuthController:
    def __init__(self):
        self.usuario_controller = UsuarioController()
        self.login_view = None
        self.main_window = None

    def iniciar_autenticacion(self):
        """Iniciar proceso de autenticación"""
        self.login_view = LoginView(self)
        self.login_view.show()

    def autenticar_usuario(self, email, password):
        """Autenticar usuario y mostrar ventana principal"""
        if self.usuario_controller.autenticar_usuario(email, password):
            # Cerrar login y abrir ventana principal
            self.mostrar_ventana_principal()
            return True
        return False

    def mostrar_ventana_principal(self):
        """Mostrar ventana principal después de autenticación exitosa"""
        from src.controllers.main_controller import MainController
        main_controller = MainController()
        main_controller.usuario_actual = self.usuario_controller.usuario_actual
        main_controller.mostrar_ventana_principal()

    def cerrar_session(self):
        """Cerrar sesión y volver al login"""
        self.usuario_controller.usuario_actual = None
        if self.main_window:
            self.main_window.root.destroy()
        self.iniciar_autenticacion()
