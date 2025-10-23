"""
Vista de configuración del sistema
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from src.utils.styles import COLORS


class ConfiguracionView(QWidget):
    """Vista de configuración del sistema"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # ========== TÍTULO ==========
        title = QLabel("⚙️ Configuración del Sistema")
        title.setStyleSheet(f"""
            font-size: 18pt;
            font-weight: bold;
            color: {COLORS['text']};
            padding: 10px;
        """)
        layout.addWidget(title)

        # Grid de opciones
        grid = QVBoxLayout()
        grid.setSpacing(20)

        # ========== GESTIÓN DE CATÁLOGOS ==========
        catalogos = self.create_config_section(
            "📚 Gestión de Catálogos",
            [
                ("Tipos de Accidente", "gestionar_tipos"),
                ("Tipos de Vehículo", "gestionar_vehiculos"),
                ("Niveles de Gravedad", "gestionar_gravedad"),
                ("Aseguradoras", "gestionar_aseguradoras"),
            ]
        )
        grid.addWidget(catalogos)

        # ========== GESTIÓN DE USUARIOS ==========
        usuarios = self.create_config_section(
            "👥 Gestión de Usuarios",
            [
                ("Usuarios del Sistema", "gestionar_usuarios"),
                ("Roles y Permisos", "gestionar_roles"),
                ("Comisarías", "gestionar_comisarias"),
            ]
        )
        grid.addWidget(usuarios)

        # ========== CONFIGURACIÓN GENERAL ==========
        general = self.create_config_section(
            "🔧 Configuración General",
            [
                ("Base de Datos", "config_database"),
                ("Respaldos", "config_backup"),
                ("Preferencias", "config_preferences"),
            ]
        )
        grid.addWidget(general)

        # ========== SISTEMA ==========
        sistema = self.create_config_section(
            "💻 Sistema",
            [
                ("Información del Sistema", "info_sistema"),
                ("Logs del Sistema", "ver_logs"),
                ("Acerca de", "acerca_de"),
            ]
        )
        grid.addWidget(sistema)

        layout.addLayout(grid)
        layout.addStretch()

    def create_config_section(self, title, buttons):
        """
        Crea una sección de configuración

        Args:
            title: Título de la sección
            buttons: Lista de tuplas (texto_boton, accion)
        """
        frame = QFrame()
        frame.setObjectName("cardFrame")

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setSpacing(15)

        # Título de sección
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: bold;
            color: {COLORS['primary']};
        """)
        frame_layout.addWidget(lbl_title)

        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        for btn_text, action in buttons:
            btn = QPushButton(btn_text)
            btn.setMinimumHeight(45)
            btn.clicked.connect(lambda checked, a=action: self.open_config(a))
            buttons_layout.addWidget(btn)

        frame_layout.addLayout(buttons_layout)

        return frame

    def open_config(self, config_type):
        """
        Abre una configuración específica

        Args:
            config_type: Tipo de configuración a abrir
        """
        config_messages = {
            # Catálogos
            'gestionar_tipos': 'Gestión de Tipos de Accidente',
            'gestionar_vehiculos': 'Gestión de Tipos de Vehículo',
            'gestionar_gravedad': 'Gestión de Niveles de Gravedad',
            'gestionar_aseguradoras': 'Gestión de Aseguradoras',

            # Usuarios
            'gestionar_usuarios': 'Gestión de Usuarios del Sistema',
            'gestionar_roles': 'Gestión de Roles y Permisos',
            'gestionar_comisarias': 'Gestión de Comisarías',

            # General
            'config_database': 'Configuración de Base de Datos',
            'config_backup': 'Configuración de Respaldos',
            'config_preferences': 'Preferencias del Sistema',

            # Sistema
            'info_sistema': 'Información del Sistema',
            'ver_logs': 'Logs del Sistema',
            'acerca_de': 'Acerca de SIATLITE'
        }

        title = config_messages.get(config_type, 'Configuración')

        if config_type == 'acerca_de':
            self.mostrar_acerca_de()
        elif config_type == 'info_sistema':
            self.mostrar_info_sistema()
        else:
            QMessageBox.information(
                self,
                title,
                f"{title}\n\nEsta funcionalidad se implementará próximamente.\n\n"
                f"Permitirá configurar y administrar:\n"
                f"• Agregar, editar y eliminar registros\n"
                f"• Establecer valores predeterminados\n"
                f"• Gestionar permisos y accesos"
            )

    def mostrar_acerca_de(self):
        """Muestra información sobre el sistema"""
        QMessageBox.about(
            self,
            "Acerca de SIATLITE",
            "<h2>🚦 SIATLITE</h2>"
            "<p><b>Sistema de Información de Accidentes de Tránsito y Transporte</b></p>"
            "<p>Versión: 1.0.0</p>"
            "<p>Fecha: Octubre 2025</p>"
            "<hr>"
            "<p><b>Desarrollado para:</b><br>"
            "Gestión integral de accidentes de tránsito</p>"
            "<hr>"
            "<p><b>Características:</b></p>"
            "<ul>"
            "<li>Registro de accidentes</li>"
            "<li>Gestión de personas y vehículos</li>"
            "<li>Generación de reportes</li>"
            "<li>Análisis estadístico</li>"
            "<li>Sistema multi-usuario</li>"
            "</ul>"
            "<hr>"
            "<p>© 2025 SIATLITE - Todos los derechos reservados</p>"
        )

    def mostrar_info_sistema(self):
        """Muestra información técnica del sistema"""
        import sys
        from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
        import platform
        import sqlite3

        info = f"""
<h3>📊 Información del Sistema</h3>

<b>Sistema Operativo:</b><br>
• SO: {platform.system()} {platform.release()}<br>
• Versión: {platform.version()}<br>
• Arquitectura: {platform.machine()}<br>

<b>Python:</b><br>
• Versión: {sys.version.split()[0]}<br>
• Implementación: {platform.python_implementation()}<br>

<b>PyQt6:</b><br>
• PyQt6: {PYQT_VERSION_STR}<br>
• Qt: {QT_VERSION_STR}<br>

<b>Base de Datos:</b><br>
• SQLite: {sqlite3.sqlite_version}<br>
• Ubicación: database/siatlite.db<br>

<b>Recursos:</b><br>
• Memoria: {self.obtener_uso_memoria()}<br>
• Logs: logs/siatlite_*.log<br>
        """

        QMessageBox.information(
            self,
            "Información del Sistema",
            info
        )

    def obtener_uso_memoria(self):
        """Obtiene el uso de memoria aproximado"""
        try:
            import psutil
            process = psutil.Process()
            mem = process.memory_info().rss / 1024 / 1024  # En MB
            return f"{mem:.2f} MB"
        except:
            return "N/A"