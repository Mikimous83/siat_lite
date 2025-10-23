"""
Ventana principal de SIATLITE con navegación lateral moderna
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import sys

# Importa tus vistas
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.accidentes_view import AccidentesView
from src.ui.views.personas_view import PersonasView
from src.ui.views.vehiculos_view import VehiculosView
from src.ui.views.reportes_view import ReportesView
from src.ui.views.configuracion_view import ConfiguracionView
from src.ui.views.usuario_view import UsuarioRegisterView  # ✅ vista de registro

# Conexión a la base
from src.models.database_connection import DatabaseConnection
from src.ui.views.login_view import LoginView  # ✅ para reabrir login al cerrar sesión


class MainWindow(QMainWindow):
    def __init__(self, usuario_activo=None):
        super().__init__()
        self.usuario_activo = usuario_activo  # 👈 guarda los datos del login
        self.setWindowTitle("SIATLITE - Sistema de Accidentes de Tránsito")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)

        # Instancia de conexión a la base
        self.db = DatabaseConnection()

        self.setup_ui()

    # =====================================================
    # INTERFAZ PRINCIPAL
    # =====================================================
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar y contenido
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        self.content_stack = QStackedWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        self.header = self.create_header()
        content_layout.addWidget(self.header)
        content_layout.addWidget(self.content_stack)

        # Contenedor del contenido
        content_wrapper = QWidget()
        content_wrapper.setLayout(content_layout)
        main_layout.addWidget(content_wrapper, 1)

        # Cargar vistas
        self.setup_views()

        # Mostrar dashboard al inicio
        self.show_dashboard()

    # =====================================================
    # COMPONENTES DE UI
    # =====================================================
    def create_sidebar(self):
        """Crea el menú lateral"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebarFrame")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)

        # Logo
        logo_label = QLabel("🚦 SIATLITE")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #2A82DA;")

        subtitle = QLabel("Sistema de Accidentes")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 9pt; color: #9A9A9A;")

        layout.addWidget(logo_label)
        layout.addWidget(subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #404050; max-height: 2px;")
        layout.addWidget(separator)
        layout.addSpacing(10)

        # Botones del menú lateral
        self.btn_dashboard = self.create_menu_button("📊 Dashboard", True)
        self.btn_accidentes = self.create_menu_button("🚨 Accidentes")
        self.btn_personas = self.create_menu_button("👥 Personas")
        self.btn_vehiculos = self.create_menu_button("🚗 Vehículos")
        self.btn_reportes = self.create_menu_button("📈 Reportes")
        self.btn_config = self.create_menu_button("⚙️ Configuración")
        self.btn_usuarios = self.create_menu_button("👤 Usuarios")

        # Conectar señales
        self.btn_dashboard.clicked.connect(self.show_dashboard)
        self.btn_accidentes.clicked.connect(self.show_accidentes)
        self.btn_personas.clicked.connect(self.show_personas)
        self.btn_vehiculos.clicked.connect(self.show_vehiculos)
        self.btn_reportes.clicked.connect(self.show_reportes)
        self.btn_config.clicked.connect(self.show_configuracion)
        self.btn_usuarios.clicked.connect(self.show_usuarios)

        # Agregar botones
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_accidentes)
        layout.addWidget(self.btn_personas)
        layout.addWidget(self.btn_vehiculos)
        layout.addWidget(self.btn_reportes)
        layout.addWidget(self.btn_config)
        layout.addWidget(self.btn_usuarios)

        layout.addStretch()

        # Pie de usuario dinámico
        user_frame = QFrame()
        user_frame.setStyleSheet("""
            QFrame {
                background-color: #282838;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        user_layout = QVBoxLayout(user_frame)

        nombre = self.usuario_activo.get("nombre", "Invitado")
        apellido = self.usuario_activo.get("apellido", "")
        email = self.usuario_activo.get("email", "")
        rol = self.usuario_activo.get("rol", "Usuario")

        user_label = QLabel(f"👤 Usuario: {nombre} {apellido}")
        user_label.setStyleSheet("font-weight: bold; font-size: 10pt;")

        role_label = QLabel(f"Rol: {rol}")
        role_label.setStyleSheet("font-size: 9pt; color: #9A9A9A;")

        email_label = QLabel(f"📧 {email}")
        email_label.setStyleSheet("font-size: 8pt; color: #AAAAAA;")

        btn_logout = QPushButton("🚪 Cerrar Sesión")
        btn_logout.setObjectName("btnDanger")
        btn_logout.clicked.connect(self.logout)
        btn_logout.setMaximumHeight(35)

        user_layout.addWidget(user_label)
        user_layout.addWidget(role_label)
        user_layout.addWidget(email_label)
        user_layout.addSpacing(10)
        user_layout.addWidget(btn_logout)

        layout.addWidget(user_frame)
        return sidebar

    def create_menu_button(self, text, checked=False):
        btn = QPushButton(text)
        btn.setObjectName("sidebarButton")
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setMinimumHeight(45)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def create_header(self):
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1E1E28;
                border-bottom: 2px solid #404050;
            }
        """)
        header.setMinimumHeight(70)
        header.setMaximumHeight(70)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 10, 30, 10)

        self.section_title = QLabel("Dashboard")
        self.section_title.setStyleSheet("font-size: 20pt; font-weight: bold; color: #DCDCDC;")
        layout.addWidget(self.section_title)
        layout.addStretch()

        btn_nuevo = QPushButton("➕ Nuevo Accidente")
        btn_nuevo.setObjectName("btnSuccess")
        btn_nuevo.clicked.connect(self.nuevo_accidente)
        btn_nuevo.setMinimumHeight(40)
        btn_nuevo.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(btn_nuevo)
        return header

    # =====================================================
    # CARGA DE VISTAS
    # =====================================================
    def setup_views(self):
        """Carga todas las vistas al Stack"""
        self.dashboard_view = DashboardView()
        self.accidentes_view = AccidentesView()
        self.personas_view = PersonasView(self.db)
        self.vehiculos_view = VehiculosView(self.db)
        self.reportes_view = ReportesView()
        self.configuracion_view = ConfiguracionView()

        db_path = r"D:\programacion\python\avanzada\IIICICICLO\siatlite\data\siatlite.db"
        public_base_url = "http://localhost"
        self.usuarios_view = UsuarioRegisterView(db_path, public_base_url)

        for view in [
            self.dashboard_view, self.accidentes_view, self.personas_view,
            self.vehiculos_view, self.reportes_view, self.configuracion_view,
            self.usuarios_view
        ]:
            self.content_stack.addWidget(view)

    # =====================================================
    # NAVEGACIÓN
    # =====================================================
    def uncheck_all_menu_buttons(self):
        for btn in [
            self.btn_dashboard, self.btn_accidentes, self.btn_personas,
            self.btn_vehiculos, self.btn_reportes, self.btn_config,
            self.btn_usuarios
        ]:
            btn.setChecked(False)

    def show_dashboard(self):
        self.uncheck_all_menu_buttons()
        self.btn_dashboard.setChecked(True)
        self.section_title.setText("📊 Dashboard")
        self.content_stack.setCurrentWidget(self.dashboard_view)

    def show_accidentes(self):
        self.uncheck_all_menu_buttons()
        self.btn_accidentes.setChecked(True)
        self.section_title.setText("🚨 Gestión de Accidentes")
        self.content_stack.setCurrentWidget(self.accidentes_view)

    def show_personas(self):
        self.uncheck_all_menu_buttons()
        self.btn_personas.setChecked(True)
        self.section_title.setText("👥 Personas Involucradas")
        self.content_stack.setCurrentWidget(self.personas_view)

    def show_vehiculos(self):
        self.uncheck_all_menu_buttons()
        self.btn_vehiculos.setChecked(True)
        self.section_title.setText("🚗 Vehículos Involucrados")
        self.content_stack.setCurrentWidget(self.vehiculos_view)

    def show_reportes(self):
        self.uncheck_all_menu_buttons()
        self.btn_reportes.setChecked(True)
        self.section_title.setText("📈 Reportes y Estadísticas")
        self.content_stack.setCurrentWidget(self.reportes_view)

    def show_configuracion(self):
        self.uncheck_all_menu_buttons()
        self.btn_config.setChecked(True)
        self.section_title.setText("⚙️ Configuración del Sistema")
        self.content_stack.setCurrentWidget(self.configuracion_view)

    def show_usuarios(self):
        self.uncheck_all_menu_buttons()
        self.btn_usuarios.setChecked(True)
        self.section_title.setText("👤 Gestión de Usuarios")
        self.content_stack.setCurrentWidget(self.usuarios_view)

    # =====================================================
    # ACCIONES DEL HEADER
    # =====================================================
    def nuevo_accidente(self):
        self.show_accidentes()
        if hasattr(self.accidentes_view, "abrir_formulario_nuevo"):
            self.accidentes_view.abrir_formulario_nuevo()

    # =====================================================
    # CIERRE DE SESIÓN
    # =====================================================
    def logout(self):
        reply = QMessageBox.question(
            self, "Cerrar Sesión",
            "¿Está seguro que desea cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.hide()
            self.reabrir_login()

    def reabrir_login(self):
        """Reabre la ventana de login sin cerrar la app"""
        login = LoginView(r"D:\programacion\python\avanzada\IIICICLO\siatlite\data\siatlite.db")
        if login.exec() == login.DialogCode.Accepted:
            usuario = login.usuario_autenticado
            self.__init__(usuario)
            self.show()
        else:
            sys.exit(0)
