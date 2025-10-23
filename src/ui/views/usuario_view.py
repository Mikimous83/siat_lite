from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from src.controllers.usuario_controller import UsuarioController


class UsuarioRegisterView(QWidget):
    def __init__(self, db_path: str, public_base_url: str):
        super().__init__()
        self.controller = UsuarioController(db_path, public_base_url)
        self._build_ui()

    # =====================================================
    # 🧱 CONSTRUCCIÓN DE INTERFAZ
    # =====================================================
    def _build_ui(self):
        self.setWindowTitle("Registro de Usuario - SIATLITE")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("🧾 Crear nueva cuenta de usuario")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        frame = QFrame()
        form_layout = QVBoxLayout(frame)
        form_layout.setSpacing(10)

        # Campos de entrada
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Nombre")

        self.inp_apellido = QLineEdit()
        self.inp_apellido.setPlaceholderText("Apellido")

        self.inp_email = QLineEdit()
        self.inp_email.setPlaceholderText("Correo electrónico")

        self.inp_pass = QLineEdit()
        self.inp_pass.setPlaceholderText("Contraseña")
        self.inp_pass.setEchoMode(QLineEdit.EchoMode.Password)

        # Botón
        self.btn_registrar = QPushButton("Registrarse")
        self.btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_registrar.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
        """)
        self.btn_registrar.clicked.connect(self._registrar)

        # Añadir widgets al layout
        form_layout.addWidget(self.inp_nombre)
        form_layout.addWidget(self.inp_apellido)
        form_layout.addWidget(self.inp_email)
        form_layout.addWidget(self.inp_pass)
        form_layout.addWidget(self.btn_registrar)

        layout.addWidget(title)
        layout.addWidget(frame)

    # =====================================================
    # 🚀 FUNCIÓN DE REGISTRO
    # =====================================================
    def _registrar(self):
        n = self.inp_nombre.text().strip()
        a = self.inp_apellido.text().strip()
        e = self.inp_email.text().strip()
        p = self.inp_pass.text().strip()

        if not all([n, a, e, p]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos.")
            return

        # Desactivar botón mientras se procesa
        self.btn_registrar.setEnabled(False)
        self.btn_registrar.setText("Registrando...")

        ok, msg = self.controller.registrar(n, a, e, p)

        # Mostrar resultado
        if ok:
            QMessageBox.information(self, "Registro exitoso", msg)
            self.inp_nombre.clear()
            self.inp_apellido.clear()
            self.inp_email.clear()
            self.inp_pass.clear()
        else:
            QMessageBox.warning(self, "Error", msg)

        # Restaurar botón
        self.btn_registrar.setEnabled(True)
        self.btn_registrar.setText("Registrarse")
