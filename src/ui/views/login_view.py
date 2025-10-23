from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from src.controllers.usuario_controller import UsuarioController
from src.ui.views.usuario_view import UsuarioRegisterView


class LoginView(QDialog):
    """Ventana de inicio de sesión del sistema SIATLITE"""

    def __init__(self, db_path: str, public_base_url: str = "http://127.0.0.1:8000"):
        super().__init__()
        self.db_path = db_path
        self.public_base_url = public_base_url
        self.controller = UsuarioController(db_path, public_base_url)
        self.setup_ui()

    # =====================================================
    # 🧱 INTERFAZ
    # =====================================================
    def setup_ui(self):
        self.setWindowTitle("Inicio de Sesión - SIATLITE")
        self.setFixedSize(380, 480)
        self.setStyleSheet("""
            QLabel { color: white; }
            QLineEdit {
                padding: 10px;
                border-radius: 6px;
                background-color: #333;
                color: white;
                border: 1px solid #555;
                font-size: 10pt;
                min-height: 38px;
            }
            QPushButton {
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
                min-height: 40px;
            }
            QPushButton#btnLogin {
                background-color: #2A82DA;
                color: white;
            }
            QPushButton#btnLogin:hover {
                background-color: #1E5FA8;
            }
            QPushButton#btnReset {
                background-color: #555;
                color: white;
            }
            QPushButton#btnReset:hover {
                background-color: #777;
            }
            QPushButton#btnCreate {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#btnCreate:hover {
                background-color: #3E8E41;
            }
            QDialog {
                background-color: #1E1E28;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 🪪 Logo y título
        title = QLabel("🚦 SIATLITE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26pt; font-weight: bold; color: #2A82DA;")

        subtitle = QLabel("Inicio de sesión del sistema")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 11pt; color: #AAAAAA;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        # 🧍 Campos de entrada
        self.inp_email = QLineEdit()
        self.inp_email.setPlaceholderText("Correo electrónico")

        self.inp_pass = QLineEdit()
        self.inp_pass.setPlaceholderText("Contraseña")
        self.inp_pass.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.inp_email)
        layout.addWidget(self.inp_pass)
        layout.addSpacing(10)

        # 🔘 Botones
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setObjectName("btnLogin")
        self.btn_login.clicked.connect(self.iniciar_sesion)

        self.btn_reset = QPushButton("¿Olvidaste tu contraseña?")
        self.btn_reset.setObjectName("btnReset")
        self.btn_reset.clicked.connect(self.recuperar_password)

        self.btn_create = QPushButton("🧾 Crear nueva cuenta")
        self.btn_create.setObjectName("btnCreate")
        self.btn_create.clicked.connect(self.crear_cuenta)

        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_reset)
        layout.addWidget(self.btn_create)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    # =====================================================
    # 🚀 LÓGICA DE LOGIN
    # =====================================================
    def iniciar_sesion(self):
        """Valida las credenciales e inicia sesión"""
        email = self.inp_email.text().strip()
        password = self.inp_pass.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Campos incompletos", "Por favor, ingresa tus credenciales.")
            return

        ok, result = self.controller.login(email, password)
        if not ok:
            QMessageBox.warning(self, "Error de inicio de sesión", result)
            return

        QMessageBox.information(self, "Bienvenido", f"Hola {result['nombre']} 👋")
        self.accept()  # ✅ Cierra el diálogo con código Aceptado

    def recuperar_password(self):
        """Envía enlace de recuperación por correo"""
        email = self.inp_email.text().strip()
        if not email:
            QMessageBox.warning(self, "Correo requerido", "Ingresa tu correo para enviar el enlace.")
            return

        ok, msg = self.controller.solicitar_reset(email)
        (QMessageBox.information if ok else QMessageBox.warning)(self, "Recuperación", msg)

    def crear_cuenta(self):
        """Abre la ventana de registro sin destruir ni cerrar el login"""
        # Deshabilitar temporalmente el login (en lugar de ocultarlo o cerrarlo)
        self.setEnabled(False)

        # Crear ventana de registro independiente
        registro = UsuarioRegisterView(self.db_path, self.public_base_url)
        registro.setWindowTitle("Registro de Usuario - SIATLITE")
        registro.setWindowModality(Qt.WindowModality.NonModal)
        registro.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # 🧩 Cerrar registro tras crear cuenta
        def on_registro_completado(ok, msg):
            if ok:
                QMessageBox.information(registro, "Registro exitoso", msg)
                registro.close()
            else:
                QMessageBox.warning(registro, "Error", msg)

        # Sobrescribir el método _registrar para usar el callback
        registro._registrar = lambda: self._registrar_usuario(registro, on_registro_completado)

        # 🪄 Cuando se cierre la ventana de registro, reactivar el login
        def reactivar_login():
            self.setEnabled(True)
            self.raise_()
            self.activateWindow()

        registro.destroyed.connect(reactivar_login)

        registro.show()
        registro.raise_()
        registro.activateWindow()

    def _registrar_usuario(self, vista_registro, callback):
        """Lógica de registro conectada desde LoginView"""
        n = vista_registro.inp_nombre.text().strip()
        a = vista_registro.inp_apellido.text().strip()
        e = vista_registro.inp_email.text().strip()
        p = vista_registro.inp_pass.text().strip()

        if not all([n, a, e, p]):
            callback(False, "Completa todos los campos.")
            return

        ok, msg = self.controller.registrar(n, a, e, p)
        callback(ok, msg)
