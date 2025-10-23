"""
Vista de reportes y estadísticas
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from src.utils.styles import COLORS


class ReportesView(QWidget):
    """Vista de reportes y estadísticas"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # ========== TÍTULO ==========
        title = QLabel("📈 Generador de Reportes")
        title.setStyleSheet(f"""
            font-size: 18pt;
            font-weight: bold;
            color: {COLORS['text']};
            padding: 10px;
        """)
        layout.addWidget(title)

        # ========== TARJETAS DE REPORTES - FILA 1 ==========
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Reporte de accidentes por periodo
        card1 = self.create_report_card(
            "📊 Accidentes por Periodo",
            "Genera un reporte de todos los accidentes en un rango de fechas específico",
            "generar_periodo"
        )
        cards_layout.addWidget(card1)

        # Reporte por tipo
        card2 = self.create_report_card(
            "🚗 Accidentes por Tipo",
            "Estadísticas detalladas de accidentes clasificados por tipo",
            "generar_tipo"
        )
        cards_layout.addWidget(card2)

        # Reporte por ubicación
        card3 = self.create_report_card(
            "📍 Puntos Críticos",
            "Identifica las zonas con mayor incidencia de accidentes",
            "generar_ubicacion"
        )
        cards_layout.addWidget(card3)

        layout.addLayout(cards_layout)

        # ========== TARJETAS DE REPORTES - FILA 2 ==========
        cards_layout2 = QHBoxLayout()
        cards_layout2.setSpacing(20)

        card4 = self.create_report_card(
            "⚠️ Gravedad y Víctimas",
            "Análisis de accidentes por nivel de gravedad y número de víctimas",
            "generar_gravedad"
        )
        cards_layout2.addWidget(card4)

        card5 = self.create_report_card(
            "👥 Conductores Recurrentes",
            "Lista de conductores involucrados en múltiples accidentes",
            "generar_conductores"
        )
        cards_layout2.addWidget(card5)

        card6 = self.create_report_card(
            "📈 Reporte Completo",
            "Reporte ejecutivo con todas las estadísticas del sistema",
            "generar_completo"
        )
        cards_layout2.addWidget(card6)

        layout.addLayout(cards_layout2)

        # ========== TARJETAS DE REPORTES - FILA 3 ==========
        cards_layout3 = QHBoxLayout()
        cards_layout3.setSpacing(20)

        card7 = self.create_report_card(
            "🌤️ Por Condiciones",
            "Análisis de accidentes según condiciones climáticas e iluminación",
            "generar_condiciones"
        )
        cards_layout3.addWidget(card7)

        card8 = self.create_report_card(
            "📅 Tendencias Temporales",
            "Análisis de accidentes por mes, día de la semana y hora del día",
            "generar_tendencias"
        )
        cards_layout3.addWidget(card8)

        card9 = self.create_report_card(
            "🚙 Análisis de Vehículos",
            "Estadísticas de vehículos involucrados por tipo y marca",
            "generar_vehiculos"
        )
        cards_layout3.addWidget(card9)

        layout.addLayout(cards_layout3)

        layout.addStretch()

    def create_report_card(self, title, description, action):
        """
        Crea una tarjeta de reporte

        Args:
            title: Título del reporte
            description: Descripción breve
            action: Acción a ejecutar
        """
        card = QFrame()
        card.setObjectName("cardFrame")
        card.setMinimumHeight(200)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        # Título
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: bold;
            color: {COLORS['primary']};
        """)
        lbl_title.setWordWrap(True)

        # Descripción
        lbl_desc = QLabel(description)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet(f"color: {COLORS['text_secondary']};")

        # Botón
        btn_generate = QPushButton("Generar Reporte")
        btn_generate.setObjectName("btnSuccess")
        btn_generate.setMinimumHeight(40)
        btn_generate.clicked.connect(lambda: self.generate_report(action))

        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_desc)
        card_layout.addStretch()
        card_layout.addWidget(btn_generate)

        return card

    def generate_report(self, report_type):
        """
        Genera un reporte

        Args:
            report_type: Tipo de reporte a generar
        """
        report_names = {
            'generar_periodo': 'Accidentes por Periodo',
            'generar_tipo': 'Accidentes por Tipo',
            'generar_ubicacion': 'Puntos Críticos',
            'generar_gravedad': 'Gravedad y Víctimas',
            'generar_conductores': 'Conductores Recurrentes',
            'generar_completo': 'Reporte Completo',
            'generar_condiciones': 'Por Condiciones',
            'generar_tendencias': 'Tendencias Temporales',
            'generar_vehiculos': 'Análisis de Vehículos'
        }

        report_name = report_names.get(report_type, 'Reporte')

        QMessageBox.information(
            self,
            "Generando Reporte",
            f"Generando reporte: {report_name}\n\n"
            f"Esta funcionalidad se implementará con los servicios de reportes.\n\n"
            f"El reporte incluirá:\n"
            f"• Análisis estadístico detallado\n"
            f"• Gráficos y visualizaciones\n"
            f"• Exportación a PDF y Excel"
        )