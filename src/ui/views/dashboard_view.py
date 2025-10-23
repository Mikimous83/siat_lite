from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
    QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from src.utils.styles import COLORS, get_stat_card_style
from src.models.database_connection import DatabaseConnection


class DashboardView(QWidget):
    """Vista principal del panel de control (Dashboard)"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection().connect()
        self.setup_ui()
        self.load_data()

    # =====================================================
    # INTERFAZ
    # =====================================================
    def setup_ui(self):
        """Crea toda la interfaz del dashboard"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # ---------- TARJETAS ----------
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.card_total = self.create_stat_card("Total Accidentes", "0", "📋", COLORS['primary'])
        self.card_mes = self.create_stat_card("Este Mes", "0", "📅", COLORS['success'])
        self.card_graves = self.create_stat_card("Graves", "0", "⚠️", COLORS['danger'])
        self.card_pendientes = self.create_stat_card("Pendientes", "0", "⏳", COLORS['warning'])

        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_mes)
        stats_layout.addWidget(self.card_graves)
        stats_layout.addWidget(self.card_pendientes)

        main_layout.addLayout(stats_layout)

        # ---------- TABLAS Y ESTADÍSTICAS ----------
        content_grid = QGridLayout()
        content_grid.setSpacing(20)

        self.recent_frame = self.create_recent_accidents_section()
        self.type_stats_frame = self.create_type_statistics_section()
        self.severity_stats_frame = self.create_severity_statistics_section()

        content_grid.addWidget(self.recent_frame, 0, 0, 1, 2)
        content_grid.addWidget(self.type_stats_frame, 1, 0)
        content_grid.addWidget(self.severity_stats_frame, 1, 1)

        main_layout.addLayout(content_grid)
        main_layout.addStretch()

        scroll.setWidget(content)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

    # =====================================================
    # SECCIONES
    # =====================================================
    def create_stat_card(self, title, value, icon, color):
        """Crea una tarjeta de resumen"""
        card = QFrame()
        card.setStyleSheet(get_stat_card_style(color))
        card.setMinimumHeight(140)

        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 36pt; color: {color};")

        value_label = QLabel(value)
        value_label.setObjectName("lblValue")
        value_label.setStyleSheet(f"font-size: 32pt; font-weight: bold; color: {color};")

        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 11pt; color: {COLORS['text_secondary']};")

        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        layout.addStretch()
        return card

    def create_recent_accidents_section(self):
        """Sección: Últimos accidentes"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("📋 Últimos Accidentes Registrados")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; padding-bottom: 10px;")
        layout.addWidget(title)

        self.table_recent = QTableWidget()
        self.table_recent.setColumnCount(6)
        self.table_recent.setHorizontalHeaderLabels([
            "N° Caso", "Fecha", "Hora", "Lugar", "Tipo", "Gravedad"
        ])
        self.table_recent.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_recent.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_recent.verticalHeader().setVisible(False)
        header = self.table_recent.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_recent.setMinimumHeight(300)

        layout.addWidget(self.table_recent)
        return frame

    def create_type_statistics_section(self):
        """Sección: Accidentes por tipo"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("📊 Accidentes por Tipo")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; padding-bottom: 10px;")
        layout.addWidget(title)
        self.type_stats_layout = QVBoxLayout()
        layout.addLayout(self.type_stats_layout)
        layout.addStretch()
        return frame

    def create_severity_statistics_section(self):
        """Sección: Accidentes por gravedad"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("⚠️ Accidentes por Gravedad")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; padding-bottom: 10px;")
        layout.addWidget(title)
        self.severity_stats_layout = QVBoxLayout()
        layout.addLayout(self.severity_stats_layout)
        layout.addStretch()
        return frame

    def create_stat_bar(self, label, value, total, color):
        """Crea una barra de progreso estadística"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        top = QHBoxLayout()
        lbl_name = QLabel(label)
        lbl_value = QLabel(str(value))
        lbl_value.setStyleSheet(f"color: {color}; font-weight: bold;")
        top.addWidget(lbl_name)
        top.addStretch()
        top.addWidget(lbl_value)
        layout.addLayout(top)

        percentage = (value / total * 100) if total > 0 else 0
        bar_bg = QFrame()
        bar_bg.setStyleSheet(f"background-color: {COLORS['dark_light']}; border-radius: 6px;")
        bar = QFrame(bar_bg)
        bar.setStyleSheet(f"background-color: {color}; border-radius: 6px;")
        bar.setFixedWidth(int(percentage * 2))  # ancho proporcional
        layout.addWidget(bar_bg)
        return container

    # =====================================================
    # CARGA DE DATOS
    # =====================================================
    def load_data(self):
        """Carga los datos del dashboard desde SQLite"""
        if not self.db:
            print("❌ No hay conexión a la base de datos.")
            return

        cursor = self.db.cursor()

        # --- TARJETAS PRINCIPALES ---
        cursor.execute("SELECT COUNT(*) FROM accidentes;")
        total_accidentes = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT COUNT(*) FROM accidentes 
            WHERE strftime('%m', fecha) = strftime('%m', 'now');
        """)
        accidentes_mes = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT COUNT(*) FROM accidentes a
            JOIN niveles_gravedad g ON a.id_gravedad = g.id_gravedad
            WHERE g.nivel LIKE '%Grave%';
        """)
        graves = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM accidentes WHERE estado_caso = 'Pendiente';")
        pendientes = cursor.fetchone()[0] or 0

        self.update_stat_card(self.card_total, str(total_accidentes))
        self.update_stat_card(self.card_mes, str(accidentes_mes))
        self.update_stat_card(self.card_graves, str(graves))
        self.update_stat_card(self.card_pendientes, str(pendientes))

        # --- TABLA DE ACCIDENTES RECIENTES ---
        cursor.execute("""
            SELECT 
                a.numero_caso, 
                a.fecha, 
                a.hora, 
                a.lugar,
                (SELECT descripcion FROM tipos_accidente t WHERE t.id_tipo = a.id_tipo),
                (SELECT nivel FROM niveles_gravedad g WHERE g.id_gravedad = a.id_gravedad)
            FROM accidentes a
            ORDER BY a.fecha DESC, a.hora DESC
            LIMIT 10;
        """)
        rows = cursor.fetchall()
        self.table_recent.setRowCount(len(rows))
        for row, data in enumerate(rows):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value) if value else "")
                if col == 5 and value == "Grave":
                    item.setForeground(Qt.GlobalColor.red)
                elif col == 5 and value == "Moderado":
                    item.setForeground(Qt.GlobalColor.darkYellow)
                self.table_recent.setItem(row, col, item)

        # --- ESTADÍSTICAS POR TIPO ---
        cursor.execute("""
            SELECT t.descripcion, COUNT(*)
            FROM accidentes a
            JOIN tipos_accidente t ON t.id_tipo = a.id_tipo
            GROUP BY t.descripcion;
        """)
        type_stats = cursor.fetchall()
        total_types = sum(v[1] for v in type_stats) or 1
        for label, value in type_stats:
            bar = self.create_stat_bar(label or "Sin tipo", value, total_types, COLORS['primary'])
            self.type_stats_layout.addWidget(bar)

        # --- ESTADÍSTICAS POR GRAVEDAD ---
        cursor.execute("""
            SELECT g.nivel, COUNT(*)
            FROM accidentes a
            JOIN niveles_gravedad g ON g.id_gravedad = a.id_gravedad
            GROUP BY g.nivel;
        """)
        severity_stats = cursor.fetchall()
        total_severity = sum(v[1] for v in severity_stats) or 1
        for label, value in severity_stats:
            bar = self.create_stat_bar(label or "Sin dato", value, total_severity, COLORS['danger'])
            self.severity_stats_layout.addWidget(bar)

        cursor.close()

    def update_stat_card(self, card, new_value):
        """Actualiza el número en las tarjetas"""
        for child in card.findChildren(QLabel):
            if child.objectName() == "lblValue":
                child.setText(new_value)
                break
