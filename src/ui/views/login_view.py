from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QSpacerItem, QSizePolicy, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from src.controllers.usuario_controller import UsuarioController
from src.ui.views.usuario_view import UsuarioRegisterView


from PyQt6.QtCore import QThread, pyqtSignal, QTimer

class LoginWorker(QThread):
    login_resultado = pyqtSignal(bool, object)  # object permite dict o str

    def __init__(self, controller, email, password):
        super().__init__()
        self.controller = controller
        self.email = email
        self.password = password

    def run(self):
        try:
            print("🧩 [HILO] Verificando credenciales en segundo plano...")
            ok, result = self.controller.login(self.email, self.password)
            self.login_resultado.emit(ok, result)
        except Exception as e:
            print("❌ [HILO] Error en LoginWorker:", e)
            self.login_resultado.emit(False, f"Error interno: {e}")


class LoginView(QDialog):
    """Ventana de inicio de sesión del sistema SIATLITE - Diseño Premium"""

    def __init__(self, db_path: str, public_base_url: str = "http://127.0.0.1:8000"):
        super().__init__()
        self.db_path = db_path
        self.public_base_url = public_base_url
        self.controller = UsuarioController(db_path, public_base_url)
        self.login_thread = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("SIATLITE - Sistema Inteligente de Tráfico")
        self.setFixedSize(420, 560)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)

        # ✨ Diseño Premium con Gradiente Azul-Cyan
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0F2027, stop:0.5 #203A43, stop:1 #2C5364);
                border-radius: 20px;
            }

            QLabel {
                color: white;
            }

            QLineEdit {
                padding: 12px 18px;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 2px solid rgba(42, 130, 218, 0.3);
                font-size: 11pt;
                min-height: 45px;
                font-weight: 500;
            }

            QLineEdit:focus {
                border: 2px solid #2A82DA;
                background-color: rgba(42, 130, 218, 0.15);
            }

            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }

            QPushButton {
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
                min-height: 36px;
                max-height: 36px;
                border: none;
                letter-spacing: 0.5px;
                transition: 0.3s;
            }

            QPushButton#btnLogin {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2A82DA, stop:1 #1E5FA8);
                color: white;
            }

            QPushButton#btnLogin:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3A92EA, stop:1 #2E7FB8);
            }

            QPushButton#btnLogin:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1A7CCA, stop:1 #0E4FA8);
            }

            QPushButton#btnReset {
                background-color: rgba(255, 255, 255, 0.1);
                color: #2A82DA;
                border: 2px solid rgba(42, 130, 218, 0.3);
            }

            QPushButton#btnReset:hover {
                background-color: rgba(42, 130, 218, 0.2);
                border: 2px solid #2A82DA;
            }

            QPushButton#btnCreate {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #388E3C);
                color: white;
            }

            QPushButton#btnCreate:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5CBF60, stop:1 #4A9D4C);
            }

            QProgressBar {
                border: none;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.1);
                text-align: center;
                color: white;
            }

            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2A82DA, stop:1 #1E5FA8);
                border-radius: 5px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(40, 35, 40, 35)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 🎨 Logo y Títulos con estilos mejorados
        title = QLabel("🚦 SIATLITE")
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2A82DA; text-shadow: 0px 2px 10px rgba(0,0,0,0.3);")

        subtitle = QLabel("Sistema de Tráfico Inteligente")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7);")

        benefit = QLabel("✓ Acceso seguro y rápido")
        benefit_font = QFont("Segoe UI", 9)
        benefit.setFont(benefit_font)
        benefit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        benefit.setStyleSheet("color: rgba(76, 175, 80, 0.9);")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(benefit)
        main_layout.addSpacing(15)

        # 🔐 Campos de entrada con iconos conceptuales
        label_email = QLabel("📧 Correo Electrónico")
        label_email.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 10pt; font-weight: 500;")
        self.inp_email = QLineEdit()
        self.inp_email.setPlaceholderText("tu@correo.com")

        label_pass = QLabel("🔐 Contraseña")
        label_pass.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 10pt; font-weight: 500;")
        self.inp_pass = QLineEdit()
        self.inp_pass.setPlaceholderText("Tu contraseña segura")
        self.inp_pass.setEchoMode(QLineEdit.EchoMode.Password)

        main_layout.addWidget(label_email)
        main_layout.addWidget(self.inp_email)
        main_layout.addWidget(label_pass)
        main_layout.addWidget(self.inp_pass)
        main_layout.addSpacing(15)

        # 📊 Barra de progreso (oculta inicialmente)
        self.progress = QProgressBar()
        self.progress.setMaximum(0)
        self.progress.setVisible(False)
        self.progress.setMinimumHeight(4)
        self.progress.setMaximumHeight(4)
        main_layout.addWidget(self.progress)

        # 🔘 Botones principales en fila única
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.btn_login = QPushButton("▶ INICIAR SESIÓN")
        self.btn_login.setObjectName("btnLogin")
        self.btn_login.clicked.connect(self.iniciar_sesion)
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_create = QPushButton("✨ CREAR CUENTA")
        self.btn_create.setObjectName("btnCreate")
        self.btn_create.clicked.connect(self.crear_cuenta)
        self.btn_create.setCursor(Qt.CursorShape.PointingHandCursor)

        buttons_layout.addWidget(self.btn_login)
        buttons_layout.addWidget(self.btn_create)
        main_layout.addLayout(buttons_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # 🛡️ Información de seguridad
        security_info = QLabel("🔒 Datos protegidos con encriptación empresarial")
        security_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        security_info.setStyleSheet("color: rgba(76, 175, 80, 0.7); font-size: 8pt; font-style: italic;")

        # 🔐 Link de recuperar contraseña al pie
        self.link_reset = QLabel(
            "❓ <a href='reset' style='color: #2A82DA; text-decoration: none;'>¿Olvidaste tu contraseña?</a>")
        self.link_reset.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.link_reset.setStyleSheet("font-size: 9pt;")
        self.link_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.link_reset.setOpenExternalLinks(False)
        self.link_reset.linkActivated.connect(self.recuperar_password)

        main_layout.addWidget(security_info)
        main_layout.addWidget(self.link_reset)

    def iniciar_sesion(self):
        """Inicia sesión en hilo seguro y muestra progreso"""
        email = self.inp_email.text().strip()
        password = self.inp_pass.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Campos incompletos", "Por favor, ingresa tu correo y contraseña.")
            return

        print("🚀 Iniciando sesión con:", email)
        self.progress.setVisible(True)
        self.btn_login.setEnabled(False)
        self.btn_create.setEnabled(False)
        self.inp_email.setEnabled(False)
        self.inp_pass.setEnabled(False)

        # Crear hilo y conectar señal
        self.login_thread = LoginWorker(self.controller, email, password)
        self.login_thread.login_resultado.connect(self.on_login_completado)
        self.login_thread.start()

    def on_login_completado(self, ok, result):
        """Callback cuando se completa el login"""
        self.progress.setVisible(False)
        self.btn_login.setEnabled(True)
        self.inp_email.setEnabled(True)
        self.inp_pass.setEnabled(True)

        if not ok:
            QMessageBox.critical(self, "❌ Error de Autenticación", str(result))
            return

        # ✅ Guardar el usuario autenticado para usarlo en MainWindow
        self.usuario_autenticado = result

        QMessageBox.information(
            self,
            "✅ Bienvenido",
            f"¡Hola {result.get('nombre', 'Usuario')} 👋!\n\nAcceso concedido al sistema."
        )

        self.accept()

    def recuperar_password(self, link=None):
        """Envía enlace de recuperación por correo"""
        email = self.inp_email.text().strip()
        if not email:
            QMessageBox.warning(self, "⚠️ Correo requerido",
                                "Ingresa tu correo para enviar el enlace de recuperación.")
            return

        self.btn_login.setEnabled(False)
        ok, msg = self.controller.solicitar_reset(email)
        self.btn_login.setEnabled(True)

        if ok:
            QMessageBox.information(self, "✅ Correo Enviado", msg)
        else:
            QMessageBox.warning(self, "❌ Error", msg)

    def crear_cuenta(self):
        """Abre ventana de registro como ventana independiente"""
        from PyQt6.QtCore import QTimer

        registro = UsuarioRegisterView(self.db_path, self.public_base_url)
        registro.setWindowTitle("Registro de Usuario - SIATLITE")

        registro.setParent(None)
        registro.setWindowModality(Qt.WindowModality.NonModal)
        registro.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        registro.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.CustomizeWindowHint
        )

        def reactivar_login():
            self.raise_()
            self.activateWindow()

        registro.destroyed.connect(reactivar_login)

        def on_registro_completado(ok, msg):
            if ok:
                QMessageBox.information(registro, "✅ Registro Exitoso", msg)
                registro.close()
            else:
                QMessageBox.warning(registro, "❌ Error de Registro", msg)

        registro._registrar = lambda: self._registrar_usuario(registro, on_registro_completado)
        registro.show()

        QTimer.singleShot(100, lambda: (
            registro.raise_(),
            registro.activateWindow(),
            registro.setFocus()
        ))

    def _registrar_usuario(self, vista_registro, callback):
        """Lógica de registro conectada desde LoginView"""
        n = vista_registro.inp_nombre.text().strip()
        a = vista_registro.inp_apellido.text().strip()
        e = vista_registro.inp_email.text().strip()
        p = vista_registro.inp_pass.text().strip()

        if not all([n, a, e, p]):
            callback(False, "⚠️ Completa todos los campos.")
            return

        ok, msg = self.controller.registrar(n, a, e, p)
        callback(ok, msg)