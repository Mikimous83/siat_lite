from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal


class TableToolBar(QWidget):
    search = pyqtSignal(str)
    add = pyqtSignal()
    refresh = pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        self.q = QLineEdit(); self.q.setPlaceholderText("Buscar por número de caso…")
        btn_add = QPushButton("Nuevo")
        btn_ref = QPushButton("Recargar")


        self.q.textChanged.connect(self.search.emit)
        btn_add.clicked.connect(self.add.emit)
        btn_ref.clicked.connect(self.refresh.emit)


        layout.addWidget(self.q, 1)
        layout.addWidget(btn_ref)
        layout.addWidget(btn_add)