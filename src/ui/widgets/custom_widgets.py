from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QTableWidget, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from src.utils.styles import COLORS


class StatCard(QFrame):
    """Tarjeta de estadística personalizada"""

    def __init__(self, title, value, icon, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setup_ui(title, value, icon)

    def setup_ui(self, title, value, icon):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card']};
                border-radius: 12px;
                border-left: 4px solid {self.color};
                padding: 20px;
            }}
        """)
        self.setMinimumHeight(140)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Icono
        self.lbl_icon = QLabel(icon)
        self.lbl_icon.setStyleSheet(f"font-size: 36pt; color: {self.color};")

        # Valor
        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"font-size: 32pt; font-weight: bold; color: {self.color};")

        # Título
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet(f"font-size: 11pt; color: {COLORS['text_secondary']};")

        layout.addWidget(self.lbl_icon)
        layout.addWidget(self.lbl_value)
        layout.addWidget(self.lbl_title)
        layout.addStretch()

    def update_value(self, new_value):
        """Actualiza el valor mostrado"""
        self.lbl_value.setText(str(new_value))


class SearchBar(QWidget):
    """Barra de búsqueda con botón"""

    search_requested = pyqtSignal(str)  # Señal cuando se solicita búsqueda

    def __init__(self, placeholder="Buscar...", parent=None):
        super().__init__(parent)
        self.setup_ui(placeholder)

    def setup_ui(self, placeholder):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Campo de búsqueda
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText(placeholder)
        self.txt_search.setMinimumWidth(300)
        self.txt_search.returnPressed.connect(self.perform_search)

        # Botón de búsqueda
        self.btn_search = QPushButton("🔍 Buscar")
        self.btn_search.setMinimumHeight(40)
        self.btn_search.clicked.connect(self.perform_search)

        # Botón limpiar
        self.btn_clear = QPushButton("✖")
        self.btn_clear.setObjectName("btnSecondary")
        self.btn_clear.setMaximumWidth(40)
        self.btn_clear.setMinimumHeight(40)
        self.btn_clear.clicked.connect(self.clear_search)

        layout.addWidget(QLabel("🔍"))
        layout.addWidget(self.txt_search)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.btn_clear)

    def perform_search(self):
        """Emite señal de búsqueda"""
        text = self.txt_search.text().strip()
        self.search_requested.emit(text)

    def clear_search(self):
        """Limpia el campo de búsqueda"""
        self.txt_search.clear()
        self.search_requested.emit("")

    def get_text(self):
        """Obtiene el texto de búsqueda"""
        return self.txt_search.text()


class InfoCard(QFrame):
    """Tarjeta de información general"""

    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setup_ui(title, content)

    def setup_ui(self, title, content):
        self.setObjectName("cardFrame")
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: bold;
            color: {COLORS['primary']};
        """)

        # Contenido
        self.lbl_content = QLabel(content)
        self.lbl_content.setWordWrap(True)
        self.lbl_content.setStyleSheet(f"color: {COLORS['text']};")

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_content)
        layout.addStretch()

    def update_content(self, content):
        """Actualiza el contenido"""
        self.lbl_content.setText(content)


class ActionButton(QPushButton):
    """Botón de acción personalizado"""

    def __init__(self, text, icon="", style_type="primary", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}" if icon else text)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if style_type == "success":
            self.setObjectName("btnSuccess")
        elif style_type == "danger":
            self.setObjectName("btnDanger")
        elif style_type == "warning":
            self.setObjectName("btnWarning")
        elif style_type == "secondary":
            self.setObjectName("btnSecondary")


