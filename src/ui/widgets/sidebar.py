from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class SideBar(QWidget):
    navigate_to = pyqtSignal(str)


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)


        layout = QVBoxLayout(self); layout.setContentsMargins(8,8,8,8); layout.setSpacing(6)
        self.buttons = {}
        for name in ("Accidentes", "Personas", "Vehículos", "Catálogos", "Auditoría"):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self.navigate_to.emit(n))
            layout.addWidget(btn)
            self.buttons[name] = btn
        layout.addStretch(1)


    def set_active(self, name: str):
        for n, b in self.buttons.items():
            b.setChecked(n == name)