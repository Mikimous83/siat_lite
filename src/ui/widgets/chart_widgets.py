"""
Widgets de gráficos usando PyQt6
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from src.utils.styles import COLORS


class BarChartWidget(QFrame):
    """Widget de gráfico de barras simple"""

    def __init__(self, data, title="", parent=None):
        super().__init__(parent)
        self.data = data  # Lista de tuplas: [(label, value, color), ...]
        self.title = title
        self.max_value = max([v for _, v, _ in data]) if data else 1
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("cardFrame")
        self.setMinimumHeight(300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet(f"""
                font-size: 14pt;
                font-weight: bold;
                color: {COLORS['text']};
                padding-bottom: 10px;
            """)
            layout.addWidget(title_label)

        # Widget de canvas para dibujar
        self.canvas = BarChartCanvas(self.data, self.max_value)
        layout.addWidget(self.canvas)

    def update_data(self, new_data):
        """Actualiza los datos del gráfico"""
        self.data = new_data
        self.max_value = max([v for _, v, _ in new_data]) if new_data else 1
        self.canvas.update_data(new_data, self.max_value)


class BarChartCanvas(QWidget):
    """Canvas para dibujar el gráfico de barras"""

    def __init__(self, data, max_value, parent=None):
        super().__init__(parent)
        self.data = data
        self.max_value = max_value
        self.setMinimumHeight(250)

    def update_data(self, new_data, max_value):
        """Actualiza los datos"""
        self.data = new_data
        self.max_value = max_value
        self.update()

    def paintEvent(self, event):
        """Dibuja el gráfico"""
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dimensiones
        width = self.width() - 40
        height = self.height() - 60
        margin_left = 20
        margin_bottom = 40

        # Calcular ancho de cada barra
        num_bars = len(self.data)
        bar_width = (width - (num_bars - 1) * 10) / num_bars

        # Dibujar barras
        x = margin_left
        for label, value, color in self.data:
            # Calcular altura de la barra
            bar_height = (value / self.max_value) * height if self.max_value > 0 else 0

            # Dibujar barra
            painter.setBrush(QColor(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(
                int(x),
                int(self.height() - margin_bottom - bar_height),
                int(bar_width),
                int(bar_height),
                5, 5
            )

            # Dibujar valor sobre la barra
            painter.setPen(QColor(COLORS['text']))
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            value_text = str(int(value))
            painter.drawText(
                int(x),
                int(self.height() - margin_bottom - bar_height - 5),
                int(bar_width),
                20,
                Qt.AlignmentFlag.AlignCenter,
                value_text
            )

            # Dibujar etiqueta debajo de la barra
            painter.setPen(QColor(COLORS['text_secondary']))
            painter.setFont(QFont("Segoe UI", 8))

            # Truncar label si es muy largo
            display_label = label[:10] + '...' if len(label) > 10 else label

            painter.drawText(
                int(x),
                int(self.height() - margin_bottom + 5),
                int(bar_width),
                30,
                Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                display_label
            )

            x += bar_width + 10


class PieChartWidget(QFrame):
    """Widget de gráfico circular simple"""

    def __init__(self, data, title="", parent=None):
        super().__init__(parent)
        self.data = data  # Lista de tuplas: [(label, value, color), ...]
        self.title = title
        self.total = sum([v for _, v, _ in data]) if data else 1
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("cardFrame")
        self.setMinimumHeight(350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet(f"""
                font-size: 14pt;
                font-weight: bold;
                color: {COLORS['text']};
                padding-bottom: 10px;
            """)
            layout.addWidget(title_label)

        # Widget de canvas
        self.canvas = PieChartCanvas(self.data, self.total)
        layout.addWidget(self.canvas)

    def update_data(self, new_data):
        """Actualiza los datos"""
        self.data = new_data
        self.total = sum([v for _, v, _ in new_data]) if new_data else 1
        self.canvas.update_data(new_data, self.total)


class PieChartCanvas(QWidget):
    """Canvas para dibujar gráfico circular"""

    def __init__(self, data, total, parent=None):
        super().__init__(parent)
        self.data = data
        self.total = total
        self.setMinimumHeight(300)

    def update_data(self, new_data, total):
        """Actualiza los datos"""
        self.data = new_data
        self.total = total
        self.update()

    def paintEvent(self, event):
        """Dibuja el gráfico circular"""
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dimensiones
        center_x = self.width() // 2
        center_y = self.height() // 2 - 20
        radius = min(center_x, center_y) - 80

        # Dibujar segmentos
        start_angle = 0

        for label, value, color in self.data:
            # Calcular ángulo del segmento
            angle = int((value / self.total) * 360 * 16) if self.total > 0 else 0

            # Dibujar segmento
            painter.setBrush(QColor(color))
            painter.setPen(QPen(QColor(COLORS['card']), 2))
            painter.drawPie(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2,
                start_angle,
                angle
            )

            start_angle += angle

        # Dibujar leyenda
        legend_y = center_y + radius + 30
        legend_x = 20

        painter.setFont(QFont("Segoe UI", 9))

        for i, (label, value, color) in enumerate(self.data):
            # Cuadrado de color
            painter.setBrush(QColor(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(legend_x, legend_y + i * 25, 15, 15)

            # Texto
            percentage = (value / self.total * 100) if self.total > 0 else 0
            text = f"{label}: {int(value)} ({percentage:.1f}%)"
            painter.setPen(QColor(COLORS['text']))
            painter.drawText(legend_x + 25, legend_y + i * 25 + 12, text)


class LineChartWidget(QFrame):
    """Widget de gráfico de líneas simple"""

    def __init__(self, data, title="", xlabel="", ylabel="", parent=None):
        super().__init__(parent)
        self.data = data  # Lista de tuplas: [(x, y), ...]
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("cardFrame")
        self.setMinimumHeight(300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet(f"""
                font-size: 14pt;
                font-weight: bold;
                color: {COLORS['text']};
                padding-bottom: 10px;
            """)
            layout.addWidget(title_label)

        # Widget de canvas
        self.canvas = LineChartCanvas(self.data, self.xlabel, self.ylabel)
        layout.addWidget(self.canvas)

    def update_data(self, new_data):
        """Actualiza los datos"""
        self.data = new_data
        self.canvas.update_data(new_data)


class LineChartCanvas(QWidget):
    """Canvas para dibujar gráfico de líneas"""

    def __init__(self, data, xlabel="", ylabel="", parent=None):
        super().__init__(parent)
        self.data = data
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.setMinimumHeight(250)

    def update_data(self, new_data):
        """Actualiza los datos"""
        self.data = new_data
        self.update()

    def paintEvent(self, event):
        """Dibuja el gráfico de líneas"""
        if not self.data or len(self.data) < 2:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dimensiones
        margin = 40
        width = self.width() - 2 * margin
        height = self.height() - 2 * margin

        # Calcular valores mínimos y máximos
        y_values = [y for _, y in self.data]
        min_y = min(y_values)
        max_y = max(y_values)
        range_y = max_y - min_y if max_y != min_y else 1

        # Dibujar ejes
        painter.setPen(QPen(QColor(COLORS['border']), 2))
        painter.drawLine(margin, margin, margin, self.height() - margin)  # Eje Y
        painter.drawLine(margin, self.height() - margin,
                         self.width() - margin, self.height() - margin)  # Eje X

        # Dibujar línea
        painter.setPen(QPen(QColor(COLORS['primary']), 3))

        points = []
        for i, (x_label, y) in enumerate(self.data):
            x = margin + (i / (len(self.data) - 1)) * width
            y_scaled = self.height() - margin - ((y - min_y) / range_y) * height
            points.append((int(x), int(y_scaled)))

        for i in range(len(points) - 1):
            painter.drawLine(points[i][0], points[i][1],
                             points[i + 1][0], points[i + 1][1])

        # Dibujar puntos
        painter.setBrush(QColor(COLORS['primary']))
        for x, y in points:
            painter.drawEllipse(x - 4, y - 4, 8, 8)

        # Dibujar valores
        painter.setFont(QFont("Segoe UI", 8))
        painter.setPen(QColor(COLORS['text_secondary']))

        for i, (x_label, y) in enumerate(self.data):
            x, y_pos = points[i]

            # Valor Y sobre el punto
            value_text = str(int(y))
            painter.drawText(x - 15, y_pos - 10, 30, 20,
                             Qt.AlignmentFlag.AlignCenter, value_text)

            # Label X debajo del eje
            label_text = str(x_label)[:10]
            painter.drawText(x - 30, self.height() - margin + 5, 60, 30,
                             Qt.AlignmentFlag.AlignCenter, label_text)


# Ejemplo de uso
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Ejemplos de Gráficos")
    window.setGeometry(100, 100, 900, 700)

    central = QWidget()
    layout = QVBoxLayout(central)

    # Gráfico de barras
    bar_data = [
        ("Colisión", 45, COLORS['primary']),
        ("Choque", 32, COLORS['info']),
        ("Atropello", 28, COLORS['danger']),
        ("Volcadura", 20, COLORS['warning']),
    ]
    bar_chart = BarChartWidget(bar_data, "Accidentes por Tipo")
    layout.addWidget(bar_chart)

    # Gráfico circular
    pie_data = [
        ("Leve", 89, COLORS['success']),
        ("Moderado", 38, COLORS['warning']),
        ("Grave", 18, COLORS['danger']),
    ]
    pie_chart = PieChartWidget(pie_data, "Accidentes por Gravedad")
    layout.addWidget(pie_chart)

    window.setCentralWidget(central)
    window.show()

    sys.exit(app.exec())