class ProgressCard(QFrame):
    """Tarjeta con barra de progreso"""

    def __init__(self, label, value, total, color, parent=None):
        super().__init__(parent)
        self.total = total
        self.color = color
        self.setup_ui(label, value)

    def setup_ui(self, label, value):
        self.setObjectName("cardFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Fila superior: label y valor
        top_layout = QHBoxLayout()

        self.lbl_name = QLabel(label)
        self.lbl_name.setStyleSheet("font-weight: 500; font-size: 10pt;")

        self.lbl_value = QLabel(str(value))
        self.lbl_value.setStyleSheet(f"color: {self.color}; font-weight: bold; font-size: 10pt;")

        top_layout.addWidget(self.lbl_name)
        top_layout.addStretch()
        top_layout.addWidget(self.lbl_value)

        layout.addLayout(top_layout)

        # Barra de progreso
        self.progress_container = QFrame()
        self.progress_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['dark_light']};
                border-radius: 6px;
                max-height: 12px;
                min-height: 12px;
            }}
        """)

        self.progress_bar = QFrame(self.progress_container)
        percentage = (value / self.total * 100) if self.total > 0 else 0
        width = int(200 * percentage / 100)

        self.progress_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color};
                border-radius: 6px;
                max-height: 12px;
                min-height: 12px;
            }}
        """)
        self.progress_bar.setFixedWidth(width)

        layout.addWidget(self.progress_container)

    def update_progress(self, new_value):
        """Actualiza el progreso"""
        self.lbl_value.setText(str(new_value))
        percentage = (new_value / self.total * 100) if self.total > 0 else 0
        width = int(200 * percentage / 100)
        self.progress_bar.setFixedWidth(width)


class EmptyState(QWidget):
    """Widget para mostrar estado vacío"""

    def __init__(self, icon="📭", title="No hay datos", message="", action_text="", parent=None):
        super().__init__(parent)
        self.setup_ui(icon, title, message, action_text)

    def setup_ui(self, icon, title, message, action_text):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Icono grande
        lbl_icon = QLabel(icon)
        lbl_icon.setStyleSheet("font-size: 72pt; color: #6C757D;")
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"""
            font-size: 18pt;
            font-weight: bold;
            color: {COLORS['text']};
        """)
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Mensaje
        lbl_message = QLabel(message)
        lbl_message.setStyleSheet(f"font-size: 11pt; color: {COLORS['text_secondary']};")
        lbl_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_message.setWordWrap(True)

        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_message)

        # Botón de acción opcional
        if action_text:
            btn_action = ActionButton(action_text, "➕", "success")
            btn_action.setMaximumWidth(200)
            layout.addWidget(btn_action, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()


class FilterGroup(QFrame):
    """Grupo de filtros"""

    filters_changed = pyqtSignal(dict)  # Señal cuando cambian los filtros

    def __init__(self, filters_config, parent=None):
        super().__init__(parent)
        self.filters = {}
        self.setup_ui(filters_config)

    def setup_ui(self, filters_config):
        self.setObjectName("cardFrame")
        self.setMaximumHeight(90)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # Crear filtros según configuración
        for filter_name, filter_data in filters_config.items():
            lbl = QLabel(filter_data['label'])
            widget = filter_data['widget']
            self.filters[filter_name] = widget

            # Conectar señales
            if hasattr(widget, 'currentTextChanged'):
                widget.currentTextChanged.connect(self.on_filter_changed)
            elif hasattr(widget, 'textChanged'):
                widget.textChanged.connect(self.on_filter_changed)

            layout.addWidget(lbl)
            layout.addWidget(widget)

        # Botón limpiar
        btn_clear = QPushButton("🔄 Limpiar")
        btn_clear.setObjectName("btnSecondary")
        btn_clear.clicked.connect(self.clear_filters)
        layout.addWidget(btn_clear)

        layout.addStretch()

    def on_filter_changed(self):
        """Emite señal cuando cambia algún filtro"""
        filter_values = self.get_filter_values()
        self.filters_changed.emit(filter_values)

    def get_filter_values(self):
        """Obtiene los valores actuales de los filtros"""
        values = {}
        for name, widget in self.filters.items():
            if hasattr(widget, 'currentText'):
                values[name] = widget.currentText()
            elif hasattr(widget, 'text'):
                values[name] = widget.text()
        return values

    def clear_filters(self):
        """Limpia todos los filtros"""
        for widget in self.filters.values():
            if hasattr(widget, 'setCurrentIndex'):
                widget.setCurrentIndex(0)
            elif hasattr(widget, 'clear'):
                widget.clear()
        self.on_filter_changed()


class LoadingOverlay(QFrame):
    """Overlay de carga"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.hide()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel("⏳ Cargando...")
        lbl.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: white;
        """)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl)

    def show_loading(self):
        """Muestra el overlay"""
        if self.parent():
            self.setGeometry(self.parent().rect())
        self.show()
        self.raise_()

    def hide_loading(self):
        """Oculta el overlay"""
        self.hide()